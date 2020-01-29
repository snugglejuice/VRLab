#!/usr/bin/python3

# import avango-guacamole libraries
import avango
import avango.gua

# import application libraries
import config

# import python libraries
import math
import random
import time
import sys

# appends the objects to the scenegraph that will be visualized
class Scene:

    def __init__(self, scenegraph):
        self.scenegraph = scenegraph
        self.loader = avango.gua.nodes.TriMeshLoader()

        # build scene content
        self.build_light()
        self.build_scene()

    # adds a light to the scenegraph's root node
    def build_light(self):
        spotlight = avango.gua.nodes.LightNode(Name='spotlight')
        spotlight.Type.value = avango.gua.LightType.SPOT
        spotlight.Color.value = avango.gua.Color(1.0, 1.0, 0.9)
        spotlight.Brightness.value = 30.0
        spotlight.Falloff.value = 0.7
        spotlight.Transform.value = avango.gua.make_trans_mat(0.0, 400.0, 0.0) * \
            avango.gua.make_rot_mat(-90, 1, 0, 0) * \
            avango.gua.make_scale_mat(1000.0)
        self.scenegraph.Root.value.Children.value.append(spotlight)

    # adds the main geometry to the scenegraph's root node
    def build_scene(self):
        scene = self.loader.create_geometry_from_file('scene',
                                                      'data/objects/town/town.obj',
                                                      avango.gua.LoaderFlags.LOAD_MATERIALS |
                                                      avango.gua.LoaderFlags.MAKE_PICKABLE)
        self.apply_material_uniform_recursively(scene, 'Emissivity', 0.5)
        self.apply_material_uniform_recursively(scene, 'Roughness', 0.8)
        self.apply_backface_culling_recursively(scene, False)
        self.scenegraph.Root.value.Children.value.append(scene)

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
