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
        self.num_objects = 30
        self.object_scale = 0.075

        # build scene content
        self.build_light()
        self.build_floor()
        self.build_objects()

    # adds a light to the scenegraph's root node
    def build_light(self):
        spotlight = avango.gua.nodes.LightNode(Name='spotlight')
        spotlight.Type.value = avango.gua.LightType.SPOT
        spotlight.Color.value = avango.gua.Color(1.0, 1.0, 0.9)
        spotlight.Brightness.value = 20.0
        spotlight.Falloff.value = 0.7
        spotlight.Transform.value = avango.gua.make_trans_mat(0.0, 20.0, 0.0) * \
            avango.gua.make_rot_mat(-90, 1, 0, 0) * \
            avango.gua.make_scale_mat(30.0)
        self.scenegraph.Root.value.Children.value.append(spotlight)

    # adds the floor geometry to the scenegraph's root node
    def build_floor(self):
        floor = self.loader.create_geometry_from_file('floor',
                                                      'data/objects/plane.obj',
                                                      avango.gua.LoaderFlags.DEFAULTS)
        self.apply_material_uniform_recursively(
            floor, 'ColorMap', 'data/textures/tiles.tif')
        self.apply_material_uniform_recursively(floor, 'Roughness', 0.5)
        floor.Transform.value = avango.gua.make_scale_mat(10.0)
        self.scenegraph.Root.value.Children.value.append(floor)

    # adds some objects to the scenegraph's root node
    def build_objects(self):
        file_handle = open('data/objects/object_positions.txt', 'r')
        for line_num, line in enumerate(file_handle):
            splitted_line = line.split(',')
            file_path = splitted_line[0]
            piece = self.loader.create_geometry_from_file('object_' + str(line_num),
                                                          file_path,
                                                          avango.gua.LoaderFlags.MAKE_PICKABLE)
            position = avango.gua.Vec3(float(splitted_line[1]), float(
                splitted_line[2]), float(splitted_line[3]))
            quat = avango.gua.Quat(float(splitted_line[4]), float(
                splitted_line[5]), float(splitted_line[6]), float(splitted_line[7]))
            piece.Transform.value = avango.gua.make_trans_mat(position) * \
                avango.gua.make_rot_mat(quat) * \
                avango.gua.make_scale_mat(self.object_scale)
            color_id = int(file_path[-5])-1
            piece.Tags.value.append(str(color_id))
            piece.Material.value.set_uniform(
                'Color', config.OBJECT_COLORS[color_id])
            piece.Material.value.set_uniform('Emissivity', 0.5)
            self.scenegraph.Root.value.Children.value.append(piece)
        file_handle.close()

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
