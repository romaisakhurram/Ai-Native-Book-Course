# Creating a Basic Perception Pipeline with Isaac ROS

This chapter guides you through setting up a fundamental perception pipeline using NVIDIA Isaac ROS modules, and visualizing its output within Isaac Sim.

## Isaac Sim Environment Setup

Setting up the Isaac Sim environment for perception involves creating a scene with a camera and objects. This is primarily done using Python scripting within the Isaac Sim Editor.

1.  **Create Isaac Sim Script**:
    *   Refer to the `simple_perception_env.py` in `frontend/src/isaac_sim_examples/` for a conceptual script.
    *   This script should create a ground plane, place a camera, and add a few objects that an Isaac ROS perception module can detect.
    *   Refer to the `README.md` in `frontend/src/isaac_sim_examples/` for manual steps on how to create and run this script within Isaac Sim.

### Conceptual Isaac Sim Script (`simple_perception_env.py`)

```python
import omni.usd
from pxr import Usd, UsdGeom, UsdPhysics, Gf, Sdf
# ... (rest of the Isaac Sim script as shown in T009)
```

## Isaac ROS Perception Module Integration

Once your Isaac Sim environment is set up to generate visual data (e.g., camera images), you can integrate an Isaac ROS perception module to process this data. This usually involves setting up a ROS 2 workspace, building Isaac ROS packages, and creating launch files to run the perception nodes.

1.  **Set up Isaac ROS Environment**: Ensure you have a working Isaac ROS development environment (Docker, NVIDIA GPU, ROS 2). Refer to `frontend/docs/module3/00-setup-isaac.md`.
2.  **Integrate Perception Module**:
    *   Choose a basic Isaac ROS perception module (e.g., `isaac_ros_stereo_image_proc` for depth estimation or a simple object detection module).
    *   Refer to the `README.md` in `frontend/src/isaac_ros_examples/perception_pipeline/` for guidance on setting up the module.
    *   Create a launch file to start the Isaac ROS node and configure its inputs (from Isaac Sim via ROS 2 bridge) and outputs.

### Conceptual Isaac ROS Launch File

```python
import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    # ... (rest of the Isaac ROS launch file as shown in T010)
    return ld
```

## How to Run the Perception Pipeline

1.  Launch your Isaac Sim environment with the `simple_perception_env.py` script. This will publish camera data as ROS 2 topics.
2.  In a separate terminal, launch your Isaac ROS perception module using its ROS 2 launch file. This will consume the camera data and publish processed perception results.
3.  Visualize the output (e.g., depth map, bounding boxes) using RViz2 or within Isaac Sim's built-in visualization tools if available.
