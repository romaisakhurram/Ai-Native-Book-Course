# Setting up Unity for Robotics

Unity provides a powerful platform for 3D visualization, realistic simulation, and developing interactive Human-Robot Interaction (HRI) applications. This chapter guides you through setting up Unity for robotics development, focusing on its integration with ROS 2.

## Learning Objectives

After completing this chapter, you will be able to:

-   Install Unity Hub and a compatible Unity Editor version.
-   Integrate the Unity Robotics Hub packages (ROS-TCP-Connector) into a Unity project.
-   Understand the basic setup for ROS 2 and Unity communication.
-   Verify your Unity and ROS 2 integration using a simple example.

## 1.1 Unity Hub and Editor Installation

### Step 1: Install Unity Hub

Unity Hub is a management tool for your Unity projects and Editor versions.
1.  Download and install [Unity Hub](https://unity.com/download) for your operating system. Follow the on-screen instructions.

### Step 2: Install Unity Editor

For robotics development, it's recommended to use a recent LTS (Long Term Support) version of the Unity Editor due to its stability and extended support.

1.  Open **Unity Hub**.
2.  Navigate to the **Installs** tab.
3.  Click **Install Editor**.
4.  Select a **Unity 2022 LTS** version (e.g., 2022.3.x LTS). This version is generally well-supported by the Unity Robotics Hub packages.
5.  Ensure you include the **Linux Build Support (Mono)** and **Windows Build Support (Mono)** modules during installation if you plan to build applications for these platforms.
6.  Click **Install**. This process may take some time.

:::tip
Always use a compatible Unity Editor version with the ROS-Unity Integration package you plan to use. Check the Unity Robotics Hub GitHub page for version compatibility.
:::

## 1.2 ROS-Unity Integration: Unity Robotics Hub

Unity can communicate with ROS 2 through the `Unity Robotics Hub` project, which provides a suite of tools including the `ROS-TCP-Connector` for establishing a TCP/IP connection between Unity and ROS 2.

### Step 1: Prepare your Unity Project

You can either create a new Unity project or use an existing one. For this guide, let's assume a new 3D project.

1.  In Unity Hub, create a **New Project**.
2.  Select the **3D Core** template.
3.  Choose your installed Unity 2022 LTS Editor version.
4.  Give your project a name (e.g., `ROS2UnityProject`) and click **Create Project**.

### Step 2: Import the `Unity-Robotics-Hub` Package

The `Unity-Robotics-Hub` repository contains the `ROS-TCP-Connector` and example projects.

1.  **Clone the Repository**: Open a terminal and clone the repository to your local machine:
    ```bash
    git clone https://github.com/Unity-Technologies/Unity-Robotics-Hub.git
    ```
2.  **Import `ROS-TCP-Connector`**:
    *   Open your Unity project (e.g., `ROS2UnityProject`) in the Unity Editor.
    *   In the Unity Editor, go to `Assets` > `Import Package` > `Custom Package...`
    *   Navigate to the cloned `Unity-Robotics-Hub` directory.
    *   Find the `UnityProject/Assets/ROS-TCP-Connector` folder and select the `ROS-TCP-Connector.unitypackage` file (or the latest version available).
    *   Click `Open`, then `Import` all items when prompted.

:::info
Alternatively, you can use the Unity Package Manager (`Window > Package Manager`) and add the package via a Git URL, if the repository supports it for the specific package version.
:::

### Step 3: Install `ROS-TCP-Endpoint` (ROS 2 side)

On your ROS 2 machine (typically your Ubuntu setup), you need to install the `ros_tcp_endpoint` package, which acts as the server to which Unity connects.

1.  Ensure your ROS 2 environment is sourced.
2.  Install the package:
    ```bash
    sudo apt install ros-humble-ros-tcp-endpoint
    ```

## 1.3 Verifying Your Setup

To ensure proper communication between Unity and ROS 2, let's run a simple test.

### Step 1: Start `ROS-TCP-Endpoint` in ROS 2

Open a terminal on your ROS 2 machine and launch the endpoint:

```bash
source /opt/ros/humble/setup.bash
ros2 run ros_tcp_endpoint default_server_endpoint
```

You should see messages indicating that the TCP endpoint server has started and is listening for connections.

### Step 2: Connect from Unity

1.  In your Unity project, open a sample scene that uses the `ROS-TCP-Connector`. The `Unity-Robotics-Hub` repository provides example scenes (e.g., in `UnityProject/Assets/ROS-TCP-Connector/RosPublisherExample/Scenes/RosPublisherExample.unity`).
2.  Ensure you have a GameObject with the `ROSConnection` component. You might need to add one (`GameObject > Create Empty`, then `Add Component > ROSConnection`). Configure its `Ros IP Address` to your ROS 2 machine's IP address (if running on a different machine) or `127.0.0.1` (if on the same machine).
3.  Press the **Play** button in the Unity Editor.

### Expected Outcome:

-   In your ROS 2 terminal, the `ros_tcp_endpoint` should show a message indicating a new connection from Unity.
-   In Unity, if you're running an example publisher scene, you should see messages being published.
-   You can verify ROS 2 messages from Unity using `ros2 topic list` and `ros2 topic echo <topic_name>` in another ROS 2 terminal.

## Summary

This chapter walked you through the process of setting up Unity for robotics development, including installing Unity Hub and a compatible Editor, integrating the Unity Robotics Hub packages, and installing the `ROS-TCP-Endpoint` in your ROS 2 environment. You also verified the successful communication between Unity and ROS 2 using a basic example. This integration lays the groundwork for creating rich 3D simulations and intuitive HRI experiences.

## Review Questions

1.  Why is a recent LTS version of the Unity Editor recommended for robotics development?
2.  What is the primary role of the `ROS-TCP-Connector` in Unity Robotics Hub?
3.  Which ROS 2 package acts as the server for the Unity `ROS-TCP-Connector`?
4.  List the key steps to import the `ROS-TCP-Connector` into a Unity project.
5.  How would you configure `ROSConnection` in Unity to communicate with a ROS 2 endpoint running on a different machine?
6.  Describe how you would verify a successful connection and message exchange between a Unity publisher and ROS 2.