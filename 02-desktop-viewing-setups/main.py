#!/usr/bin/python3

# import avango-guacamole libraries
import avango
import avango.gua

# import application libraries
from lib.DesktopViewingSetup import *
from lib.Renderer import *
from lib.Scene import *


def start():
    # scenegraph
    scenegraph = avango.gua.nodes.SceneGraph(Name="scenegraph")

    # create scene branch of scenegraph
    scene = Scene(scenegraph)

    # create viewing setup branch of scenegraph
    viewing_setup = DesktopViewingSetup()
    viewing_setup.create(scenegraph)

    # print scenegraph
    print_graph(scenegraph.Root.value)

    # create renderer to display scenegraph
    renderer = Renderer(scenegraph, viewing_setup)
    renderer.run(locals(), globals())


def print_graph(root_node):
    stack = [(root_node, 0)]
    while stack:
        node, level = stack.pop()
        print("│   " * level + "├── {0} <{1}>".format(
              node.Name.value, node.__class__.__name__))
        if not node.Name.value == 'island_model' and \
           not node.Name.value == 'bird_model':
            stack.extend([(child, level + 1) for child in
                          reversed(node.Children.value)])


# entry point when launching this file
if __name__ == '__main__':
    start()
