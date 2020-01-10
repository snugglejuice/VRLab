#!/usr/bin/python3

# import avango-guacamole libraries
import avango
import avango.gua

# IP address of machine to which HMD is attached
HMD_IP_ADDRESS = '141.54.147.27'

# Object colors
OBJECT_COLORS = [avango.gua.Vec4(1.0, 0.0, 0.0, 1.0),
                 avango.gua.Vec4(1.0, 0.65, 0.0, 1.0),
                 avango.gua.Vec4(1.0, 1.0, 0.0, 1.0),
                 avango.gua.Vec4(0.0, 1.0, 0.0, 1.0),
                 avango.gua.Vec4(0.63, 0.13, 0.94, 1.0)]