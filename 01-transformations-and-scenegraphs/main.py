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
    viewing_setup = DesktopViewingSetup(scenegraph)

    # create renderer to display scenegraph
    renderer = Renderer(scenegraph, viewing_setup)
    renderer.run(locals(), globals())


# entry point when launching this file
if __name__ == '__main__':
    start()
