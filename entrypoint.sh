#!/bin/bash
set -e

# Source ROS2 and workspace
source /opt/ros/jazzy/setup.bash
source /ros2_ws/install/setup.bash

case "$1" in
  talker)
    echo "Starting fsm_talker node..."
    exec ros2 run fsm_talker fsm_talker
    ;;
  listener)
    echo "Starting fsm_listener node..."
    exec ros2 run fsm_listener fsm_listener
    ;;
  *)
    echo "Usage: docker run fsm-ros2 [talker|listener]"
    echo ""
    echo "  talker   - Reads Arduino serial, publishes to /led_state"
    echo "             Requires: --device /dev/ttyACM0 --network host"
    echo ""
    echo "  listener - Subscribes to /led_state, logs state changes"
    echo "             Requires: --network host"
    exit 1
    ;;
esac
