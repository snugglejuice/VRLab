#!/usr/bin/python3

# import avango-guacamole libraries
import avango
import avango.daemon
import avango.gua
import avango.script
from avango.script import field_has_changed

# import application libraries
from lib.Picker import Picker

# import python libraries
import math
import time


# class realizing a jumping navigation technique
class JumpingNavigation(avango.script.Script):

    # input field
    sf_touchpad_button = avango.SFBool()
    sf_touchpad_button.value = False

    # output field
    sf_navigation_matrix = avango.gua.SFMatrix4()
    sf_navigation_matrix.value = avango.gua.make_identity_mat()

    def __init__(self):
        self.super(JumpingNavigation).__init__()
        self.transition_mode = 'instant'
        self.ray_max_distance = 30.0  # m
        self.animation_speed = 20.0  # m/s
        self.active = False
        self.animation_start_time = None
        self.animation_start_pos = None
        self.animation_target_pos = None

    # sets the inputs to be used for navigation
    def set_inputs(self, scenegraph, navigation_node, head_node, controller_node, controller_sensor):
        self.scenegraph = scenegraph
        self.navigation_node = navigation_node
        self.head_node = head_node
        self.controller_node = controller_node
        self.controller_sensor = controller_sensor
        self.build_resources()
        self.sf_touchpad_button.connect_from(self.controller_sensor.Button4)

    # builds the line node and intersection geometries
    def build_resources(self):
        # ray line node
        line_loader = avango.gua.nodes.LineStripLoader()
        self.ray_line = line_loader.create_empty_geometry(
            'ray_line', 'ray.lob')
        self.ray_line.ScreenSpaceLineWidth.value = 5.0
        self.ray_line.RenderVolumetric.value = False
        self.ray_line.Material.value.set_uniform(
            'Color', avango.gua.Vec4(1.0, 0.0, 0.0, 1.0))
        self.ray_line.Tags.value.append('invisible')
        self.controller_node.Children.value.append(self.ray_line)

        # intersection geometry
        self.intersection_pos_node = avango.gua.nodes.TransformNode(
            Name='intersection_position')
        self.scenegraph.Root.value.Children.value.append(
            self.intersection_pos_node)

        loader = avango.gua.nodes.TriMeshLoader()
        self.intersection_sphere = loader.create_geometry_from_file('intersection_sphere',
                                                                    'data/objects/sphere.obj',
                                                                    avango.gua.LoaderFlags.LOAD_MATERIALS)
        self.intersection_sphere.Transform.value = avango.gua.make_scale_mat(0.1)
        self.intersection_sphere.Material.value.set_uniform(
            'Color', avango.gua.Vec4(1.0, 0.0, 0.0, 1.0))
        self.intersection_sphere.Tags.value.append('invisible')
        self.intersection_pos_node.Children.value.append(
            self.intersection_sphere)

        # picker
        self.picker = Picker(self.scenegraph)
        self.always_evaluate(True)

    # enables or disables the navigation technique
    def enable(self, boolean):
        if boolean:
            self.sf_navigation_matrix.value = self.navigation_node.Transform.value
            self.navigation_node.Transform.disconnect()
            self.navigation_node.Transform.connect_from(
                self.sf_navigation_matrix)
        self.active = boolean

    # switches between instant and animated transition
    def set_transition_mode(self, mode):
        if mode == 'instant':
            self.transition_mode = 'instant'
        elif mode == 'animated':
            self.transition_mode = 'animated'
        self.animation_start_time = None
        self.animation_start_pos = None
        self.animation_target_pos = None

    # called every frame because of self.always_evaluate(True)
    # updates sf_navigation_matrix by processing the inputs
    # YOUR CODE - BEGIN (Exercises 6.2, 6.3 - Jumping Navigation)
    cur_distance = 0
    def evaluate(self):
        if (self.animation_start_pos != None):
            direction_animation =  self.animation_target_pos - self.animation_start_pos
            #direction_animation.normalize()
            speed = 2
            dist = math.sqrt(direction_animation.x**2 + direction_animation.z**2)
            total_time = dist / speed
            elapsed_time = time.time() - self.animation_start_time
            fraction = elapsed_time/total_time
            print(elapsed_time,total_time)
            self.navigation_node.Transform.value = avango.gua.make_trans_mat(self.animation_start_pos.x + fraction * direction_animation.x, self.animation_start_pos.y + fraction * direction_animation.y, self.animation_start_pos.z + fraction * direction_animation.z)
            #self.navigation_node.Transform.value*avango.gua.make_trans_mat(direction_animation.x*(elapsed_time/total_time),0,direction_animation.z*(elapsed_time/total_time))
            if (elapsed_time >= total_time):
                self.navigation_node.Transform.value = avango.gua.make_trans_mat(self.animation_target_pos.x, self.animation_target_pos.y, self.animation_target_pos.z)
                self.animation_start_pos = None
                self.animation_start_time = None
                self.animation_target_pos = None
        else:
            self.ray_line.start_vertex_list()
            self.ray_line.enqueue_vertex(0.0, 0.0, 0.0)
            self.ray_line.enqueue_vertex(0.0, 0.0, -self.cur_distance)
            self.ray_line.end_vertex_list()
            direction = (self.controller_node.Transform.value * avango.gua.make_trans_mat(0,0,-1)).get_translate() -self.controller_node.Transform.value.get_translate()
            direction.normalize()
            self.intersections = self.picker.compute_all_pick_results(self.controller_node.Transform.value.get_translate(),direction,self.ray_max_distance,['invisible'])
            if ( len(self.intersections) != 0 and self.sf_touchpad_button.value and self.active):
                self.intersection_pos_node.Transform.value = avango.gua.make_trans_mat(self.intersections[0].WorldPosition.value) * self.navigation_node.Transform.value
                self.intersection_sphere.Tags.value.remove('invisible')  
                self.cur_distance = abs((self.intersection_pos_node.Transform.value.get_translate() - self.controller_node.WorldTransform.value.get_translate()).z)
            else:
                self.cur_distance = self.ray_max_distance
                self.intersection_sphere.Tags.value.append('invisible')
        

    # called whenever sf_touchpad_button changes
    @field_has_changed(sf_touchpad_button)
    def sf_touchpad_button_changed(self):
        if self.active:
            if self.sf_touchpad_button.value:
                self.ray_line.Tags.value.remove('invisible')
            else:
                self.ray_line.Tags.value.append('invisible')
                self.intersection_sphere.Tags.value.append('invisible')
                if (self.transition_mode == "animated"):
                    self.animation_start_time = time.time()
                    self.animation_start_pos = self.navigation_node.WorldTransform.value.get_translate()
                    direction =  self.intersection_pos_node.WorldTransform.value.get_translate() - self.navigation_node.WorldTransform.value.get_translate()
                    self.animation_target_pos = (self.navigation_node.Transform.value*avango.gua.make_trans_mat(direction.x,0,direction.z)).get_translate()
                    #self.animation_target_pos = self.intersection_pos_node.WorldTransform.value.get_translate()
                    
                else:
                    direction =  self.intersection_pos_node.WorldTransform.value.get_translate() - self.navigation_node.WorldTransform.value.get_translate()
                    self.navigation_node.Transform.value = self.navigation_node.Transform.value*avango.gua.make_trans_mat(direction.x,0,direction.z)
                
    # YOUR CODE - END (Exercises 6.2, 6.3 - Jumping Navigation)