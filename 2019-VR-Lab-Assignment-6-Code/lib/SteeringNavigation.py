#!/usr/bin/python3

# import avango-guacamole libraries
import avango
import avango.daemon
import avango.gua
import avango.script
from avango.script import field_has_changed

# import python libraries
import math
import time


# class realizing a steering navigation technique
class SteeringNavigation(avango.script.Script):

    # input fields
    sf_controller_matrix = avango.gua.SFMatrix4()
    sf_controller_matrix.value = avango.gua.make_identity_mat()

    sf_rocker = avango.SFFloat()
    sf_rocker.value = 0.0

    sf_grip_button = avango.SFBool()
    sf_grip_button.value = False

    # output field
    sf_navigation_matrix = avango.gua.SFMatrix4()
    sf_navigation_matrix.value = avango.gua.make_identity_mat()

    def __init__(self):
        self.super(SteeringNavigation).__init__()
        self.steering_mode = 'pointing-directed'
        self.center_circle_diameter = 0.5  # m
        self.maximum_speed = 5.0  # m/s
        self.head_node = None
        self.lf_time = time.time()

    # sets the inputs to be used for navigation
    def set_inputs(self, scenegraph, navigation_node, head_node, controller_node, controller_sensor):
        self.scenegraph = scenegraph
        self.navigation_node = navigation_node
        self.head_node = head_node
        self.controller_node = controller_node
        self.controller_sensor = controller_sensor
        self.build_center_circle()
        self.sf_controller_matrix.connect_from(self.controller_node.Transform)
        self.sf_rocker.connect_from(self.controller_sensor.Value3)
        self.sf_grip_button.connect_from(self.controller_sensor.Button2)

    # builds the center circle for position-directed steering
    def build_center_circle(self):
        loader = avango.gua.nodes.TriMeshLoader()
        self.center_circle = loader.create_geometry_from_file(
            'center-circle', 'data/objects/circle.obj', avango.gua.LoaderFlags.DEFAULTS)
        self.set_center_circle_pos(0.0, 0.0)
        self.center_circle.Material.value.set_uniform(
            'Color', avango.gua.Vec4(0.2, 0.5, 0.65, 1.0))
        self.center_circle.Material.value.set_uniform('Roughness', 0.8)
        self.center_circle.Tags.value.append('invisible')
        self.navigation_node.Children.value.append(self.center_circle)

    # sets the center circle to a given position in the xz plane
    def set_center_circle_pos(self, x, z):
        self.center_circle.Transform.value = avango.gua.make_trans_mat(x, 0.001, z) * \
            avango.gua.make_rot_mat(-90, 1, 0, 0) * \
            avango.gua.make_scale_mat(self.center_circle_diameter)

    # enables or disables the navigation technique
    def enable(self, boolean):
        if boolean:
            self.sf_navigation_matrix.value = self.navigation_node.Transform.value
            self.navigation_node.Transform.disconnect()
            self.navigation_node.Transform.connect_from(
                self.sf_navigation_matrix)
            user_pos = self.head_node.Transform.value.get_translate()
            self.set_center_circle_pos(user_pos.x, user_pos.z)
        else:
            self.center_circle.Tags.value.append('invisible')
        self.always_evaluate(boolean)

    # switches between pointing-directed and position-directed movement mode
    def set_steering_mode(self, mode):
        if mode == 'pointing-directed':
            self.steering_mode = 'pointing-directed'
            self.center_circle.Tags.value.append('invisible')
        elif mode == 'position-directed':
            self.steering_mode = 'position-directed'
            self.center_circle.Tags.value.remove('invisible')

    # called every frame because of self.always_evaluate(True)
    # updates sf_navigation_matrix by processing the inputs
    def evaluate(self):
        now = time.time()
        elapsed = now - self.lf_time

        if self.steering_mode == 'pointing-directed':
            movement_vector = self.apply_pointing_directed_steering(elapsed)
        elif self.steering_mode == 'position-directed':
            movement_vector = self.apply_position_directed_steering(elapsed)

        # apply movement vector
        self.sf_navigation_matrix.value *= avango.gua.make_trans_mat(
            movement_vector)
        self.lf_time = now

    # applies pointing-directed steering movements
    def apply_pointing_directed_steering(self, delta_time):
        # compute movement vector
        speed = self.sf_rocker.value * self.maximum_speed * delta_time
        forward_matrix = self.controller_node.WorldTransform.value * \
            avango.gua.make_trans_mat(0.0, 0.0, -1.0)
        forward_vector = forward_matrix.get_translate() - \
            self.controller_node.WorldTransform.value.get_translate()
        forward_vector.normalize()
        movement_vector = forward_vector * speed

        # restrict movements to ground plane
        movement_vector.y = 0.0
        return movement_vector

    # applies position-directed steering movements
    def apply_position_directed_steering(self, delta_time):
        # YOUR CODE - BEGIN (Exercise 6.1 - Position-Based Steering)
        if self.steering_mode == 'position-directed':
            self.center_circle.Tags.value.remove('invisible')
            movement_vector = self.head_node.WorldTransform.value.get_translate() - self.center_circle.WorldTransform.value.get_translate()
            print(movement_vector)
            if ((movement_vector.x ** 2 + movement_vector.z ** 2) > (self.center_circle_diameter/2)**2):
                return avango.gua.Vec3(delta_time * (movement_vector.x - self.center_circle_diameter/2),0,delta_time*(movement_vector.z - self.center_circle_diameter/2))
            else:
                return avango.gua.Vec3(0.0, 0.0, 0.0)
        else:
            self.center_circle.Tags.value.append('invisible')
        return avango.gua.Vec3(0.0, 0.0, 0.0)
        # YOUR CODE - END (Exercise 6.1 - Position-Based Steering)

    # called whenever sf_grip_button changes
    @field_has_changed(sf_grip_button)
    def sf_grip_button_changed(self):
        if self.sf_grip_button.value and self.head_node is not None:
            user_pos = self.head_node.Transform.value.get_translate()
            self.set_center_circle_pos(user_pos.x, user_pos.z)
