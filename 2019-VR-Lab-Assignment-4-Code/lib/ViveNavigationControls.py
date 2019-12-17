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
    	#4.7
    	if(rocker_value != 0):
    		disp = self.controller1_node.WorldTransform.value.get_translate() - self.head_node.WorldTransform.value.get_translate()
    		dist = math.sqrt(disp.x**2+disp.z**2)
    		angle = math.acos(disp.x/dist)
    		print(angle)
    		if ((disp.x > 0) & (disp.z > 0)):
    			self.sf_output_matrix.value = self.sf_output_matrix.value * avango.gua.make_rot_mat(angle,0,1,0) * avango.gua.make_trans_mat(dist*0.01,0,0) * avango.gua.make_rot_mat(-angle,0,1,0)
    		if ((disp.x > 0) & (disp.z < 0)):
    			self.sf_output_matrix.value = self.sf_output_matrix.value * avango.gua.make_rot_mat(angle,0,1,0) * avango.gua.make_trans_mat(dist*0.01,0,0) * avango.gua.make_rot_mat(-angle,0,1,0)
			if ((disp.x < 0) & (disp.z > 0)):
				self.sf_output_matrix.value = self.sf_output_matrix.value * avango.gua.make_rot_mat(-angle,0,1,0) * avango.gua.make_trans_mat(dist*0.01,0,0) * avango.gua.make_rot_mat(angle,0,1,0)
			if ((disp.x < 0) & (disp.z < 0)):
				self.sf_output_matrix.value = self.sf_output_matrix.value * avango.gua.make_rot_mat(-angle,0,1,0) * avango.gua.make_trans_mat(dist*0.01,0,0) * avango.gua.make_rot_mat(angle,0,1,0) 
        	