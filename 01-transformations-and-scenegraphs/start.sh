#!/bin/bash

# determine absolute path of this file
GUACAMOLE=/opt/guacamole/master
AVANGO=/opt/avango/master

# set environment variables
export LD_LIBRARY_PATH=$GUACAMOLE/lib:$AVANGO/lib:/opt/boost/boost_1_55_0/lib:/opt/zmq/current/lib:/opt/Awesomium/lib:/opt/pbr/inst_cb/lib:/opt/schism/current/lib/linux_x86
export PYTHONPATH=$AVANGO/lib/python3.5:$AVANGO/examples

# run daemon and application
python3 daemon.py > /dev/null &
python3 main.py

# kill daemon after termination
kill %1
