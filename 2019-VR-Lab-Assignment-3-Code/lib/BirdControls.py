#!/usr/bin/python3

# import avango-guacamole libraries
import avango
import avango.daemon
import avango.gua
from avango.script import field_has_changed

# import python libraries
import math
import time

# implement control mechanisms for the bird
class BirdControls(avango.script.Script):

    # input fields
    sf_mouse_x = avango.SFFloat()
    sf_mouse_x.value = 0.0

    sf_mouse_y = avango.SFFloat()
    sf_mouse_y.value = 0.0

    sf_mouse_click = avango.SFBool()
    sf_mouse_click.value = False

    sf_space_navigator_x = avango.SFFloat()
    sf_space_navigator_x.value = 0.0

    sf_space_navigator_y = avango.SFFloat()
    sf_space_navigator_y.value = 0.0

    sf_one_key = avango.SFBool()
    sf_one_key.value = False

    sf_two_key = avango.SFBool()
    sf_two_key.value = False

    sf_three_key = avango.SFBool()
    sf_three_key.value = False

    sf_four_key = avango.SFBool()
    sf_four_key.value = False

    sf_five_key = avango.SFBool()
    sf_five_key.value = False

    sf_six_key = avango.SFBool()
    sf_six_key.value = False

    sf_seven_key = avango.SFBool()
    sf_seven_key.value = False

    def __init__(self):
        self.super(BirdControls).__init__()
        self.current_technique = 1

    # sets the bird transform node to be controlled
    def set_bird_transform_node(self, bird_node, target_spheres):
        self.bird_node = bird_node
        self.bird_start_mat = bird_node.Transform.value
        self.target_spheres = target_spheres

        self.connect_input_sensors()
        self.create_cursor()
        self.reset()
        self.always_evaluate(True)

    # restores the initial state of objects
    def reset(self):
        self.move_start_time = None
        self.bird_node.Transform.value = self.bird_start_mat
        self.cursor_transform.Transform.value = self.bird_start_mat
        self.velocity = avango.gua.Vec2(0.0, 0.0)
        self.acceleration = avango.gua.Vec2(0.0, 0.0)
        for target_sphere in self.target_spheres:
            target_sphere.Tags.value.remove('invisible')
        self.num_targets_visible = len(self.target_spheres)
        if self.current_technique == 7:
            self.cursor.Tags.value.remove('invisible')
        elif 'invisible' not in self.cursor.Tags.value:
            self.cursor.Tags.value.append('invisible')

    # creates and connects the input sensors to the respective fields
    def connect_input_sensors(self):
        self.device_service = avango.daemon.DeviceService()

        # mouse
        self.mouse_sensor = avango.daemon.nodes.DeviceSensor(
            DeviceService=self.device_service)
        self.mouse_sensor.Station.value = 'gua-device-mouse'
        self.sf_mouse_x.connect_from(self.mouse_sensor.Value0)
        self.sf_mouse_y.connect_from(self.mouse_sensor.Value1)
        self.sf_mouse_click.connect_from(self.mouse_sensor.Button0)

        # space navigator
        self.space_navigator_sensor = avango.daemon.nodes.DeviceSensor(
            DeviceService=self.device_service)
        self.space_navigator_sensor.Station.value = 'gua-device-space'
        self.sf_space_navigator_x.connect_from(
            self.space_navigator_sensor.Value0)
        self.sf_space_navigator_y.connect_from(
            self.space_navigator_sensor.Value1)

        # keyboard
        self.keyboard_sensor = avango.daemon.nodes.DeviceSensor(
            DeviceService=self.device_service)
        self.keyboard_sensor.Station.value = 'gua-device-keyboard'
        self.sf_one_key.connect_from(self.keyboard_sensor.Button1)
        self.sf_two_key.connect_from(self.keyboard_sensor.Button2)
        self.sf_three_key.connect_from(self.keyboard_sensor.Button3)
        self.sf_four_key.connect_from(self.keyboard_sensor.Button4)
        self.sf_five_key.connect_from(self.keyboard_sensor.Button5)
        self.sf_six_key.connect_from(self.keyboard_sensor.Button6)
        self.sf_seven_key.connect_from(self.keyboard_sensor.Button7)

    # creates a cursor in the scene for selection
    def create_cursor(self):
        self.cursor_transform = avango.gua.nodes.TransformNode(
            Name='cursor_transform')
        self.bird_node.Parent.value.Children.value.append(
            self.cursor_transform)

        loader = avango.gua.nodes.TriMeshLoader()
        self.cursor = loader.create_geometry_from_file('cursor',
                                                       'data/objects/sphere.obj',
                                                       avango.gua.LoaderFlags.DEFAULTS)
        self.cursor.Material.value.set_uniform(
            'Color', avango.gua.Vec4(1.0, 0.0, 0.0, 1.0))
        self.cursor.Material.value.set_uniform('Emissivity', 1.0)
        self.cursor.Transform.value = avango.gua.make_scale_mat(0.2)
        self.cursor_transform.Children.value.append(self.cursor)

        self.animation_start_pos = None
        self.animation_target_pos = None
        self.animation_start_time = None
        self.animation_speed = 10.0  # m/s

    # called every frame because of self.always_evaluate(True)
    def evaluate(self):
        isotonic_x_input = self.sf_mouse_x.value
        isotonic_y_input = self.sf_mouse_y.value
        elastic_x_input = self.sf_space_navigator_x.value
        elastic_y_input = self.sf_space_navigator_y.value

        # start timer on first movement
        start_timer = False
        if self.move_start_time is None:
            if self.current_technique <= 3 or self.current_technique == 7:
                if isotonic_x_input != 0.0 or isotonic_y_input != 0.0:
                    start_timer = True
            else:
                if elastic_x_input != 0.0 or elastic_y_input != 0.0:
                    start_timer = True

        if start_timer:
            self.move_start_time = time.time()
            print("Timer Started")

        # map the input with respect to the current transfer function
        if self.current_technique == 1:
            self.apply_isotonic_position_control_mapping(
                isotonic_x_input, isotonic_y_input)
        elif self.current_technique == 2:
            self.apply_isotonic_rate_control_mapping(
                isotonic_x_input, isotonic_y_input)
        elif self.current_technique == 3:
            self.apply_isotonic_acceleration_control_mapping(
                isotonic_x_input, isotonic_y_input)
        elif self.current_technique == 4:
            self.apply_elastic_position_control_mapping(
                elastic_x_input, elastic_y_input)
        elif self.current_technique == 5:
            self.apply_elastic_rate_control_mapping(
                elastic_x_input, elastic_y_input)
        elif self.current_technique == 6:
            self.apply_elastic_acceleration_control_mapping(
                elastic_x_input, elastic_y_input)
        elif self.current_technique == 7:
            self.apply_cursor_movement(isotonic_x_input, isotonic_y_input)
            self.animate_bird()

        # adjust bird matrix and check for target collisions
        self.wrap_matrix(self.bird_node)
        self.wrap_matrix(self.cursor_transform)
        self.check_targets()

    # moves the bird using a position-control transfer function on the mouse input
    def apply_isotonic_position_control_mapping(self, x_input, y_input):
        x_offset = x_input * 0.01
        y_offset = -y_input * 0.01
        self.bird_node.Transform.value = self.bird_node.Transform.value * \
            avango.gua.make_trans_mat(x_offset, y_offset, 0.0)

    # moves the bird using a rate-control transfer function on the mouse input
    def apply_isotonic_rate_control_mapping(self, x_input, y_input):
        # YOUR CODE - BEGIN (Exercise 3.1 - Isotonic Rate-Control)
        #pass
        x_offset = x_input * 0.00002
        y_offset = -y_input * 0.00002
        self.velocity = self.velocity + avango.gua.Vec2(x_offset,y_offset)
        self.bird_node.Transform.value = self.bird_node.Transform.value * \
            avango.gua.make_trans_mat(self.velocity.x, self.velocity.y, 0.0)
        #self.bird_node.Transform.value = ...
        # YOUR_CODE - END (Exercise 3.1 - Isotonic Rate-Control)

    # moves the bird using an acceleration-control transfer function on the mouse input
    def apply_isotonic_acceleration_control_mapping(self, x_input, y_input):
        # YOUR CODE - BEGIN (Exercise 3.2 - Isotonic Acceleration-Control)
        x_offset = x_input * 0.00000005
        y_offset = -y_input * 0.0000005
        self.acceleration = self.acceleration + avango.gua.Vec2(x_offset,y_offset)
        self.velocity = self.velocity + self.acceleration
        self.bird_node.Transform.value = self.bird_node.Transform.value * \
            avango.gua.make_trans_mat(self.velocity.x, self.velocity.y, 0.0)
        # self.bird_node.Transform.value = ...
        # YOUR_CODE - END (Exercise 3.2 - Isotonic Acceleration-Control)

    # moves the bird using a position-control transfer function on the space navigator input
    def apply_elastic_position_control_mapping(self, x_input, y_input):
        # YOUR CODE - BEGIN (Exercise 3.3 - Elastic Position-Control)
        x_offset = x_input * 0.0001
        y_offset = -y_input * 0.0001
        self.bird_node.Transform.value = self.bird_node.Transform.value * \
            avango.gua.make_trans_mat(x_offset, y_offset, 0.0)
        # self.bird_node.Transform.value = ...
        # YOUR_CODE - END (Exercise 3.3 - Elastic Position-Control)

    # moves the bird using a rate-control transfer function on the space navigator input
    def apply_elastic_rate_control_mapping(self, x_input, y_input):
        # YOUR CODE - BEGIN (Exercise 3.4 - Elastic Rate-Control)
        x_offset = x_input * 0.000001
        y_offset = -y_input * 0.000001
        self.velocity = self.velocity + avango.gua.Vec2(x_offset,y_offset)
        self.bird_node.Transform.value = self.bird_node.Transform.value * \
            avango.gua.make_trans_mat(self.velocity.x, self.velocity.y, 0.0)
        # self.bird_node.Transform.value = ...
        # YOUR_CODE - END (Exercise 3.4 - Elastic Rate-Control)

    # moves the bird using an acceleration-control transfer function on the space navigator input
    def apply_elastic_acceleration_control_mapping(self, x_input, y_input):
        # YOUR CODE - BEGIN (Exercise 3.5 - Elastic Acceleration-Control)
        x_offset = x_input  * 0.0000000000005
        y_offset = -y_input * 0.0000000000005
        self.acceleration = self.acceleration + avango.gua.Vec2(x_offset,y_offset)
        self.velocity = self.velocity + self.acceleration
        self.bird_node.Transform.value = self.bird_node.Transform.value * \
            avango.gua.make_trans_mat(self.velocity.x, self.velocity.y, 0.0)
        # self.bird_node.Transform.value = ...
        # YOUR_CODE - END (Exercise 3.5 - Elastic Acceleration-Control)

    # maps the mouse input to the movement of the virtual cursor
    def apply_cursor_movement(self, x_input, y_input):
        x_offset = x_input * 0.03
        y_offset = -y_input * 0.03
        self.cursor_transform.Transform.value = self.cursor_transform.Transform.value * \
            avango.gua.make_trans_mat(x_offset, y_offset, 0.0)

    # called whenever sf_mouse_click changes
    @field_has_changed(sf_mouse_click)
    def sf_mouse_click_changed(self):
        if self.sf_mouse_click.value and self.current_technique == 7:
            start = self.bird_node.Transform.value.get_translate()
            target = self.cursor_transform.Transform.value.get_translate()

            if start.x != target.x or start.y != target.y:
                self.animation_start_pos = start
                self.animation_target_pos = target
                self.animation_start_time = time.time()

    # animates the bird to a specified target position
    def animate_bird(self):
        if self.animation_start_time is not None:
            # YOUR CODE - BEGIN (Exercises 3.6 and 3.7 - Animation)
            speed = 10
            distance_x = self.animation_target_pos.x - self.animation_start_pos.x
            distance_y = self.animation_target_pos.y - self.animation_start_pos.y
            distance_to_travel = (self.animation_target_pos - self.animation_start_pos)
            distance = (math.sqrt(distance_x**2 + distance_y**2))
            expected_time =  (distance/speed)
            t = time.time()-self.animation_start_time
            fraction = t/expected_time
            fraction = 3*(fraction**2)-2*(fraction**3)
            self.bird_node.Transform.value = avango.gua.make_trans_mat(self.animation_start_pos.x + fraction * distance_x, self.animation_start_pos.y + fraction * distance_y, self.bird_node.Transform.value.get_translate().z)
            if (fraction >= 0.99):
                self.bird_node.Transform.value = avango.gua.make_trans_mat(self.animation_target_pos.x, self.animation_target_pos.y, self.bird_node.Transform.value.get_translate().z)
                self.animation_target_pos = None
                self.animation_start_time = None
                self.animation_start_pos = None
            # YOUR_CODE - END (Exercises 3.6 and 3.7 - Animation)

    # makes the bird appear on the other screen side when exiting the field of view
    def wrap_matrix(self, node):
        pos = node.Transform.value.get_translate()
        new_pos = avango.gua.Vec3(pos)

        if pos.x > 12.5:
            new_pos.x = -12.5
        elif pos.x < -12.5:
            new_pos.x = 12.5

        if pos.y > 31.0:
            new_pos.y = 31.0
        elif pos.y < 19.0:
            new_pos.y = 19.0

        node.Transform.value = avango.gua.make_trans_mat(new_pos)

    # checks for collisions of the bird with the target spheres
    def check_targets(self):
        for target_sphere in self.target_spheres:
            if 'invisible' not in target_sphere.Tags.value:
                sphere_pos = target_sphere.Transform.value.get_translate()
                sphere_pos = avango.gua.Vec2(sphere_pos.x, sphere_pos.y)
                bird_pos = self.bird_node.Transform.value.get_translate()
                bird_pos = avango.gua.Vec2(bird_pos.x, bird_pos.y)
                pos_difference = bird_pos - sphere_pos
                distance = math.sqrt(pos_difference.x * pos_difference.x +
                                     pos_difference.y * pos_difference.y)
                if distance < 0.5:
                    target_sphere.Tags.value.append('invisible')
                    self.num_targets_visible -= 1

                    if self.num_targets_visible == 0:
                        elapsed = round(time.time()-self.move_start_time, 2)
                        print("Total Time: " + str(elapsed) + " s")

    # called whenever sf_one_key changes
    @field_has_changed(sf_one_key)
    def sf_one_key_changed(self):
        if self.sf_one_key.value:
            self.current_technique = 1
            self.reset()
            print("Isotonic Position-Control Mapping activated")

    # called whenever sf_two_key changes
    @field_has_changed(sf_two_key)
    def sf_two_key_changed(self):
        if self.sf_two_key.value:
            self.current_technique = 2
            self.reset()
            print("Isotonic Rate-Control Mapping activated")

    # called whenever sf_three_key changes
    @field_has_changed(sf_three_key)
    def sf_three_key_changed(self):
        if self.sf_three_key.value:
            self.current_technique = 3
            self.reset()
            print("Isotonic Acceleration-Control Mapping activated")

    # called whenever sf_four_key changes
    @field_has_changed(sf_four_key)
    def sf_four_key_changed(self):
        if self.sf_four_key.value:
            self.current_technique = 4
            self.reset()
            print("Elastic Position-Control Mapping activated")

    # called whenever sf_five_key changes
    @field_has_changed(sf_five_key)
    def sf_five_key_changed(self):
        if self.sf_five_key.value:
            self.current_technique = 5
            self.reset()
            print("Elastic Rate-Control Mapping activated")

    # called whenever sf_six_key changes
    @field_has_changed(sf_six_key)
    def sf_six_key_changed(self):
        if self.sf_six_key.value:
            self.current_technique = 6
            self.reset()
            print("Elastic Acceleration-Control Mapping activated")

    # called whenever sf_seven_key changes
    @field_has_changed(sf_seven_key)
    def sf_seven_key_changed(self):
        if self.sf_seven_key.value:
            self.current_technique = 7
            self.reset()
            print("Target-Based Controls activated")
