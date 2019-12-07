#!/usr/bin/python3

# import avango-guacamole libraries
import avango
import avango.daemon
import avango.gua

# import application libraries
from lib.NavigationControls import NavigationControls

# import python libraries
import math
import time

# constant size of the window on the monitor in meters
SCREEN_SIZE = avango.gua.Vec2(0.45, 0.25)

# appends a camera node, screen node, and navigation capabilities to the scenegraph
class DesktopViewingSetup:

    def __init__(self, scenegraph):
        self.scenegraph = scenegraph

        # navigation node
        self.navigation_node = avango.gua.nodes.TransformNode(
            Name='navigation_node')
        self.navigation_controls = NavigationControls()
        self.navigation_controls.set_scenegraph(self.scenegraph)
        self.navigation_node.Transform.connect_from(
            self.navigation_controls.sf_output_matrix)
        self.scenegraph.Root.value.Children.value.append(self.navigation_node)

        # avatar
        self.loader = avango.gua.nodes.TriMeshLoader()
        self.avatar = self.loader.create_geometry_from_file('avatar',
                                                            'data/objects/figure.obj',
                                                            avango.gua.LoaderFlags.LOAD_MATERIALS)
        for child in self.avatar.Children.value:
            child.Material.value.set_uniform("Roughness", 0.6)
        self.navigation_node.Children.value.append(self.avatar)

        # 4.5

        sphere_coords = [avango.gua.Vec3(5,9,-13),
                        avango.gua.Vec3(10,8,-13),
                        avango.gua.Vec3(10,8,-15),
                        avango.gua.Vec3(0,1, 5),
                        avango.gua.Vec3(5,1,4)]
        self.pickable_object_list = []

        for i in range(len(sphere_coords)):
            obj_transform = self.loader.create_geometry_from_file('sphere_'+str(i),'data/objects/sphere.obj',avango.gua.LoaderFlags.LOAD_MATERIALS |avango.gua.LoaderFlags.MAKE_PICKABLE)
            
            obj_transform.Transform.value = avango.gua.make_trans_mat(sphere_coords[i].x, sphere_coords[i].y, sphere_coords[i].z)
            self.pickable_object_list.append(obj_transform)
            self.scenegraph.Root.value.Children.value.append(obj_transform)

        self.navigation_controls.set_pickable_object(self.pickable_object_list)
        # screen node
        self.screen_dimensions = SCREEN_SIZE
        self.screen_node = avango.gua.nodes.ScreenNode(Name='screen_node')
        self.screen_node.Width.value = self.screen_dimensions.x
        self.screen_node.Height.value = self.screen_dimensions.y
        self.screen_node.Transform.value = avango.gua.make_trans_mat(
            0.0, 0.0, -0.6)
        #self.navigation_node.Children.value.append(self.screen_node)

        # camera node (head)
        self.camera_node = avango.gua.nodes.CameraNode(Name='camera_node')
        self.camera_node.SceneGraph.value = self.scenegraph.Name.value
        #self.camera_node.LeftScreenPath.value = self.screen_node.Path.value
        self.camera_node.BlackList.value = ['invisible']
        #self.navigation_node.Children.value.append(self.camera_node)
        # 4.2
        self.camera_rot = avango.gua.nodes.TransformNode(Name='camera_rot')
        self.camera_rot.Transform.value = avango.gua.make_identity_mat()
        #self.camera_rot.Transform.value = avango.gua.make_rot_mat(self.navigation_controls.sf_input_rx.value*0.05,1,0,0)
        self.camera_trans = avango.gua.nodes.TransformNode(Name='camera_trans')
        self.camera_trans.Transform.value = avango.gua.make_trans_mat(0,0,30) 
        self.avatar.Children.value.append(self.camera_rot)
        self.camera_rot.Children.value.append(self.camera_trans)
        self.camera_trans.Children.value.append(self.screen_node)
        self.camera_node.LeftScreenPath.value = self.screen_node.Path.value
        self.camera_trans.Children.value.append(self.camera_node)

    # registers a window created in the class Renderer with the camera node
    def register_window(self, window):
        self.camera_node.OutputWindowName.value = window.Title.value
        self.camera_node.Resolution.value = window.Size.value
        avango.gua.register_window(window.Title.value, window)

    # registers a pipeline description in the class Renderer with the camera node
    def register_pipeline_description(self, pipeline_description):
        self.camera_node.PipelineDescription.value = pipeline_description

        
