# Unity C# Scripts - Manual Steps

This directory is intended to hold C# scripts for controlling robot joints via human input (e.g., keyboard teleoperation) within a Unity project. Creating and integrating these scripts is best done within the Unity Editor.

## Steps:

1.  **Open Unity Project**: Open the Unity project located in `frontend/src/unity_examples/UnityProject/` in the Unity Editor.
2.  **Create C# Script**: In the `Assets/Scripts` folder within Unity, create a new C# script (e.g., `TeleopController.cs`).
3.  **Implement Logic**: Write C# code to:
    *   Detect human input (e.g., keyboard presses).
    *   Translate input into robot commands (e.g., joint angle changes).
    *   Apply these commands to the robot model in the Unity scene.

## Example TeleopController.cs (Conceptual)

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

Once the script is created and attached to a relevant GameObject in your scene, you will be able to control your robot model using human input.
