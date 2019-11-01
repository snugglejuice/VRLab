#!/usr/bin/python3

# import avango-guacamole libraries
import avango
import avango.gua

# import python libraries
import math
import time

# appends the objects to the scenegraph that will be visualized
class Scene:

    def __init__(self, scenegraph):
        self.scenegraph = scenegraph
        self.loader = avango.gua.nodes.TriMeshLoader()

        # build scene content
        self.build_light()
        self.build_island()
        self.build_bird()

    # adds a light to the scenegraph's root nodes
    def build_light(self):
        self.lamp_node = avango.gua.nodes.LightNode(Type=avango.gua.LightType.SPOT,
                                                    Name='lamp',
                                                    EnableShadows=True,
                                                    Brightness=30.0,
                                                    ShadowMapSize=4096,
                                                    ShadowOffset=0.0001)
        self.lamp_node.Transform.value = avango.gua.make_trans_mat(5, 25, -5) * \
            avango.gua.make_rot_mat(45, 0, 1, 0) * \
            avango.gua.make_rot_mat(-80, 1, 0, 0) * \
            avango.gua.make_scale_mat(500, 500, 100)
        self.lamp_node.ShadowNearClippingInSunDirection.value = \
            self.lamp_node.ShadowNearClippingInSunDirection.value * \
            (1.0 / self.lamp_node.Transform.value.get_scale().z)
        self.lamp_node.ShadowFarClippingInSunDirection.value = \
            self.lamp_node.ShadowFarClippingInSunDirection.value * \
            (1.0 / self.lamp_node.Transform.value.get_scale().z)
        self.scenegraph.Root.value.Children.value.append(self.lamp_node)

    # adds an island model to the scenegraph's root node
    def build_island(self):
        self.island = self.loader.create_geometry_from_file('island_model',
                                                            'data/objects/island.obj',
                                                            avango.gua.LoaderFlags.LOAD_MATERIALS)
        self.apply_material_uniform_recursively(self.island, 'Emissivity', 0.3)
        self.apply_material_uniform_recursively(self.island, 'Roughness', 0.8)
        self.apply_material_uniform_recursively(self.island, 'Metalness', 0.0)
        self.island.Transform.value = avango.gua.make_scale_mat(2.0)
        self.scenegraph.Root.value.Children.value.append(self.island)

    # adds a bird model to the scenegraph's root node
    def build_bird(self):
        self.rotation_animator = RotationAnimator()

        # rotation animation node
        self.bird_rot_animation = avango.gua.nodes.TransformNode(
            Name='bird_rot_animation')
        self.bird_rot_animation.Transform.connect_from(
            self.rotation_animator.sf_rot_mat)
        self.scenegraph.Root.value.Children.value.append(
            self.bird_rot_animation)

        # bird transformation node
        self.bird_transform = avango.gua.nodes.TransformNode(
            Name='bird_transform')
        self.bird_transform.Transform.value = avango.gua.make_trans_mat(12.0, 7.0, 0.0) * \
            avango.gua.make_rot_mat(25, 0, 0, 1)
        self.bird_rot_animation.Children.value.append(self.bird_transform)

        # bird geometry node including scaling
        self.bird = self.loader.create_geometry_from_file('bird_model',
                                                          'data/objects/birdie_smooth.obj',
                                                          avango.gua.LoaderFlags.LOAD_MATERIALS)
        self.apply_material_uniform_recursively(self.bird, 'Emissivity', 1)
        self.apply_material_uniform_recursively(self.bird, 'Roughness', 0.5)
        self.apply_material_uniform_recursively(self.bird, 'Metalness', 0.0)
        self.apply_backface_culling_recursively(self.bird, False)
        self.bird.Transform.value = avango.gua.make_scale_mat(0.5)
        self.bird_transform.Children.value.append(self.bird)

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

# Field Container taking the rotation speed as input and outputting an animated rotation matrix
class RotationAnimator(avango.script.Script):

    # input field
    sf_rotation_speed = avango.SFFloat()
    sf_rotation_speed.value = 40.0  # deg/s

    # output field
    sf_rot_mat = avango.gua.SFMatrix4()
    sf_rot_mat.value = avango.gua.make_identity_mat()

    def __init__(self):
        self.super(RotationAnimator).__init__()
        # YOUR CODE - BEGIN (Exercise 2.8 - Frame-Rate Independent Mapping of Bird)
        # ...
        # YOUR CODE - END (Exercise 2.8 - Frame-Rate Independent Mapping of Bird)
        self.always_evaluate(True)

    # called every frame because of self.always_evaluate(True)
    def evaluate(self):
        # YOUR CODE - BEGIN (Exercise 2.8 - Frame-Rate Independent Mapping of Bird)
        self.sf_rot_mat.value = avango.gua.make_rot_mat(0.1, 0, 1, 0) * \
            self.sf_rot_mat.value
        # YOUR CODE - BEGIN (Exercise 2.8 - Frame-Rate Independent Mapping of Bird)
