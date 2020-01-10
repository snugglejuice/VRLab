#!/usr/bin/python3

# import avango-guacamole libraries
import avango.daemon

# import application libraries
import config

# import python libraries
import os
import sys

# registers a head-mounted display connection
def init_hmd_tracking(id, server_ip, port):
    hmd = avango.daemon.HMDTrack()
    for i in range(7):
        hmd.stations[i] = avango.daemon.Station(
            'gua-device-hmd-{0}-{1}'.format(str(id), str(i)))
    hmd.server = server_ip
    hmd.port = port
    device_list.append(hmd)
    print("Head-Mounted Display started at: " + str(server_ip))


# entry point when launching this file
if __name__ == '__main__':
    device_list = []

    if sys.platform.startswith('win'):  # head-mounted display on windows
        init_hmd_tracking(0, config.HMD_IP_ADDRESS, '7770')
    else:  # desktop setup on linux
        pass

    avango.daemon.run(device_list)
