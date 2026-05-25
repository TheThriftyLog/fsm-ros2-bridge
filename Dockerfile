# =============================================================================
# Arduino FSM → ROS2 Bridge
# Single image for both fsm_talker and fsm_listener nodes
#
# Build:
#   docker build -t fsm-ros2 .
#
# Run talker (needs serial device access):
#   docker run --rm -it --device /dev/ttyACM0 --network host fsm-ros2 talker
#
# Run listener:
#   docker run --rm -it --network host fsm-ros2 listener
# =============================================================================

FROM ros:jazzy-ros-base

# Avoid interactive prompts during build
ENV DEBIAN_FRONTEND=noninteractive

# Install CycloneDDS RMW and Python serial library
RUN apt-get update && apt-get install -y --no-install-recommends \
    ros-jazzy-rmw-cyclonedds-cpp \
    python3-pip \
    python3-serial \
    && rm -rf /var/lib/apt/lists/*

# Pin setuptools for ROS2/Python 3.12 compatibility
RUN pip install --break-system-packages setuptools==70.0.0

# Set CycloneDDS as the default RMW
ENV RMW_IMPLEMENTATION=rmw_cyclonedds_cpp

# Copy workspace source
WORKDIR /ros2_ws
COPY src/ src/

# Build both packages
RUN . /opt/ros/jazzy/setup.sh && \
    colcon build --symlink-install

# Copy entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["listener"]
