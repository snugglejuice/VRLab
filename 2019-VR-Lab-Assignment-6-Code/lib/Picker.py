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
            avango.gua.PickingOptions.GET_WORLD_NORMALS

    # computes an intersection with the scene using the given intersection ray parameters
    def compute_all_pick_results(self, pos, direction, length, blacklist):
        picking_ray = avango.gua.nodes.Ray()
        picking_ray.Origin.value = pos
        picking_ray.Direction.value = direction / direction.length()
        picking_ray.Direction.value *= length
        picking_results = self.scenegraph.ray_test(
            picking_ray, self.picking_options, [], blacklist)

        output_list = []
        for pick_result in picking_results.value:
            pick_result.Distance.value *= length
            output_list.append(pick_result)
        return output_list
