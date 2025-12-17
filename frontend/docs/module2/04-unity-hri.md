# Unity for Robot Visualization and Human-Robot Interaction

Unity is a powerful platform for creating interactive 3D environments, making it ideal for visualizing robot digital twins and developing intuitive human-robot interfaces (HRI). This chapter guides you through using Unity for robot visualization and implementing basic HRI, specifically focusing on how to integrate with ROS 2 for sending commands.

## Learning Objectives

After completing this chapter, you will be able to:

-   Set up a Unity project for robot visualization.
-   Import and display a robot model in Unity.
-   Implement basic human-robot interaction using Unity's input system.
-   Integrate Unity controls with ROS 2 to command a simulated robot.

## 1.1 Unity Project Setup for Robotics

This section builds upon the Unity installation from `00-setup-unity.md`.

### Step 1: Create or Use an Existing Unity Project

For this module, we'll assume you have a Unity project set up as described in `00-setup-unity.md`. If not, create a new 3D project in your Unity Hub.

**Path**: Your Unity project should be saved within `frontend/src/unity_examples/UnityProject/`. This path is provided as a reference to keep the book's examples organized.

### Step 2: Import Robot Model

To visualize a robot in Unity, you need to import its 3D model. We can use the `basic_robot` model defined previously, or a placeholder.

1.  **Obtain 3D Model**:
    *   If your robot is defined in URDF/SDF, you can use tools (e.g., `urdf_to_collada` package in ROS, or Blender plugins) to convert the visual meshes (typically `.dae`, `.stl`, `.obj`, `.fbx`) into a format Unity understands.
    *   For simplicity, you can also use primitive Unity shapes (cubes, spheres) or import a simple `.fbx` model.

2.  **Import into Unity**:
    *   Drag and drop your 3D model files (e.g., `basic_robot.fbx`) into your Unity project's `Assets` folder (e.g., `Assets/Models/`).
    *   Drag the imported model from the `Assets` panel into your Scene Hierarchy.
    *   Adjust its position, rotation, and scale as needed.
    *   Create a simple scene with a ground plane and appropriate lighting.

## 1.2 Robot Model Visualization

Once your robot model is imported, you can customize its visualization:

-   **Materials**: Apply PBR (Physically Based Rendering) materials to give your robot realistic textures and colors.
-   **Lighting**: Use Unity's lighting system (Directional Light, Point Lights, Spot Lights) to illuminate your robot.
-   **Cameras**: Configure the main camera to provide optimal views of your robot.

## 1.3 Human-Robot Interaction (HRI) via ROS 2

We will create a C# script in Unity to capture user input (e.g., keyboard presses) and then publish these commands to ROS 2 topics. A ROS 2 node can then subscribe to these topics to control a simulated robot (e.g., in Gazebo).

### Step 1: Ensure ROS-Unity Integration

Make sure you have followed the `ROS-Unity Integration` steps in `00-setup-unity.md`, especially installing `ROS-TCP-Connector` in Unity and `ros_tcp_endpoint` in ROS 2.

### Step 2: Create C# Teleoperation Script

1.  In the Unity Editor, create a new C# script. Navigate to `Assets/Scripts` (create if it doesn't exist). Right-click in the `Project` window -> `Create` -> `C# Script` and name it `RobotTeleop.cs`.
2.  Open `RobotTeleop.cs` and replace its content with the following:

```csharp
using UnityEngine;
using Unity.Robotics.ROSTCPConnector; // Required for ROS 2 communication
using RosMessageTypes.Geometry; // For Twist message type

public class RobotTeleop : MonoBehaviour
{
    // ROS Connector
    private ROSConnection ros;

    // ROS 2 Topic for command velocity
    public string topicName = "/cmd_vel"; // Default topic name
    public float linearSpeed = 0.5f; // m/s
    public float angularSpeed = 0.5f; // rad/s

    void Start()
    {
        // Get the ROSConnection instance
        ros = ROSConnection.instance;
        // Register the publisher for cmd_vel
        ros.RegisterPublisher<TwistMsg>(topicName);
    }

    void Update()
    {
        float linearX = 0f;
        float angularZ = 0f;

        // --- Keyboard Input ---
        if (Input.GetKey(KeyCode.W)) // Forward
        {
            linearX = linearSpeed;
        }
        else if (Input.GetKey(KeyCode.S)) // Backward
        {
            linearX = -linearSpeed;
        }

        if (Input.GetKey(KeyCode.A)) // Turn Left
        {
            angularZ = angularSpeed;
        }
        else if (Input.GetKey(KeyCode.D)) // Turn Right
        {
            angularZ = -angularSpeed;
        }
        // --- End Keyboard Input ---

        // Create a Twist message
        TwistMsg twistMessage = new TwistMsg
        {
            linear = new Vector3Msg(linearX, 0.0, 0.0),
            angular = new Vector3Msg(0.0, 0.0, angularZ)
        };

        // Publish the message to the /cmd_vel topic
        ros.Publish(topicName, twistMessage);
    }
}
```

### Step 3: Attach Script and Configure

1.  In your Unity Scene, select an empty GameObject (or create one: `GameObject` -> `Create Empty`). Rename it to `ROS2Commander`.
2.  Drag and drop the `RobotTeleop.cs` script from your `Assets/Scripts` folder onto the `ROS2Commander` GameObject in the Hierarchy.
3.  In the Inspector window for `ROS2Commander`, you can adjust the `Topic Name`, `Linear Speed`, and `Angular Speed` parameters.

## 1.4 Running the HRI Example

To see your Unity teleoperation in action, you'll need:

1.  **ROS 2 `ros_tcp_endpoint` running**: On your ROS 2 machine, start the endpoint:
    ```bash
    source /opt/ros/humble/setup.bash
    ros2 run ros_tcp_endpoint default_server_endpoint
    ```
2.  **Simulated Robot (e.g., in Gazebo) running**: Ensure you have a simulated robot that subscribes to `/cmd_vel` (e.g., a differential drive robot in Gazebo with `diff_drive_controller` and `ros_gz_ros2_control` or similar plugins). You can use the `basic_robot` from `03-gazebo-digital-twin.md` if modified to accept `cmd_vel`.

3.  **Run Unity Scene**: In the Unity Editor, press the **Play** button.

Now, pressing 'W', 'A', 'S', 'D' keys in Unity should publish `Twist` messages to the `/cmd_vel` topic in ROS 2, which your simulated robot can then use for movement. You can verify this by running `ros2 topic echo /cmd_vel` in a ROS 2 terminal.

## Summary

This chapter demonstrated how to use Unity for robot visualization and implement basic human-robot interaction. You learned how to set up your Unity project, import a robot model, and create a C# script to send teleoperation commands to ROS 2 topics via the `ROS-TCP-Connector`. This integration enables rich, interactive control interfaces for your robotic systems.

## Review Questions

1.  What is the main advantage of using Unity for robot visualization compared to a purely command-line simulator?
2.  Describe the steps to import a 3D robot model into a Unity project.
3.  Explain how the `RobotTeleop.cs` script uses Unity's input system to generate commands.
4.  Which ROS 2 message type is commonly used for sending velocity commands to robots?
5.  What is the role of `ROSConnection.instance.RegisterPublisher<TwistMsg>(topicName)` in the Unity script?
6.  How would you verify that your Unity teleoperation commands are being received by ROS 2?