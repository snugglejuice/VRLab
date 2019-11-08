#!/usr/bin/python3

# import avango-guacamole libraries
import avango.daemon

# import python libraries
import os

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

        keyboard.buttons[0] = 'EV_KEY::KEY_W'
        keyboard.buttons[1] = 'EV_KEY::KEY_A'
        keyboard.buttons[2] = 'EV_KEY::KEY_S'
        keyboard.buttons[3] = 'EV_KEY::KEY_D'
        keyboard.buttons[4] = 'EV_KEY::KEY_RIGHTCTRL'
        keyboard.buttons[5] = 'EV_KEY::KEY_LEFT'
        keyboard.buttons[6] = 'EV_KEY::KEY_RIGHT'
        keyboard.buttons[7] = 'EV_KEY::KEY_LEFTALT'
        # YOUR CODE - BEGIN (Exercise 2.7 - Register Up and Down Arrow Keys)
        keyboard.buttons[8] = 'EV_KEY::KEY_UP'
        keyboard.buttons[9] = 'EV_KEY::KEY_DOWN'
        # YOUR CODE - END (Exercise 2.7 - Register Up and Down Arrow Keys)

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

        mouse.values[0] = 'EV_REL::REL_X'
        mouse.values[1] = 'EV_REL::REL_Y'
        mouse.buttons[0] = 'EV_KEY::BTN_LEFT'
        mouse.buttons[1] = 'EV_KEY::BTN_RIGHT'

        device_list.append(mouse)
        print('Mouse ' + mouse_list[0] + ' started')


# entry point when launching this file
if __name__ == '__main__':
    device_list = []
    init_keyboard()
    init_mouse()
    avango.daemon.run(device_list)
