# Creating a Basic Perception Pipeline with Isaac ROS

This chapter guides you through setting up a fundamental perception pipeline using NVIDIA Isaac ROS modules, and visualizing its output. We will focus on integrating Isaac Sim as the sensor data source and an Isaac ROS Docker container for processing the data.

## Learning Objectives

After completing this chapter, you will be able to:

-   Create a simple Isaac Sim environment with an RGB-D camera.
-   Understand how Isaac Sim publishes sensor data to ROS 2.
-   Integrate an Isaac ROS perception module (`isaac_ros_image_proc`) to process image data.
-   Visualize the output of a hardware-accelerated perception pipeline.

## 1.1 Isaac Sim Environment Setup: Simple Perception Scene

We will create a Python script to set up an Isaac Sim scene that publishes RGB and Depth images. This script will ensure our camera is correctly positioned and configured for ROS 2 output.

Create a file named `simple_perception_env.py` in `frontend/src/isaac_sim_examples/`:

```python
# simple_perception_env.py
import omni.usd
from pxr import Usd, UsdGeom, Gf, Sdf
from omni.isaac.core import World
from omni.isaac.core.objects import DynamicCuboid
from omni.isaac.core.utils.nucleus import get_assets_root_path
from omni.isaac.ros2_bridge import ROS2Base
from omni.isaac.sensor import Camera

import asyncio
import os

# Define the path to where the script is
ISAAC_SIM_EXAMPLES_DIR = os.path.dirname(os.path.abspath(__file__))

# Initialize the world
world = World(stage_units_in_meters=1.0)
world.scene.add_default_ground_plane()

# Add a simple cuboid object
cube = world.scene.add(
    DynamicCuboid(
        prim_path="/World/cube",
        name="cube",
        position=Gf.Vec3f(0.5, 0, 0.5),
        scale=Gf.Vec3f(0.2, 0.2, 0.2),
        color=Gf.Vec3f(0.8, 0.2, 0.2)
    )
)

# Add an RGB-D camera
camera_prim_path = "/World/Camera"
camera = world.scene.add(
    Camera(
        prim_path=camera_prim_path,
        name="my_camera",
        position=Gf.Vec3f(0, 0, 1.0), # Position above the cube
        orientation=Gf.Quatf(0.7071068, 0, 0.7071068, 0), # Pointing downwards
        resolution=(640, 480),
        fov=90.0,
        set_params=Camera.Params(
            trigger_type="automatic",
            horizontal_aperture=2.0955,
            vertical_aperture=1.571625
        )
    )
)

# Enable ROS 2 Bridge
ros2_bridge = world.add_asset(ROS2Base(prim_path="/ROS2_Bridge"))
camera.add_ros_interface(
    name="rgbd_camera_ros_interface",
    frame_id="camera_link",
    topic_name="rgbd_camera",
    # Specify output types
    image_pub_enabled=True,
    depth_pub_enabled=True,
    camera_info_pub_enabled=True,
    point_cloud_pub_enabled=False # Disable point cloud to simplify for now
)

# Reset and play the simulation
world.reset()
world.play()

# Keep the script running
async def run_sim():
    while True:
        await omni.usd.get_context().step_async(0.0)

asyncio.ensure_future(run_sim())
```

### How to Run `simple_perception_env.py` in Isaac Sim

1.  **Launch Isaac Sim** from the Omniverse Launcher.
2.  Go to `Window` -> `Script Editor`.
3.  In the Script Editor, open `simple_perception_env.py` (located at `frontend/src/isaac_sim_examples/`).
4.  Click the **Play** button (`>` icon) in the Script Editor. You should see a cube and a camera in the scene, and ROS 2 topics being published.

## 1.2 Isaac ROS Perception Module Integration: Image Processing

Now, we will integrate an Isaac ROS module to process the image data coming from Isaac Sim. We'll use `isaac_ros_image_proc` for basic image rectification/resize, which is often a preliminary step in perception pipelines.

Create a file named `perception_pipeline.launch.py` in `frontend/src/isaac_ros_examples/perception_pipeline/`:

```python
# perception_pipeline.launch.py
import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # Path to the Isaac ROS Image Proc config
    image_proc_share_dir = get_package_share_directory('isaac_ros_image_proc')
    image_proc_config_path = os.path.join(
        image_proc_share_dir, 'config', 'rgb_camera.yaml'
    )

    image_proc_node = Node(
        package='isaac_ros_image_proc',
        executable='image_proc_node',
        name='image_proc_node',
        namespace='rgbd_camera', # Use the camera's namespace
        parameters=[image_proc_config_path],
        remappings=[
            ('image_raw', '/rgbd_camera/rgb/image_raw'), # Input from Isaac Sim
            ('camera_info', '/rgbd_camera/camera_info'),
            ('image_rect', '/rgbd_camera/image_rect'), # Output rectified image
            ('image_rect_color', '/rgbd_camera/image_rect_color')
        ],
        output='screen'
    )

    return LaunchDescription([
        image_proc_node
    ])
```

## 1.3 Running the Perception Pipeline

Follow these steps to run the complete pipeline:

1.  **Start Isaac Sim with Environment Script**:
    *   Launch Isaac Sim.
    *   Open `simple_perception_env.py` in the Script Editor (from `frontend/src/isaac_sim_examples/`).
    *   Click the **Play** button in the Script Editor.

2.  **Launch Isaac ROS Perception Node**:
    *   Open a terminal on your host system and launch your Isaac ROS development container (as set up in `00-setup-isaac.md`).
    *   Inside the container, ensure your ROS 2 environment is sourced and your workspace is built.
    *   Navigate to your workspace (e.g., `cd ~/isaac_ros_ws`).
    *   Run the launch file:
        ```bash
        ros2 launch isaac_ros_examples_perception_pipeline perception_pipeline.launch.py
        # Assuming you created a package 'isaac_ros_examples_perception_pipeline'
        # with this launch file. Otherwise, adjust package name.
        ```
        You should see log messages indicating the `image_proc_node` has started.

3.  **Visualize the Output with RViz2**:
    *   Open a new terminal (either on host or another container, with ROS 2 sourced).
    *   Launch RViz2:
        ```bash
        ros2 run rviz2 rviz2
        ```
    *   In RViz2, add a new `Image` display.
    *   Set the `Topic` to `/rgbd_camera/image_rect_color`.
    *   You should see the rectified color image from Isaac Sim, processed by the Isaac ROS `image_proc_node`.

## Summary

This chapter guided you through creating a basic perception pipeline using Isaac Sim as a data source and `isaac_ros_image_proc` for hardware-accelerated image processing. You learned how to set up an Isaac Sim environment via Python scripting, integrate an Isaac ROS module using a launch file, and visualize the processed output in RViz2. This foundational pipeline demonstrates the power and efficiency of combining Isaac Sim and Isaac ROS for advanced robotics applications.

## Review Questions

1.  What is the primary purpose of the `simple_perception_env.py` script in this chapter?
2.  How does Isaac Sim publish sensor data to be consumed by ROS 2 nodes?
3.  Which Isaac ROS module was used in this chapter to process image data?
4.  Explain the role of the `remappings` in the `perception_pipeline.launch.py` file.
5.  What command would you use to visualize the processed image data from the pipeline in RViz2?
6.  How does the `namespace` parameter in the `image_proc_node` configuration contribute to organizing ROS 2 topics?