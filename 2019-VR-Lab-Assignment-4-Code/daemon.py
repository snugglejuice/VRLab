#!/usr/bin/python3

# import avango-guacamole libraries
import avango.daemon

# import application libraries
import config

# import python libraries
import os
import sys

# registers a keyboard device for the application (Name: gua-device-keyboard)
def init_keyboard():
    keyboard_list = os.popen(
        "ls /dev/input/by-path | grep \"-event-kbd\" | sed -e \'s/\"//g\'  | cut -d\" \" -f4").read()
    keyboard_list = keyboard_list.split('\n')
    keyboard_list.remove('')
    keyboard_list.sort(key=lambda entry: float(entry.split(':')[3]))

    if len(keyboard_list) > 0:
        keyboard = avango.daemon.HIDInput()
        keyboard.station = avango.daemon.Station('gua-device-keyboard')
        keyboard.device = '/dev/input/by-path/' + keyboard_list[0]

        keyboard.buttons[0] = 'EV_KEY::KEY_SPACE'
        keyboard.buttons[1] = 'EV_KEY::KEY_1'
        keyboard.buttons[2] = 'EV_KEY::KEY_2'
        keyboard.buttons[3] = 'EV_KEY::KEY_3'
        keyboard.buttons[4] = 'EV_KEY::KEY_4'
        keyboard.buttons[5] = 'EV_KEY::KEY_5'
        keyboard.buttons[6] = 'EV_KEY::KEY_6'
        keyboard.buttons[7] = 'EV_KEY::KEY_7'

        device_list.append(keyboard)
        print('Keyboard ' + keyboard_list[0] + ' started')

# registers a mouse device for the application (Name: gua-device-mouse)
def init_mouse():
    mouse_list = os.popen(
        "ls /dev/input/by-path | grep \"-event-mouse\" | sed -e \'s/\"//g\'  | cut -d\" \" -f4").read()
    mouse_list = mouse_list.split('\n')
    mouse_list.remove('')
    mouse_list.sort(key=lambda entry: float(entry.split(':')[3]))

    if len(mouse_list) > 0:
        mouse = avango.daemon.HIDInput()
        mouse.station = avango.daemon.Station('gua-device-mouse')
        mouse.device = '/dev/input/by-path/' + mouse_list[0]
        mouse.timeout = '10'

        mouse.values[0] = 'EV_REL::REL_X'
        mouse.values[1] = 'EV_REL::REL_Y'
        mouse.buttons[0] = 'EV_KEY::BTN_LEFT'
        mouse.buttons[1] = 'EV_KEY::BTN_RIGHT'

        device_list.append(mouse)
        print('Mouse ' + mouse_list[0] + ' started')

# registers a new space navigator device for the application (Name: gua-device-space)
def init_blue_space_navigator():
    event_string = get_event_string("3Dconnexion SpaceNavigator for Notebooks")

    if len(event_string) == 0:
        event_string = get_event_string("3Dconnexion SpaceNavigator")

    if len(event_string) == 0:
        event_string = get_event_string("3Dconnexion SpaceMouse Compact")

    if len(event_string) > 0:
        event_string = event_string.split()[0]

        space_navigator = avango.daemon.HIDInput()
        space_navigator.station = avango.daemon.Station('gua-device-space')
        space_navigator.device = event_string
        space_navigator.timeout = '14'
        space_navigator.norm_abs = 'True'

        space_navigator.values[0] = "EV_REL::REL_X"
        space_navigator.values[1] = "EV_REL::REL_Y"
        space_navigator.values[2] = "EV_REL::REL_Z"
        space_navigator.values[3] = "EV_REL::REL_RX"
        space_navigator.values[4] = "EV_REL::REL_RZ"
        space_navigator.values[5] = "EV_REL::REL_RY"

        device_list.append(space_navigator)
        print("Blue Space Navigator started at:", event_string)

# queries an input device by its name
def get_event_string(device_name):
    # file containing all devices with additional information
    device_file = os.popen("cat /proc/bus/input/devices").read()
    device_file = device_file.split("\n")
    device_name = '\"' + device_name + '\"'

    # matching lines in device file
    indices = []
    for i, line in enumerate(device_file):
        if device_name in line:
            indices.append(i)

    # if no device was found, return an empty string
    if len(indices) == 0:
        return ""

    # else captue the event number X of one specific device and return /dev/input/eventX
    else:
        event_string_start_index = device_file[indices[0]+4].find("event")
        return "/dev/input/" + device_file[indices[0]+4][event_string_start_index:].split(" ")[0]

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
        init_keyboard()
        init_mouse()
        init_blue_space_navigator()

    avango.daemon.run(device_list)
