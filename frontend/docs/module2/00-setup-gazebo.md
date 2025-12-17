# Setting up ROS 2 and Gazebo for Digital Twin Simulation

This chapter provides a foundational guide for setting up your development environment to work with ROS 2 and Gazebo for robot simulation. A robust setup is crucial for building and interacting with digital twins, allowing you to develop and test robot behaviors in a virtual environment.

## Learning Objectives

After completing this chapter, you will be able to:

-   Install Gazebo Garden on your Ubuntu system.
-   Install and configure the `ros_gz` bridge for ROS 2 and Gazebo integration.
-   Verify your combined ROS 2 and Gazebo setup.

## 1.1 Prerequisites

Ensure you have a working ROS 2 Humble Hawksbill installation, as covered in a previous module. This chapter assumes you are running Ubuntu 22.04.

## 1.2 Installing Gazebo Garden

Gazebo is a powerful 3D robot simulator widely used in the robotics community. We will install Gazebo Garden, which is the default Gazebo version integrated with ROS 2 Humble.

### Step 1: Add Gazebo Repository

First, add the Gazebo GPG key and the repository to your system.

```bash
sudo apt update
sudo apt install -y software-properties-common lsb-release
sudo sh -c 'echo "deb [arch=$(dpkg --print-architecture)] http://packages.gazebosim.org/ubuntu $(lsb_release -cs) main" > /etc/apt/sources.list.d/gazebo-latest.list'
sudo apt update
```

### Step 2: Install Gazebo Packages

Install the full Gazebo Garden suite.

```bash
sudo apt install -y gazebo-garden
```

:::info
This will install the Gazebo simulator, its graphical user interface (GUI), and all necessary libraries.
:::

## 1.3 ROS 2 - Gazebo Integration (`ros_gz` Bridge)

To enable communication between ROS 2 and Gazebo, you need to install the `ros_gz` bridge packages. This bridge allows ROS 2 messages to be translated into Gazebo messages and vice-versa, facilitating control and sensing of simulated robots.

```bash
sudo apt install ros-humble-ros-gz
```

### Explanation of `ros_gz`

The `ros_gz` package provides several components:
-   **`ros_gz_bridge`**: The core component that translates messages between ROS 2 and Gazebo topics.
-   **`ros_gz_sim`**: Provides launch files and utilities to start Gazebo simulations with ROS 2 integration.
-   **`ros_gz_image`**: For bridging image topics.

## 1.4 Verifying Your Setup

After installing both Gazebo and the `ros_gz` bridge, it's crucial to verify that everything is working as expected.

### Step 1: Launch a Simple Gazebo World with ROS 2 Integration

We will use an example launch file provided by `ros_gz_sim` to start a Gazebo world and automatically bridge some topics.

```bash
source /opt/ros/humble/setup.bash
ros2 launch ros_gz_sim_demos gz_sim_imu.launch.py
```

This command should open a Gazebo window with a simple world containing an IMU sensor. It also starts a ROS 2 node that bridges the IMU data from Gazebo to a ROS 2 topic.

### Step 2: Check for ROS 2 Nodes and Topics

Open a **new terminal window**, and remember to source your ROS 2 setup again.

```bash
source /opt/ros/humble/setup.bash
ros2 node list
```

You should see nodes like `/imu_broadcaster` (from the launch file) and potentially other Gazebo-related nodes.

Now, check the active topics:

```bash
ros2 topic list
```

You should see topics such as `/imu` (publishing IMU data from Gazebo) and other Gazebo internal topics.

To further verify, you can `echo` the IMU topic:

```bash
ros2 topic echo /imu
```

You should see a continuous stream of IMU messages, indicating successful integration between Gazebo and ROS 2.

## Summary

In this chapter, you successfully installed Gazebo Garden and the `ros_gz` bridge, integrating it with your existing ROS 2 Humble environment. You verified the setup by launching a simulated world and confirming the communication between Gazebo and ROS 2 via bridged topics. This foundation is critical for developing and testing complex digital twin simulations.

## Review Questions

1.  What is the primary purpose of Gazebo in a robotics development workflow?
2.  Which version of Gazebo is recommended for ROS 2 Humble, and why?
3.  Explain the role of the `ros_gz` bridge. Why is it necessary for ROS 2 and Gazebo to communicate?
4.  List the `apt` commands required to install Gazebo Garden.
5.  How can you verify that your `ros_gz` bridge is functioning correctly after installation?
6.  Describe the expected output when echoing a Gazebo-bridged ROS 2 topic.