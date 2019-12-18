#!/usr/bin/python3

# import avango-guacamole libraries
import avango
import avango.daemon
import avango.gua
import avango.script

# import python libraries
import time
import math
from lib.Picker import *

# class realizing a navigation on a vive setup
class ViveNavigationControls(avango.script.Script):

    # output field
    sf_output_matrix = avango.gua.SFMatrix4()
    sf_output_matrix.value = avango.gua.make_identity_mat()
    #output matrix for the ball
    sf_animation_mat = avango.gua.SFMatrix4()
    sf_animation_mat.value = avango.gua.make_identity_mat()

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

    def set_pickable_object(self, pickable_object_list):
        self.pickable_object_list = pickable_object_list
        self.pickable_object_list[2].Transform.connect_from(self.sf_animation_mat)


    # called every frame because of self.always_evaluate(True)
    # updates sf_output_matrix by processing the inputs
    falltime = 0
    collected = 0
    def evaluate(self):
        now = time.time()
        elapsed = now - self.lf_time
        rocker_value = self.controller1_sensor.Value3.value
        self.lf_time = now
        self.initial_time = self.lf_time
        self.gazedirected = False
        #4.8
        position = self.head_node.WorldTransform.value.get_translate()
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
                self.falltime = 0

        #4.7
        if(rocker_value == 1):
            disp = self.controller1_node.WorldTransform.value.get_translate() - self.head_node.WorldTransform.value.get_translate()   
        
            direction = disp
            direction.normalize()
        
            distance = (math.sqrt(direction.x**2+direction.y**2+direction.z**2))
            collide = picker.compute_pick_result(position,direction,10,['invisible'])
                   
            if (collide != None):
                if (collide.Distance.value < distance):
                    if (collide.Object.value in self.pickable_object_list):
                        print("collision pickable object")
                        collide.Object.value.Tags.value.append('invisible')
                        self.collected += 1
                        if (self.collected == len(self.pickable_object_list)):
                            print("Task completed in: ", now - self.initial_time, "seconds")
                    disp.x = 0
                    disp.z = 0  

            self.sf_output_matrix.value = self.sf_output_matrix.value * avango.gua.make_trans_mat(disp.x*0.01,trans_y,disp.z*0.01)
        else:
            #4.9
            
            #print(disp)
            #angle =  self.head_node.WorldTransform.value.get_rotate().y,0,1,0
            #print(self.head_node.WorldTransform.value.get_rotate())
            distance = 0.001#(math.sqrt(direction.x**2+direction.y**2+direction.z**2))
            angle = 2*math.acos(self.head_node.WorldTransform.value.get_rotate().w)
            x = math.sin(angle)*distance
            z = math.cos(angle)*distance
            if((x >= 0) & (z >= 0)):
                print("Q1")
                disp = avango.gua.Vec3(-x,0,-z)
            if((x >= 0) & (z < 0)):
                print("Q2")
                disp = avango.gua.Vec3(x,0,-z)
            if((x < 0) & (z >= 0)):
                print("Q3")
                disp = avango.gua.Vec3(x,0,z)
            if((x < 0) & (z < 0)):
                print("Q4")
                disp = avango.gua.Vec3(-x,0,-z)
            #Sprint(angle)
            print("disp",disp)
            direction = disp
            collide = picker.compute_pick_result(position,direction,10,['invisible'])
                   
            if (collide != None):
                if (collide.Distance.value < distance):
                    if (collide.Object.value in self.pickable_object_list):
                        print("collision pickable object")
                        collide.Object.value.Tags.value.append('invisible')
                        self.collected += 1
                        if (self.collected == len(self.pickable_object_list)):
                            print("Task completed in: ", now - self.initial_time, "seconds")
                    disp.x = 0
                    disp.z = 0  

            self.sf_output_matrix.value = self.sf_output_matrix.value * avango.gua.make_trans_mat(disp.x,trans_y,disp.z)
            #self.sf_output_matrix.value = self.sf_output_matrix.value * new_postion

        #animation
        height = math.sin(time.time()) * 8.0 + 3.0
        self.sf_animation_mat.value = avango.gua.make_trans_mat(height, 0.0, 0.0)