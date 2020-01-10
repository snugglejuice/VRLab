#!/usr/bin/python3

# import avango-guacamole libraries
import avango
import avango.gua
import avango.script
from avango.script import field_has_changed

# import application libraries
import config
from lib.Picker import Picker

# import python libraries
import time


# implements interaction techniques based on a virtual hand
class VirtualRayInteraction(avango.script.Script):

    # input fields
    sf_touchpad_button = avango.SFBool()
    sf_touchpad_button.value = False

    sf_touchpad_y = avango.SFFloat()
    sf_touchpad_y.value = 0.0

    sf_grip_button = avango.SFBool()
    sf_grip_button.value = False

    def __init__(self):
        self.super(VirtualRayInteraction).__init__()
        # YOUR CODE - BEGIN (Add additional variables if necessary)
        self.current_object = None
        # YOUR CODE - END (Add additional variables if necessary)
        self.ray_max_distance = 10.0
        self.highlighted_object = None
        self.enable_flag = False
        self.create_resources()

    # enables and disables this interaction technique
    def enable(self, boolean):
        if boolean:
            self.ray_line.Tags.value.remove('invisible')
            self.depth_marker.Tags.value.remove('invisible')
        else:
            self.ray_line.Tags.value.append('invisible')
            self.depth_marker.Tags.value.append('invisible')
        self.enable_flag = boolean

    # creates the necessary geometries for this interaction technique
    def create_resources(self):
        line_loader = avango.gua.nodes.LineStripLoader()
        self.ray_line = line_loader.create_empty_geometry('ray_line', 'ray.lob')
        self.ray_line.ScreenSpaceLineWidth.value = 5.0
        self.ray_line.RenderVolumetric.value = False
        self.ray_line.Material.value.set_uniform(
            'Color', avango.gua.Vec4(1.0, 0.0, 0.0, 1.0))
        self.ray_line.start_vertex_list()
        self.ray_line.enqueue_vertex(0.0, 0.0, 0.0)
        self.ray_line.enqueue_vertex(0.0, 0.0, -self.ray_max_distance)
        self.ray_line.end_vertex_list()
        self.ray_line.Tags.value.append('invisible')

        loader = avango.gua.nodes.TriMeshLoader()
        self.depth_marker = loader.create_geometry_from_file('depth_marker',
                                                             'data/objects/sphere.obj',
                                                             avango.gua.LoaderFlags.LOAD_MATERIALS)
        self.depth_marker.Material.value.set_uniform(
            'Color', avango.gua.Vec4(1.0, 0.0, 0.0, 1.0))
        self.depth_marker.Tags.value.append('invisible')

    # sets the correct inputs to be used for this interaction technique
    def set_inputs(self, scenegraph, head_node, controller_node, controller_sensor):
        # store references and add geometries to scenegraph
        self.scenegraph = scenegraph
        self.head_node = head_node
        self.controller_node = controller_node
        self.controller_sensor = controller_sensor
        self.controller_node.Children.value.append(self.ray_line)
        self.controller_node.Children.value.append(self.depth_marker)
        self.sf_touchpad_button.connect_from(self.controller_sensor.Button4)
        self.sf_touchpad_y.connect_from(self.controller_sensor.Value2)
        self.sf_grip_button.connect_from(self.controller_sensor.Button2)

        # create picker
        self.picker = Picker(self.scenegraph)
        self.always_evaluate(True)

    # called every frame because of self.always_evaluate(True)
    def evaluate(self):
        if self.enable_flag:
            self.update_depth_marker()
            pick_result = self.compute_pick_result()
            self.update_highlights(pick_result)

    # updates the depth marker with respect to button inputs
    def update_depth_marker(self):
        # YOUR CODE - BEGIN (Exercises 5.5 - Depth Marker)
        change = avango.gua.Vec3(0,0,0)
        if(self.sf_touchpad_y.value > 0):
            change = avango.gua.Vec3(0,0,-0.001)
        elif(self.sf_touchpad_y.value < 0):
            change = avango.gua.Vec3(0,0,0.001)
        if ((self.depth_marker.Transform.value.get_translate()+change).z <= 0) & (self.depth_marker.Transform.value.get_translate().z >= -self.ray_max_distance-change.z):
            self.depth_marker.Transform.value = self.depth_marker.Transform.value * avango.gua.make_trans_mat(change)
        # YOUR CODE - END (Exercises 5.5 - Depth Marker)

    # computes intersections of the ray with the scene
    def compute_pick_result(self):
        # YOUR CODE - BEGIN (Exercises 5.4, 5.5 - Compute pick result)
        picker = Picker(self.scenegraph)
        position = self.depth_marker.WorldTransform.value.get_translate()#self.controller_node.WorldTransform.value.get_translate()
        direction = (self.depth_marker.WorldTransform.value * avango.gua.make_trans_mat(avango.gua.Vec3(0,0,-1))).get_translate() - self.depth_marker.WorldTransform.value.get_translate()
        direction.normalize()
        collide = picker.compute_all_pick_results(position,direction,self.ray_max_distance,['invisible'])
        if (len(collide) != 0):
            return collide[0]
        else:
            return None
        # YOUR CODE - END (Exercises 5.4, 5.5 - Compute pick result)

    # updates the object highlights with respect to a pick result
    def update_highlights(self, pick_result):
        if pick_result is not None:
            if self.highlighted_object is not None and \
               pick_result.Object.value.Name.value != self.highlighted_object.Name.value:
                self.remove_highlight()
            self.highlight_object(pick_result.Object.value)
        else:
            self.remove_highlight()

    # highlights an object when hit with the intersection ray
    def highlight_object(self, node):
        node.Material.value.set_uniform(
            'Color', avango.gua.Vec4(1.0, 1.0, 1.0, 1.0))
        self.highlighted_object = node

    # removes the current object highlight
    def remove_highlight(self):
        if self.highlighted_object is not None:
            color_id = int(self.highlighted_object.Tags.value[0])
            self.highlighted_object.Material.value.set_uniform(
                'Color', config.OBJECT_COLORS[color_id])
            self.highlighted_object = None

    # called whenever sf_grip_button button changes
    @field_has_changed(sf_grip_button)
    def sf_grip_button_changed(self):
        if self.sf_grip_button.value:
            # YOUR CODE - BEGIN (Exercise 5.6 - Object Teleport)
            if(self.highlighted_object != None):
                self.highlighted_object.Tags.value.append('invisible')
                self.current_object = self.highlighted_object
            elif (self.current_object != None):
                    #if ('invisible' in self.current_object.Tags.value):
                self.current_object.Tags.value.remove('invisible')
                trans = self.current_object.WorldTransform.value.get_translate()
                print(trans)
                self.current_object.WorldTransform.value = self.current_object.WorldTransform.value * \
                                                        avango.gua.make_trans_mat(self.depth_marker.WorldTransform.value.get_translate())# - self.current_object.WorldTransform.value.get_translate())
                print(self.current_object.WorldTransform.value)
                self.current_object = None
            # YOUR CODE - END (Exercise 5.6 - Object Teleport)
