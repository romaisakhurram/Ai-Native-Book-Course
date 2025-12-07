# Unity Project Setup - Manual Steps

This directory is intended to hold a Unity project for robot visualization and human-robot interaction. Setting up a Unity project and importing a robot model requires manual steps within the Unity Editor.

## Steps:

1.  **Open Unity Hub**: Launch Unity Hub and create a new 3D project.
2.  **Save Project**: Save the new Unity project into this `frontend/src/unity_examples/UnityProject/` directory.
3.  **Import Robot Model**:
    *   You can export your `basic_robot` from Gazebo as a mesh (e.g., `.dae` or `.stl`) or manually create a simplified model in Unity.
    *   Import the robot model into your Unity project (e.g., drag and drop into the `Assets` folder).
4.  **Configure Model**: Adjust the model's scale, materials, and add colliders as needed in Unity.

Once these steps are completed, you will have a basic Unity project with a robot model ready for scripting.
