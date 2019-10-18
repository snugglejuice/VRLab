#!/usr/bin/python3

# import avango-guacamole libraries
import avango
import avango.daemon
import avango.gua
import avango.script

# import python libraries
import time

# class realizing a keyboard and mouse navigation on a desktop setup
class DesktopNavigation(avango.script.Script):

    # input fields
    sf_input_key_w = avango.SFBool()
    sf_input_key_w.value = False

    sf_input_key_a = avango.SFBool()
    sf_input_key_a.value = False

    sf_input_key_s = avango.SFBool()
    sf_input_key_s.value = False

    sf_input_key_d = avango.SFBool()
    sf_input_key_d.value = False

    sf_input_mouse_x = avango.SFFloat()
    sf_input_mouse_x.value = 0.0

    sf_input_mouse_y = avango.SFFloat()
    sf_input_mouse_y.value = 0.0

    # output field
    sf_output_matrix = avango.gua.SFMatrix4()
    sf_output_matrix.value = avango.gua.make_identity_mat()

    def __init__(self):
        self.super(DesktopNavigation).__init__()

        self.__connect_input_sensors()

        self.rotation_speed = 7.0
        self.motion_speed = 7.0

        self.__rot_x = 0.0
        self.__rot_y = 0.0
        self.__location = avango.gua.Vec3(0.0, 2.0, 10.0)
        self.__lf_time = time.time()

        self.always_evaluate(True)

    # establishes the connection to the devices registered in the daemon
    def __connect_input_sensors(self):
        self.device_service = avango.daemon.DeviceService()
        self.keyboard_sensor = avango.daemon.nodes.DeviceSensor(
            DeviceService=self.device_service)
        self.keyboard_sensor.Station.value = 'gua-device-keyboard'
        self.sf_input_key_w.connect_from(self.keyboard_sensor.Button0)
        self.sf_input_key_a.connect_from(self.keyboard_sensor.Button1)
        self.sf_input_key_s.connect_from(self.keyboard_sensor.Button2)
        self.sf_input_key_d.connect_from(self.keyboard_sensor.Button3)

        self.mouse_sensor = avango.daemon.nodes.DeviceSensor(
            DeviceService=self.device_service)
        self.mouse_sensor.Station.value = 'gua-device-mouse'
        self.sf_input_mouse_x.connect_from(self.mouse_sensor.Value0)
        self.sf_input_mouse_y.connect_from(self.mouse_sensor.Value1)

    # called every frame because of self.always_evaluate(True)
    # updates sf_output_matrix by processing the keyboard's and mouse's inputs
    def evaluate(self):
        now = time.time()
        elapsed = now - self.__lf_time

        self.__rot_x -= self.sf_input_mouse_y.value * elapsed
        self.__rot_y -= self.sf_input_mouse_x.value * elapsed

        rot_mat = avango.gua.make_rot_mat(self.__rot_y * self.rotation_speed, 0, 1, 0) *\
            avango.gua.make_rot_mat(
                self.__rot_x * self.rotation_speed, 1, 0, 0)

        if self.sf_input_key_w.value:
            self.__location += (rot_mat * avango.gua.make_trans_mat(0.0,
                                                                    0.0, -self.motion_speed * elapsed)).get_translate()

        if self.sf_input_key_s.value:
            self.__location += (rot_mat * avango.gua.make_trans_mat(0.0,
                                                                    0.0, self.motion_speed * elapsed)).get_translate()

        if self.sf_input_key_a.value:
            self.__location += (rot_mat * avango.gua.make_trans_mat(-self.motion_speed *
                                                                    elapsed, 0.0, 0.0)).get_translate()

        if self.sf_input_key_d.value:
            self.__location += (rot_mat * avango.gua.make_trans_mat(
                self.motion_speed * elapsed, 0.0, 0.0)).get_translate()

        smoothness = elapsed * 10.0
        start_mat = avango.gua.make_trans_mat(self.sf_output_matrix.value.get_translate()) * \
            avango.gua.make_rot_mat(
                self.sf_output_matrix.value.get_rotate_scale_corrected())
        target_mat = avango.gua.make_trans_mat(self.__location) * rot_mat

        self.sf_output_matrix.value = start_mat * \
            (1.0 - smoothness) + target_mat * smoothness
        self.__lf_time = now
