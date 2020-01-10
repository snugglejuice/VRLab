#!/usr/bin/python3

# import avango-guacamole libraries
import avango
import avango.gua
import avango.script
from avango.script import field_has_changed

# import application libraries
import config
from lib.Picker import Picker


# implements interaction techniques based on a virtual hand
class VirtualHandInteraction(avango.script.Script):

    # input field
    sf_dragging_trigger = avango.SFBool()
    sf_dragging_trigger.value = False

    def __init__(self):
        self.super(VirtualHandInteraction).__init__()
        # YOUR CODE - BEGIN (Add additional variables if necessary)
        # ...
        # YOUR CODE - END (Add additional variables if necessary)
        self.highlighted_object = None
        self.dragging_object = None
        self.enable_flag = False
        self.create_resources()

    # enables and disables this interaction technique
    def enable(self, boolean):
        if boolean:
            self.hand_node.Tags.value.remove('invisible')
        else:
            self.hand_node.Tags.value.append('invisible')
        self.enable_flag = boolean

    # creates the necessary geometries for this interaction technique
    def create_resources(self):
        self.hand_node_translate = avango.gua.nodes.TransformNode(
            Name='hand_translate')
        self.hand_node_translate.Transform.value = avango.gua.make_identity_mat()

        loader = avango.gua.nodes.TriMeshLoader()
        self.hand_node = loader.create_geometry_from_file('hand_node',
                                                          'data/objects/hand.obj',
                                                          avango.gua.LoaderFlags.LOAD_MATERIALS)
        self.hand_node.Material.value.set_uniform('Roughness', 0.6)
        self.hand_node.Tags.value.append('invisible')
        self.hand_node_translate.Children.value.append(self.hand_node)

    # sets the correct inputs to be used for this interaction technique
    def set_inputs(self, scenegraph, head_node, controller_node, controller_sensor):
        # store references and add geometries to scenegraph
        self.scenegraph = scenegraph
        self.head_node = head_node
        self.controller_node = controller_node
        self.controller_sensor = controller_sensor
        self.controller_node.Children.value.append(self.hand_node_translate)
        self.sf_dragging_trigger.connect_from(self.controller_sensor.Button4)

        # create picker
        self.picker = Picker(self.scenegraph)
        self.always_evaluate(True)

    # called every frame because of self.always_evaluate(True)
    def evaluate(self):
        if self.enable_flag:
            self.apply_gogo(0.5)

            if self.dragging_object is not None:
                self.dragging_update()
            else:
                pick_result = self.compute_pick_result()
                self.update_highlights(pick_result)

    # updates the position of the virtual hand with respect to the GoGo mapping
    def apply_gogo(self, threshold):
        hand_pos = self.controller_node.WorldTransform.value.get_translate()
        head_pos = self.head_node.WorldTransform.value.get_translate()
        # YOUR CODE - BEGIN (Exercise 5.3 - GoGo)
        # ...
        # YOUR CODE - END (Exercise 5.3 - GoGo)

    # computes intersections of the hand with the scene
    def compute_pick_result(self):
        # YOUR CODE - BEGIN (Exercise 5.1 - Compute pick result)
        picker = Picker(self.scenegraph)
        position = self.hand_node_translate.WorldTransform.value.get_translate()
        direction = (self.hand_node_translate.WorldTransform.value * avango.gua.make_trans_mat(avango.gua.Vec3(0,0,-1))).get_translate() - self.hand_node_translate.WorldTransform.value.get_translate()
        direction.normalize()
        collide = picker.compute_all_pick_results(position,direction,0.3,[])
        if (len(collide) != 0):
            return collide[0]
        else:
            return None
        # YOUR CODE - END (Exercise 5.1 - Compute pick result)

    # updates the object highlights with respect to a pick result
    def update_highlights(self, pick_result):
        if pick_result is not None:
            if self.highlighted_object is not None and \
               pick_result.Object.value.Name.value != self.highlighted_object.Name.value:
                self.remove_highlight()
            self.highlight_object(pick_result.Object.value)
        else:
            self.remove_highlight()

    # highlights an object
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

    # called once when the dragging button is pressed
    def start_dragging(self):
        if self.highlighted_object is not None:
            # YOUR CODE - BEGIN (Exercise 5.2 - Object Dragging)
            self.dragging_object = self.highlighted_object
            self.prev_hand_pos = self.hand_node_translate.WorldTransform.value.get_translate()
            #temp = self.hand_node_translate
            #self.dragging_object.Transform.value = self.dragging_object.Transform.value *\
                                                    #avango.gua.make_trans_mat(self.hand_node_translate.Transform.value.get_translate()-self.dragging_object.Transform.value.get_translate())
            #* avango.gua.make_inverse_mat(self.controller_node.Transform.value) * avango.gua.make_inverse_mat(self.navigation_node.Transform.value)#(self.dragging_object.Transform.value.get_translate() - self.hand_node_translate.Transform.value.get_translate())
            #self.hand_node_translate.Children.value.append(self.dragging_object) 
            #self.dragging_object.Transform.value = self.hand_node_translate.WorldTransform.value *  self.dragging_object.Transform.value #*\
                                                    #avango.gua.make_scale_mat(self.dragging_object.Transform.value.get_scale())
            # YOUR CODE - END (Exercise 5.2 - Object Dragging)

    # called during every frame of a dragging operation
    def dragging_update(self):
        # YOUR CODE - BEGIN (Exercise 5.2 - Object Dragging)
        
        self.dragging_object.Transform.value = self.dragging_object.Transform.value *\
                                                avango.gua.make_trans_mat(self.hand_node_translate.WorldTransform.value.get_translate() - self.prev_hand_pos)         # YOUR CODE - END (Exercise 5.2 - Object Dragging)

        self.prev_hand_pos = self.hand_node_translate.WorldTransform.value.get_translate()
    # called once when the dragging button is released
    def stop_dragging(self):
        # YOUR CODE - BEGIN (Exercise 5.2 - Object Dragging)
        self.dragging_object = None
        pass
        # YOUR CODE - END (Exercise 5.2 - Object Dragging)

    # called whenever sf_dragging_trigger changes and calls start_dragging()
    # or stop_dragging() depending on the current button state
    @field_has_changed(sf_dragging_trigger)
    def sf_dragging_trigger_changed(self):
        if self.sf_dragging_trigger.value:
            self.start_dragging()
        else:
            self.stop_dragging()
