# Unity for Robot Visualization and Human-Robot Interaction

Unity is a powerful platform for creating interactive 3D environments, making it ideal for visualizing robot digital twins and developing intuitive human-robot interfaces.

## Unity Project Setup

Setting up a Unity project for robotics involves several manual steps within the Unity Editor.

1.  **Create a New Unity Project**:
    *   Open Unity Hub.
    *   Create a new 3D project, and save it to `frontend/src/unity_examples/UnityProject/`.
    *   Refer to the `README.md` in `frontend/src/unity_examples/UnityProject/` for detailed manual steps.

2.  **Import Robot Model**:
    *   You can import a robot model, for instance, by exporting your `basic_robot` from Gazebo (e.g., as a `.dae` or `.stl` file) or by creating a simplified model directly in Unity.
    *   Import this model into your Unity project's `Assets` folder.
    *   Refer to the `README.md` in `frontend/src/unity_examples/UnityProject/` for more details.

## Robot Model Visualization

Once your robot model is imported into Unity, you can place it in your scene and configure its visual properties, materials, and lighting to create a compelling visualization.

## Human-Robot Interaction (HRI) Scripts

To enable human interaction with your robot model, you'll create C# scripts within Unity. These scripts will handle user input (e.g., keyboard commands) and translate them into actions for the robot, such as controlling joint movements.

1.  **Create C# Script**:
    *   In the Unity Editor, navigate to the `Assets/Scripts` folder (located at `frontend/src/unity_examples/UnityProject/Assets/Scripts/`).
    *   Create a new C# script (e.g., `TeleopController.cs`).
    *   Refer to the `README.md` in `frontend/src/unity_examples/UnityProject/Assets/Scripts/` for example script logic and manual steps.

2.  **Implement Control Logic**:
    *   The C# script will typically use Unity's `Input` class to detect keyboard presses or other input devices.
    *   It will then apply transformations or invoke methods on your robot model's components (e.g., rotating a joint GameObject).

### Example: Basic Keyboard Teleoperation

```csharp
using UnityEngine;

public class TeleopController : MonoBehaviour
{
    public float rotationSpeed = 50.0f;
    public GameObject robotJoint; // Assign your robot joint GameObject in the Inspector

    void Update()
    {
        if (robotJoint == null)
        {
            Debug.LogError("Robot Joint not assigned!");
            return;
        }

        // Example: Rotate joint based on horizontal input
        float rotationInput = Input.GetAxis("Horizontal");
        robotJoint.transform.Rotate(Vector3.up, rotationInput * rotationSpeed * Time.deltaTime);

        // Add more complex controls as needed
    }
}
```

This script, when attached to an appropriate GameObject (e.g., a central control object or the robot's base), would allow a user to control the `robotJoint` using the horizontal arrow keys.

## How to Proceed (Manual Steps)

To fully implement this section, you will need to:
1.  **Complete Unity Project Setup**: Follow the `README.md` instructions in `frontend/src/unity_examples/UnityProject/`.
2.  **Implement HRI Scripts**: Follow the `README.md` instructions in `frontend/src/unity_examples/UnityProject/Assets/Scripts/` to create and integrate your control scripts.
3.  **Test in Unity Editor**: Run your Unity scene and verify that human input correctly controls the robot model.
