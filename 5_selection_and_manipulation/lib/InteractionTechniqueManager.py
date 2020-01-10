#!/usr/bin/python3

# import avango-guacamole libraries
import avango
import avango.gua
import avango.script
from avango.script import field_has_changed

# import application libraries
from lib.VirtualHandInteraction import *
from lib.VirtualRayInteraction import *


# creates the interaction techniques and implements a toggling mechanism between them
class InteractionTechniqueManager(avango.script.Script):

    # input fields
    sf_list_button = avango.SFBool()
    sf_list_button.value = False

    def __init__(self):
        self.super(InteractionTechniqueManager).__init__()
        self.hand_interaction = VirtualHandInteraction()
        self.ray_interaction = VirtualRayInteraction()
        self.hand_interaction.enable(True)
        self.controller_node = None
        self.active_technique = 0

    # sets the correct inputs to be used for all interaction techniques
    def set_inputs(self, scenegraph, head_node, controller_node, controller_sensor):
        self.hand_interaction.set_inputs(
            scenegraph, head_node, controller_node, controller_sensor)
        self.ray_interaction.set_inputs(
            scenegraph, head_node, controller_node, controller_sensor)
        self.controller_node = controller_node
        self.controller_node.Children.value[0].Tags.value.append('invisible')
        self.sf_list_button.connect_from(controller_sensor.Button1)

    # toggles between the two interaction techniques
    def switch_technique(self):
        if self.active_technique == 0:
            self.hand_interaction.enable(False)
            self.ray_interaction.enable(True)
            self.controller_node.Children.value[0].Tags.value.remove(
                'invisible')
            self.active_technique = 1
        else:
            self.ray_interaction.enable(False)
            self.hand_interaction.enable(True)
            self.active_technique = 0
            self.controller_node.Children.value[0].Tags.value.append(
                'invisible')

    # callend whenever sf_list_button changes
    @field_has_changed(sf_list_button)
    def sf_list_button_changed(self):
        if self.sf_list_button.value:
            self.switch_technique()
