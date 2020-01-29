#!/usr/bin/python3

# import avango-guacamole libraries
import avango
import avango.gua
import avango.script
from avango.script import field_has_changed

# import application libraries
from lib.SteeringNavigation import *
from lib.JumpingNavigation import *


# creates the navigation techniques and implements a toggling mechanism between them
class NavigationTechniqueManager(avango.script.Script):

    # input fields
    sf_list_button = avango.SFBool()
    sf_list_button.value = False

    def __init__(self):
        self.super(NavigationTechniqueManager).__init__()
        self.steering_navigation = SteeringNavigation()
        self.jumping_navigation = JumpingNavigation()

    # sets the correct inputs to be used for all navigation techniques
    def set_inputs(self, scenegraph, navigation_node, head_node, controller_node, controller_sensor):
        self.steering_navigation.set_inputs(
            scenegraph, navigation_node, head_node, controller_node, controller_sensor)
        self.jumping_navigation.set_inputs(
            scenegraph, navigation_node, head_node, controller_node, controller_sensor)
        self.navigation_node = navigation_node
        self.head_node = head_node
        self.build_floor_highlight()
        self.steering_navigation.enable(True)
        self.active_technique = 0
        self.sf_list_button.connect_from(controller_sensor.Button1)

    # build floor highlight for head position
    def build_floor_highlight(self):
        loader = avango.gua.nodes.TriMeshLoader()
        self.floor_highlight = loader.create_geometry_from_file(
            'floor-highlight', 'data/objects/circle.obj', avango.gua.LoaderFlags.DEFAULTS)
        self.floor_highlight.Material.value.set_uniform(
            'Color', avango.gua.Vec4(0.0, 0.0, 0.0, 1.0))
        self.floor_highlight.Material.value.set_uniform('Emissivity', 1.0)
        self.navigation_node.Children.value.append(self.floor_highlight)
        self.always_evaluate(True)

    # called every frame because of self.always_evaluate(True)
    # updates the floor highlight
    def evaluate(self):
        head_position = self.head_node.Transform.value.get_translate()
        self.floor_highlight.Transform.value = avango.gua.make_trans_mat(head_position.x, 0.0011, head_position.z) * \
            avango.gua.make_rot_mat(-90, 1, 0, 0) * \
            avango.gua.make_scale_mat(0.05)

    # called whenever sf_list_button changes
    @field_has_changed(sf_list_button)
    def sf_list_button_changed(self):
        if self.sf_list_button.value:
            self.switch_technique()

    # toggles between the two navigation techniques
    def switch_technique(self):
        if self.active_technique == 0:
            self.jumping_navigation.enable(False)
            self.steering_navigation.set_steering_mode('position-directed')
            self.steering_navigation.enable(True)
            self.active_technique = 1
            print('Switched to position-directed steering.')
        elif self.active_technique == 1:
            self.steering_navigation.enable(False)
            self.jumping_navigation.set_transition_mode('instant')
            self.jumping_navigation.enable(True)
            self.active_technique = 2
            print('Switched to jumping with instant transition.')
        elif self.active_technique == 2:
            self.steering_navigation.enable(False)
            self.jumping_navigation.set_transition_mode('animated')
            self.jumping_navigation.enable(True)
            self.active_technique = 3
            print('Switched to jumping with animated transition.')
        else:
            self.jumping_navigation.enable(False)
            self.steering_navigation.set_steering_mode('pointing-directed')
            self.steering_navigation.enable(True)
            self.active_technique = 0
            print('Switched to pointing-directed steering.')
