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

from lib.Picker import *

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
    falltime = 0
    def evaluate(self):
        now = time.time()
        elapsed = now - self.lf_time
        self.lf_time = now

        # 4.3
        trans_y = 0
        picker = Picker(self.scenegraph)
        result = picker.compute_pick_result(self.scenegraph['/navigation_node'].Transform.value.get_translate(),avango.gua.Vec3(0.0, -1.0, 0.0),100,[])
        if (result != None):
            if ('/sphere_' not in result.Object.value.Name.value):
                trans_y = 2-result.Distance.value
                if (trans_y < 0):
                    self.falltime += 1;
                    trans_y = -0.000001*self.falltime
                else:
                    self.falltime = 0


        # 4.1
        x_offset = self.sf_input_x.value*0.00001
        z_offset = self.sf_input_z.value*0.00001
        ry_offset = self.sf_input_ry.value*0.0001
        rx_offset = self.sf_input_rx.value*0.05
        # 4.4 
        direction = avango.gua.Vec3(x_offset,0,z_offset)
        #exp_pos = self.sf_output_matrix.value * \
        #                        avango.gua.make_trans_mat(x_offset,trans_y,z_offset)
        #direction = self.scenegraph['/navigation_node'].Transform.value.get_translate() - exp_pos.get_translate()
        collision = picker.compute_pick_result(self.scenegraph['/navigation_node'].Transform.value.get_translate(),direction,10,[])
        #print(direction)
        #print(collision)
        if (collision != None):
            if (collision.Object != None):
                if ('/sphere_' in collision.Object.value.Name.value):
                    print("col")
                else:
                    x_offset = -x_offset
                    z_offset = -z_offset
        #    pass
        #else:
        #    x_offset = 0
        #    z_offset = 0
        self.sf_output_matrix.value = self.sf_output_matrix.value * \
                            avango.gua.make_trans_mat(x_offset,trans_y,z_offset) * \
                            avango.gua.make_rot_mat(ry_offset,0,1,0)
        # 4.2 rot
        self.scenegraph['/navigation_node/avatar/camera_rot'].Transform.value = avango.gua.make_rot_mat(rx_offset,1,0,0)
        #self.check_targets()

    # 4.5
    def check_targets(self):
        obj_list = []
        i = 0
        while (True): 
            if (self.scenegraph['/sphere_'+str(i)] in self.scenegraph.Root.value.Children.value):
                obj_list.append(self.scenegraph['/sphere_'+str(i)])
            else:
                break
            i+=1
        #print(obj_list)



        
        

