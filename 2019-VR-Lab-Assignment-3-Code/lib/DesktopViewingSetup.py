#!/usr/bin/python3

# import avango-guacamole libraries
import avango
import avango.daemon
import avango.gua
from avango.script import field_has_changed

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
        self.navigation_node.Transform.value = avango.gua.make_trans_mat(
            0.0, 25.0, 110.0)
        self.scenegraph.Root.value.Children.value.append(self.navigation_node)

        self.navigation_lamp_node = avango.gua.nodes.LightNode(Type=avango.gua.LightType.SPOT,
                                                               Name='navigation_lamp',
                                                               Brightness=5.0)
        self.navigation_lamp_node.Transform.value = avango.gua.make_scale_mat(
            100.0)
        self.navigation_node.Children.value.append(self.navigation_lamp_node)

        # screen node
        self.screen_dimensions = SCREEN_SIZE
        self.screen_node = avango.gua.nodes.ScreenNode(Name='screen_node')
        self.screen_node.Width.value = self.screen_dimensions.x
        self.screen_node.Height.value = self.screen_dimensions.y
        self.screen_node.Transform.value = avango.gua.make_trans_mat(
            0.0, 0.0, -0.6)
        self.navigation_node.Children.value.append(self.screen_node)

        # camera node (head)
        self.camera_node = avango.gua.nodes.CameraNode(Name='camera_node')
        self.camera_node.SceneGraph.value = self.scenegraph.Name.value
        self.camera_node.LeftScreenPath.value = self.screen_node.Path.value
        self.camera_node.BlackList.value = ['invisible']
        self.navigation_node.Children.value.append(self.camera_node)

    # registers a window created in the class Renderer with the camera node
    def register_window(self, window):
        self.camera_node.OutputWindowName.value = window.Title.value
        self.camera_node.Resolution.value = window.Size.value
        avango.gua.register_window(window.Title.value, window)

    # registers a pipeline description in the class Renderer with the camera node
    def register_pipeline_description(self, pipeline_description):
        self.camera_node.PipelineDescription.value = pipeline_description
