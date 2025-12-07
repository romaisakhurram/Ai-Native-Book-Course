# Setting up ROS 2 and Gazebo for Digital Twin Simulation

This chapter provides a foundational guide for setting up your development environment to work with ROS 2 and Gazebo for robot simulation. A robust setup is crucial for building and interacting with digital twins.

## ROS 2 Installation

Ensure you have a working ROS 2 installation. If not, follow the official ROS 2 documentation for your operating system. For this module, we assume a [ROS 2 Humble Hawksbill](https://docs.ros.org/en/humble/Installation.html) installation on Ubuntu.

## Gazebo Installation

Gazebo is a powerful 3D robot simulator. It's often installed alongside ROS 2. Verify your Gazebo installation or follow the official instructions. For this module, we will primarily use [Gazebo Garden](https://gazebosim.org/docs/garden/install_ubuntu) which is the default for ROS 2 Humble.

## ROS 2 - Gazebo Integration

To allow ROS 2 to communicate with Gazebo, you'll need the `ros_gz` bridge packages.

```bash
sudo apt install ros-humble-ros-gz
```

## Verifying Your Setup

After installation, you can verify your setup by launching a simple Gazebo world and checking for ROS 2 topics.

1.  Launch a Gazebo simulation:
    ```bash
    gazebo # or ros2 launch ros_gz_sim_demos gz_sim_imu.launch.py
    ```
2.  In a new terminal, check for ROS 2 nodes and topics:
    ```bash
    ros2 node list
    ros2 topic list
    ```
    You should see Gazebo-related nodes and topics.

This foundational setup will enable you to create, simulate, and interact with your digital twin models.
