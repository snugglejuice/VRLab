#!/usr/bin/python3

# import avango-guacamole libraries
import avango
import avango.gua

# import python libraries
import math
import time
import sys

# appends the objects to the scenegraph that will be visualized
class Scene:

    def __init__(self, scenegraph):
        self.scenegraph = scenegraph
        self.loader = avango.gua.nodes.TriMeshLoader()

        # build scene content
        self.build_light()
        self.build_park()
        self.build_platform()

    # adds a light to the scenegraph's root nodes
    def build_light(self):
        enable_shadows = True
        if sys.platform.startswith('win'):
            enable_shadows = False

        self.lamp_node = avango.gua.nodes.LightNode(Type=avango.gua.LightType.SPOT,
                                                    Name='lamp',
                                                    EnableShadows=enable_shadows,
                                                    Brightness=15.0,
                                                    Falloff=1.0,
                                                    ShadowMapSize=4096,
                                                    ShadowMaxDistance=150.0,
                                                    ShadowNearClippingInSunDirection=0.05,
                                                    ShadowFarClippingInSunDirection=1.0,
                                                    ShadowOffset=0.0001)

        self.lamp_node.Transform.value = avango.gua.make_trans_mat(-42.344, 43.267, 21.031) * \
            avango.gua.make_rot_mat(avango.gua.Quat(0.866, -0.434, -0.322, -0.033)) * \
            avango.gua.make_scale_mat(150.0, 150.0, 100.0)
        self.scenegraph.Root.value.Children.value.append(self.lamp_node)

    # adds a park model to the scenegraph's root node
    def build_park(self):
        self.park = self.loader.create_geometry_from_file('park',
                                                          'data/objects/park.obj',
                                                          avango.gua.LoaderFlags.LOAD_MATERIALS |
                                                          avango.gua.LoaderFlags.MAKE_PICKABLE)
        self.apply_material_uniform_recursively(
            self.park, 'Emissivity', 0.4)
        self.apply_material_uniform_recursively(
            self.park, 'Roughness', 0.8)
        self.apply_material_uniform_recursively(
            self.park, 'Metalness', 0.0)
        self.apply_backface_culling_recursively(self.park, False)
        self.park.Transform.value = avango.gua.make_scale_mat(2.5)
        self.scenegraph.Root.value.Children.value.append(self.park)

    # adds a moving platform to the scenegraph's root node
    def build_platform(self):
        self.platform_scene_transform = avango.gua.nodes.TransformNode(
            Name='platform_scene_transform')
        self.platform_scene_transform.Transform.value = avango.gua.make_trans_mat(
            4.0, 0.0, -12.8)
        self.scenegraph.Root.value.Children.value.append(
            self.platform_scene_transform)

        platform_animator = UpAndDownAnimator()
        self.platform_up_transform = avango.gua.nodes.TransformNode(
            Name='platform_up_transform')
        self.platform_up_transform.Transform.connect_from(
            platform_animator.sf_output_mat)
        self.platform_scene_transform.Children.value.append(
            self.platform_up_transform)

        self.platform = self.loader.create_geometry_from_file('platform',
                                                              'data/objects/cube.obj',
                                                              avango.gua.LoaderFlags.MAKE_PICKABLE)
        self.platform.Material.value.set_uniform(
            'Color', avango.gua.Vec4(0.0, 0.0, 0.0, 1.0))
        self.platform.Material.value.set_uniform(
            'Emissivity', 0.5)
        self.platform.Transform.value = avango.gua.make_scale_mat(
            5.0, 0.1, 5.0)
        self.platform_up_transform.Children.value.append(self.platform)

    # applys a material uniform to all TriMeshNode instances below the specified start node
    def apply_material_uniform_recursively(self, start_node, uniform_name, uniform_value):
        if start_node.__class__.__name__ == "TriMeshNode":
            start_node.Material.value.set_uniform(uniform_name, uniform_value)

        for child in start_node.Children.value:
            self.apply_material_uniform_recursively(
                child, uniform_name, uniform_value)

    # applys a backface culling value to all TriMeshNode instances below the specified start node
    def apply_backface_culling_recursively(self, start_node, boolean):
        if start_node.__class__.__name__ == "TriMeshNode":
            start_node.Material.value.EnableBackfaceCulling.value = boolean

        for child in start_node.Children.value:
            self.apply_backface_culling_recursively(child, boolean)

# Field Container producing an up-and-down animation matrix
class UpAndDownAnimator(avango.script.Script):

    # output fields
    sf_output_mat = avango.gua.SFMatrix4()
    sf_output_mat.value = avango.gua.make_identity_mat()

    def __init__(self):
        self.super(UpAndDownAnimator).__init__()
        self.always_evaluate(True)

    # called every frame because of self.always_evaluate(True)
    def evaluate(self):
        height = math.sin(time.time()) * 4.0 + 3.0
        self.sf_output_mat.value = avango.gua.make_trans_mat(0.0, height, 0.0)
