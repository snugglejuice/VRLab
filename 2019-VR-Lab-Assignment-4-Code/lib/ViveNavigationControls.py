#!/usr/bin/python3

# import avango-guacamole libraries
import avango
import avango.daemon
import avango.gua
import avango.script

# import python libraries
import time
import math

# class realizing a navigation on a vive setup
class ViveNavigationControls(avango.script.Script):

    # output field
    sf_output_matrix = avango.gua.SFMatrix4()
    sf_output_matrix.value = avango.gua.make_identity_mat()

    def __init__(self):
        self.super(ViveNavigationControls).__init__()
        self.lf_time = time.time()

    # sets the controller nodes to be used for navigation
    def set_nodes(self, scenegraph, navigation_node, head_node, controller1_sensor, controller1_node):
        self.scenegraph = scenegraph
        self.navigation_node = navigation_node
        self.sf_output_matrix.value = self.navigation_node.Transform.value
        self.head_node = head_node
        self.controller1_sensor = controller1_sensor
        self.controller1_node = controller1_node
        self.always_evaluate(True)

    # called every frame because of self.always_evaluate(True)
    # updates sf_output_matrix by processing the inputs
    def evaluate(self):
        now = time.time()
        elapsed = now - self.lf_time
        rocker_value = self.controller1_sensor.Value3.value
        self.lf_time = now

        disp = self.controller1_node.WorldTransform.value.get_translate() - self.navigation_node.WorldTransform.value.get_translate()
        rot = self.controller1_node.Transform.value.get_rotate()
        print(rot)
        #4.7
        if(rocker_value != 0):
            disp = self.controller1_node.WorldTransform.value.get_translate() - self.navigation_node.WorldTransform.value.get_translate()
            #disp = math.sqrt(direction.x**2+direction.y**2+direction.z**2)
            #direction = self.controller1_node.WorldTransform.value * self.navigation_node.WorldTransform.value
            #disp = direction.get_translate()
            rot = self.controller1_node.Transform.value.get_rotate()
            angle = math.atan(rot.x/rot.z)
            print("rot :", rot)
            #print(rot)
            #angle = math.acos(rot.w)*2
            #direction = avango.gua.Vec3(direction.x,0,direction.z) - self.navigation_node.Transform.value.get_translate()
            #input_rotation = self.controller1_node.Transform.value.get_rotate_scale_corrected()
            #head_rotation = self.head_node.Transform.value.get_rotate_scale_corrected()
            #print(direction)
            #new_pos = self.controller1_node.Transform.value.get_translate()
            #print("input rotation :", input_rotation)
            
            if ((angle >= 0) & (angle < math.pi/2)):
                print("case 1")
                self.sf_output_matrix.value = self.sf_output_matrix.value *\
                                            avango.gua.make_trans_mat(disp.x*0.001,0,disp.z*0.001)
            elif ((angle >= math.pi/2) & (angle < math.pi)):
                print("case 2")
                self.sf_output_matrix.value = self.sf_output_matrix.value *\
                                            avango.gua.make_trans_mat(disp.x*0.001,0,-disp.z*0.001)
            elif ((angle > math.pi) & (angle <= -math.pi/2)):
                print("case 3")
                self.sf_output_matrix.value = self.sf_output_matrix.value *\
                                            avango.gua.make_trans_mat(-disp.x*0.001,0,-disp.z*0.001)
            elif ((angle > -math.pi/2) & (angle <= 0)):
                print("case 4")
                self.sf_output_matrix.value = self.sf_output_matrix.value *\
                                            avango.gua.make_trans_mat(-disp.x*0.001,0,disp.z*0.001)

        #4.8
        """  position = self.head_node.Transform.value.get_translate()
        trans_y = 0
        height_figure = 2
        picker = Picker(self.scenegraph)
        result = picker.compute_pick_result(position,avango.gua.Vec3(0.0, -1.0, 0.0),10,['collectable'])
        
        if (result != None):
            if (round(result.Distance.value,3) < height_figure):
                trans_y += 0.01
                self.falltime = 0
            elif (round(result.Distance.value,3) > height_figure):
                self.falltime += 1
                trans_y -= 0.00001*self.falltime
            else:
                self.falltime = 0"""
