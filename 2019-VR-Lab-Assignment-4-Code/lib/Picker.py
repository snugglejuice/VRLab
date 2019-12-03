#!/usr/bin/python3

# import avango-guacamole libraries
import avango
import avango.gua

# class computing intersections with the scene geometry
class Picker:

    def __init__(self, scenegraph):
        self.scenegraph = scenegraph

        # specify picking options
        self.picking_options = avango.gua.PickingOptions.GET_POSITIONS | \
            avango.gua.PickingOptions.GET_NORMALS | \
            avango.gua.PickingOptions.GET_WORLD_POSITIONS | \
            avango.gua.PickingOptions.GET_WORLD_NORMALS | \
            avango.gua.PickingOptions.PICK_ONLY_FIRST_OBJECT

    # computes an intersection with the scene using the given intersection ray parameters
    def compute_pick_result(self, pos, direction, length, blacklist):
        picking_ray = avango.gua.nodes.Ray()
        picking_ray.Origin.value = pos
        picking_ray.Direction.value = direction
        picking_ray.Direction.value.normalize()
        picking_ray.Direction.value *= length
        picking_results = self.scenegraph.ray_test(
            picking_ray, self.picking_options, [], blacklist)

        if len(picking_results.value) > 0:
            picking_results.value[0].Distance.value *= length
            return picking_results.value[0]
        return None
