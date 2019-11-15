#!/usr/bin/python3

# import avango-guacamole libraries
import avango
import avango.gua

# import application libraries
from lib.BirdControls import BirdControls

# import python libraries
import math
import time

# appends the objects to the scenegraph that will be visualized
class Scene:

    def __init__(self, scenegraph):
        self.scenegraph = scenegraph
        self.loader = avango.gua.nodes.TriMeshLoader()
        self.bird_start_transform = avango.gua.make_trans_mat(0.0, 25.0, 80.0)

        # build scene content
        self.build_light()
        self.build_mountains()
        self.build_target_spheres()
        self.build_bird()

    # adds a light to the scenegraph's root nodes
    def build_light(self):
        self.lamp_node = avango.gua.nodes.LightNode(Type=avango.gua.LightType.SPOT,
                                                    Name='lamp',
                                                    EnableShadows=False,
                                                    Brightness=20.0)
        self.lamp_node.Transform.value = avango.gua.make_trans_mat(0, 200, 0) * \
            avango.gua.make_rot_mat(-90, 1, 0, 0) * \
            avango.gua.make_scale_mat(1000, 1000, 600)
        self.scenegraph.Root.value.Children.value.append(self.lamp_node)

    # adds a montain model to the scenegraph's root node
    def build_mountains(self):
        self.mountains = self.loader.create_geometry_from_file('mountains',
                                                               'data/objects/mountains.obj',
                                                               avango.gua.LoaderFlags.LOAD_MATERIALS)
        self.apply_material_uniform_recursively(
            self.mountains, 'Color', avango.gua.Vec4(0.0, 0.3, 0.0, 1.0))
        self.apply_material_uniform_recursively(
            self.mountains, 'Emissivity', 0.5)
        self.apply_material_uniform_recursively(
            self.mountains, 'Roughness', 0.8)
        self.apply_material_uniform_recursively(
            self.mountains, 'Metalness', 0.0)
        self.mountains.Transform.value = avango.gua.make_scale_mat(10.0)
        self.scenegraph.Root.value.Children.value.append(self.mountains)

    # adds the target spheres to the scenegraph's root node
    def build_target_spheres(self):
        sphere_xy_coords = [avango.gua.Vec2(-9.0, 30.0),
                            avango.gua.Vec2(8.0, 23.0),
                            avango.gua.Vec2(1.0, 21.0),
                            avango.gua.Vec2(-6.0, 23.0),
                            avango.gua.Vec2(-0.5, 28.0),
                            avango.gua.Vec2(7.0, 29.0)]
        self.target_spheres = []

        for i in range(len(sphere_xy_coords)):
            sphere = self.loader.create_geometry_from_file('sphere_' + str(i),
                                                           'data/objects/sphere.obj',
                                                           avango.gua.LoaderFlags.DEFAULTS)
            self.apply_material_uniform_recursively(
                sphere, 'Color', avango.gua.Vec4(0.1, 0.1, 1.0, 1.0))
            self.apply_material_uniform_recursively(sphere, 'Emissivity', 0.2)
            self.apply_material_uniform_recursively(sphere, 'Roughness', 0.8)
            self.apply_material_uniform_recursively(sphere, 'Metalness', 0.5)
            sphere_x = sphere_xy_coords[i].x
            sphere_y = sphere_xy_coords[i].y
            sphere.Transform.value = avango.gua.make_trans_mat(sphere_x, sphere_y,
                                                               self.bird_start_transform.get_translate().z - 0.25) * avango.gua.make_scale_mat(0.5)
            self.target_spheres.append(sphere)
            self.scenegraph.Root.value.Children.value.append(sphere)

    # adds a bird model to the scenegraph's root node
    def build_bird(self):
        self.bird_transform = avango.gua.nodes.TransformNode(
            Name='bird_transform')
        self.bird_transform.Transform.value = self.bird_start_transform
        self.scenegraph.Root.value.Children.value.append(self.bird_transform)

        self.bird = self.loader.create_geometry_from_file('bird_model',
                                                          'data/objects/birdie_smooth.obj',
                                                          avango.gua.LoaderFlags.LOAD_MATERIALS)
        self.apply_material_uniform_recursively(self.bird, 'Emissivity', 0.0)
        self.apply_material_uniform_recursively(self.bird, 'Roughness', 0.6)
        self.apply_material_uniform_recursively(self.bird, 'Metalness', 0.0)
        self.apply_backface_culling_recursively(self.bird, False)
        self.bird.Transform.value = avango.gua.make_rot_mat(
            -90, 0, 1, 0) * avango.gua.make_scale_mat(1.5)
        self.bird_transform.Children.value.append(self.bird)

        self.bird_controls = BirdControls()
        self.bird_controls.set_bird_transform_node(
            self.bird_transform, self.target_spheres)

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
