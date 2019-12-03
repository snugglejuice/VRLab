#!/usr/bin/python3

# import avango-guacamole libraries
import avango
import avango.daemon
import avango.gua
import avango.script

# import python libraries
import math
import random
import statistics
import time

# class realizing a spacemouse navigation on a desktop setup
class NavigationControls(avango.script.Script):

    # input fields
    sf_input_x = avango.SFFloat()
    sf_input_x.value = 0.0

    sf_input_y = avango.SFFloat()
    sf_input_y.value = 0.0

    sf_input_z = avango.SFFloat()
    sf_input_z.value = 0.0

    sf_input_rx = avango.SFFloat()
    sf_input_rx.value = 0.0

    sf_input_ry = avango.SFFloat()
    sf_input_ry.value = 0.0

    sf_input_rz = avango.SFFloat()
    sf_input_rz.value = 0.0

    # output matrix for the figure
    sf_output_matrix = avango.gua.SFMatrix4()
    sf_output_matrix.value = avango.gua.make_identity_mat()

    def __init__(self):
        self.super(NavigationControls).__init__()
        self.scenegraph = None
        self.static_user_height = 2.0
        self.lf_time = time.time()
        self.connect_input_sensors()

    # establishes the connection to the devices registered in the daemon
    def connect_input_sensors(self):
        self.device_service = avango.daemon.DeviceService()
        self.space_navigator_sensor = avango.daemon.nodes.DeviceSensor(
            DeviceService=self.device_service)
        self.space_navigator_sensor.Station.value = 'gua-device-space'
        self.sf_input_x.connect_from(
            self.space_navigator_sensor.Value0)
        self.sf_input_y.connect_from(
            self.space_navigator_sensor.Value2)
        self.sf_input_z.connect_from(
            self.space_navigator_sensor.Value1)
        self.sf_input_rx.connect_from(
            self.space_navigator_sensor.Value3)
        self.sf_input_ry.connect_from(
            self.space_navigator_sensor.Value4)
        self.sf_input_rz.connect_from(
            self.space_navigator_sensor.Value5)

    # sets the scenegraph used for ground following
    def set_scenegraph(self, scenegraph):
        self.scenegraph = scenegraph
        self.always_evaluate(True)

    # called every frame because of self.always_evaluate(True)
    # updates sf_output_matrix by processing the inputs
    def evaluate(self):
        now = time.time()
        elapsed = now - self.lf_time
        self.lf_time = now
        self.sf_output_matrix.value = self.sf_output_matrix.value * \
                                avango.gua.make_trans_mat(self.sf_input_x.value*0.001,0.0,self.sf_input_z.value*0.001)
