#!/usr/bin/python3

# import avango-guacamole libraries
import avango
import avango.gua

# import application libraries
import config
from lib.DesktopViewingSetup import *
from lib.Renderer import *
from lib.Scene import *
from lib.ViveViewingSetup import *

# import python libraries
import os
import sys

def start():
    # scenegraph
    scenegraph = avango.gua.nodes.SceneGraph(Name="scenegraph")

    # create scene branch of scenegraph
    scene = Scene(scenegraph)

    # create viewing setup branch of scenegraph
    if sys.platform.startswith('win'):
        os.system('cd hmd-tracker && start \"avango\" cmd /K HMDTracker.exe ' +
                  str(config.HMD_IP_ADDRESS) + ':7770 500')
        viewing_setup = ViveViewingSetup(scenegraph)
    else:
        viewing_setup = DesktopViewingSetup(scenegraph)

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
        stack.extend([(child, level + 1) for child in
                      reversed(node.Children.value)])

# entry point when launching this file
if __name__ == '__main__':
    start()
