# Nav2 for Humanoids with Isaac Sim and VSLAM

This chapter explores how to integrate the ROS 2 Navigation Stack (Nav2) with Isaac Sim for autonomous navigation of humanoid robots, utilizing Visual SLAM (VSLAM) for localization. Navigating complex humanoid robots autonomously in dynamic environments presents unique challenges that can be effectively addressed through advanced simulation and perception techniques.

## Learning Objectives

After completing this chapter, you will be able to:

-   Set up an Isaac Sim environment with a humanoid robot and a navigation-ready scene.
-   Integrate Visual SLAM (VSLAM) using Isaac ROS for robot localization.
-   Configure the ROS 2 Navigation Stack (Nav2) for humanoid robots.
-   Perform autonomous navigation of a humanoid robot in Isaac Sim using Nav2 and VSLAM.

## 1.1 Isaac Sim Environment for Humanoid Navigation

First, we need an Isaac Sim environment that includes a humanoid robot and a suitable navigation area.

### Conceptual Isaac Sim Script (`humanoid_nav_env.py`)

Create a file named `humanoid_nav_env.py` in `frontend/src/isaac_sim_examples/`:

```python
# humanoid_nav_env.py
import omni.usd
from pxr import Usd, UsdGeom, Gf, Sdf
from omni.isaac.core import World
from omni.isaac.core.robots import Robot
from omni.isaac.core.objects import DynamicCuboid
from omni.isaac.ros2_bridge import ROS2Base
from omni.isaac.sensor import Camera, LidarRtx

import asyncio
import os
import numpy as np

# Initialize the world
world = World(stage_units_in_meters=1.0)
world.scene.add_default_ground_plane()

# Add a simple environment
def add_environment():
    # Walls
    world.scene.add(DynamicCuboid(prim_path="/World/Wall1", name="wall1", position=Gf.Vec3f(0, 2, 0.5), scale=Gf.Vec3f(4, 0.1, 1), color=Gf.Vec3f(0.5, 0.5, 0.5)))
    world.scene.add(DynamicCuboid(prim_path="/World/Wall2", name="wall2", position=Gf.Vec3f(0, -2, 0.5), scale=Gf.Vec3f(4, 0.1, 1), color=Gf.Vec3f(0.5, 0.5, 0.5)))
    world.scene.add(DynamicCuboid(prim_path="/World/Wall3", name="wall3", position=Gf.Vec3f(2, 0, 0.5), scale=Gf.Vec3f(0.1, 4, 1), color=Gf.Vec3f(0.5, 0.5, 0.5)))
    world.scene.add(DynamicCuboid(prim_path="/World/Wall4", name="wall4", position=Gf.Vec3f(-2, 0, 0.5), scale=Gf.Vec3f(0.1, 4, 1), color=Gf.Vec3f(0.5, 0.5, 0.5)))
    
    # Obstacles
    world.scene.add(DynamicCuboid(prim_path="/World/Obstacle1", name="obstacle1", position=Gf.Vec3f(1, 1, 0.25), scale=Gf.Vec3f(0.5, 0.5, 0.5), color=Gf.Vec3f(0.8, 0.8, 0.2)))
    world.scene.add(DynamicCuboid(prim_path="/World/Obstacle2", name="obstacle2", position=Gf.Vec3f(-1, -1, 0.25), scale=Gf.Vec3f(0.5, 0.5, 0.5), color=Gf.Vec3f(0.2, 0.8, 0.8)))

add_environment()

# Add a humanoid robot (assuming a pre-built USD asset exists or is imported)
# For simplicity, let's assume we are loading a humanoid model from Isaac Sim assets
assets_root_path = get_assets_root_path()
humanoid_path = assets_root_path + "/Isaac/Robots/Humanoid/franka_emika_panda.usd" # Replace with actual humanoid USD if available

humanoid_robot = world.scene.add(
    Robot(
        prim_path="/World/HumanoidRobot",
        name="my_humanoid",
        usd_path=humanoid_path,
        position=Gf.Vec3f(0.0, 0.0, 0.1), # Adjust height as needed
        orientation=Gf.Quatf(1.0, 0, 0, 0)
    )
)

# Add sensors to the humanoid for navigation (LiDAR and RGB-D Camera)
# Add a LiDAR sensor
lidar_prim_path = "/World/HumanoidRobot/Lidar" # Attach to a link of the humanoid
lidar = world.scene.add(
    LidarRtx(
        prim_path=lidar_prim_path,
        name="humanoid_lidar",
        position=Gf.Vec3f(0.1, 0, 0.5), # Relative to humanoid base
        orientation=Gf.Quatf(1.0, 0, 0, 0),
        rotation_rate=20, # Hz
        draw_points=False,
        draw_lines=True,
        min_range=0.1,
        max_range=20.0,
        horizontal_fov=360.0,
        vertical_fov=30.0,
        horizontal_resolution=0.4,
        vertical_resolution=1.0,
        high_lod=True,
        origin=Gf.Vec3f(0.0, 0.0, 0.0),
        ros_topic_name="scan"
    )
)

# Add an RGB-D Camera
camera_prim_path = "/World/HumanoidRobot/Camera"
camera = world.scene.add(
    Camera(
        prim_path=camera_prim_path,
        name="humanoid_camera",
        position=Gf.Vec3f(0.1, 0, 0.6), # Relative to humanoid base
        orientation=Gf.Quatf(0.7071068, 0, 0.7071068, 0), # Pointing slightly down
        resolution=(640, 480),
        fov=90.0,
        set_params=Camera.Params(trigger_type="automatic")
    )
)
camera.add_ros_interface(
    name="rgbd_camera_ros_interface",
    frame_id="humanoid_camera_link",
    topic_name="rgbd_camera",
    image_pub_enabled=True,
    depth_pub_enabled=True,
    camera_info_pub_enabled=True,
    point_cloud_pub_enabled=True # For VSLAM input
)

# Enable ROS 2 Bridge
ros2_bridge = world.add_asset(ROS2Base(prim_path="/ROS2_Bridge"))


# Reset and play the simulation
world.reset()
world.play()

async def run_sim():
    while True:
        await omni.usd.get_context().step_async(0.0)

asyncio.ensure_future(run_sim())
```

### How to Run `humanoid_nav_env.py` in Isaac Sim

1.  **Launch Isaac Sim** from the Omniverse Launcher.
2.  Go to `Window` -> `Script Editor`.
3.  In the Script Editor, open `humanoid_nav_env.py` (located at `frontend/src/isaac_sim_examples/`).
4.  Click the **Play** button (`>` icon) in the Script Editor. You should see your humanoid robot in an environment with walls and obstacles, and ROS 2 topics for LiDAR and camera being published.

## 1.2 VSLAM Integration with Isaac ROS

VSLAM is crucial for a robot to localize itself and build a map of its surroundings. We will use `isaac_ros_visual_slam` for this.

### Step 1: VSLAM Configuration (`frontend/src/isaac_ros_examples/vslam_config/vslam_params.yaml`)

Create a directory `frontend/src/isaac_ros_examples/vslam_config/` and then `vslam_params.yaml` inside it:

```yaml
# vslam_params.yaml
# Parameters for isaac_ros_visual_slam node
visual_slam_node:
  ros__parameters:
    denoise_input_images: False
    enable_localization_n_mapping: True # Enable both mapping and localization
    enable_slam_visualization: False
    enable_debug_mode: False
    map_frame: "map"
    odom_frame: "odom"
    base_frame: "humanoid_base_link" # Adjust to your humanoid's base frame
    enable_imu_fusion: False # Only use visual odometry for now
    # Camera parameters - adjust based on your Isaac Sim camera
    camera_frame: "humanoid_camera_link"
    # Isaac Sim cameras typically publish rectified images already, so disable rectification
    enable_rectified_pose: True 
    image_topic: "/rgbd_camera/rgb/image_raw"
    depth_topic: "/rgbd_camera/depth/image_raw"
    camera_info_topic: "/rgbd_camera/camera_info"
    # Other parameters as needed for specific VSLAM tuning
```

### Step 2: VSLAM Launch File (`frontend/src/isaac_ros_examples/vslam.launch.py`)

Create `vslam.launch.py` in `frontend/src/isaac_ros_examples/`:

```python
# vslam.launch.py
import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    vslam_params_path = os.path.join(
        get_package_share_directory('isaac_ros_examples'), # Assuming this is in an example package
        'vslam_config',
        'vslam_params.yaml'
    )

    visual_slam_node = Node(
        package='isaac_ros_visual_slam',
        executable='isaac_ros_visual_slam_node',
        name='visual_slam_node',
        namespace='humanoid_robot', # Namespace for the humanoid
        parameters=[vslam_params_path],
        remappings=[
            ('image', '/rgbd_camera/rgb/image_raw'),
            ('depth_image', '/rgbd_camera/depth/image_raw'),
            ('camera_info', '/rgbd_camera/camera_info'),
            ('odom', 'odom'),
            ('pose', 'pose'),
            ('tf_static', 'tf_static')
        ],
        output='screen',
        arguments=['--ros-args', '--log-level', 'INFO']
    )

    return LaunchDescription([
        visual_slam_node
    ])
```

## 1.3 Nav2 Setup for Humanoid Robots

Nav2 requires a map, localization, and configuration for its planners and controllers. Humanoid navigation is complex due to non-holonomic movement and dynamic balance.

### Step 1: Nav2 Configuration (`frontend/src/isaac_ros_examples/nav2_setup/nav2_params.yaml`)

Create `frontend/src/isaac_ros_examples/nav2_setup/` and then `nav2_params.yaml` inside it:

```yaml
# nav2_params.yaml
# Basic Nav2 parameters for a humanoid, often requires significant tuning
# This is a simplified example; full Nav2 config is extensive.
amcl:
  ros__parameters:
    use_sim_time: True
    set_initial_pose: True
    initial_pose: [0.0, 0.0, 0.0] # Initial pose estimate
    # Other AMCL parameters for particle filter localization

bt_navigator:
  ros__parameters:
    use_sim_time: True
    # behavior_tree: "path/to/your/custom_humanoid_behavior_tree.xml" # Custom BT for humanoids
    # Default behavior tree will work for simple cases

controller_server:
  ros__parameters:
    use_sim_time: True
    min_x_velocity_threshold: 0.001
    min_y_velocity_threshold: 0.001
    min_theta_velocity_threshold: 0.001
    # Replace default controller with one suitable for humanoid (e.g., TEB Local Planner)
    controller_plugin_ids: ["SimpleController"] # Placeholder
    controller_plugin_types: ["nav2_controller::SimpleController"] # Placeholder
    # Need to tune parameters for humanoid locomotion (e.g., foot placement, balance)

planner_server:
  ros__parameters:
    use_sim_time: True
    planner_plugin_ids: ["GridBased"]
    planner_plugin_types: ["nav2_planner::GridBased"]
    # Adjust global planner settings

recovery_server:
  ros__parameters:
    use_sim_time: True
    # Recovery behaviors for humanoids (e.g., stand up, re-plan)

# Costmap parameters
local_costmap:
  local_costmap:
    ros__parameters:
      # ... map parameters ...
      global_frame: map
      robot_base_frame: humanoid_base_link # Your humanoid's base frame
      update_frequency: 5.0
      publish_frequency: 2.0
      resolution: 0.05
      plugins: ["obstacle_layer", "inflation_layer"] # Typical layers

global_costmap:
  global_costmap:
    ros__parameters:
      # ... map parameters ...
      global_frame: map
      robot_base_frame: humanoid_base_link
      update_frequency: 1.0
      publish_frequency: 1.0
      resolution: 0.05
      plugins: ["static_layer", "obstacle_layer", "inflation_layer"] # Typical layers
```

### Step 2: Nav2 Launch File (`frontend/src/isaac_ros_examples/nav2_setup/humanoid_nav2_bringup.launch.py`)

Create `humanoid_nav2_bringup.launch.py` in `frontend/src/isaac_ros_examples/nav2_setup/`:

```python
# humanoid_nav2_bringup.launch.py
import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node

def generate_launch_description():
    # Paths to your config files
    nav2_params_path = os.path.join(
        get_package_share_directory('isaac_ros_examples'), # Your package name
        'nav2_setup',
        'nav2_params.yaml'
    )
    
    # Nav2 bringup launch file
    nav2_bringup_dir = get_package_share_directory('nav2_bringup')
    nav2_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([nav2_bringup_dir, '/launch/bringup_launch.py']),
        launch_arguments={
            'map': '', # VSLAM will provide map, or use a static map here
            'use_sim_time': 'true',
            'params_file': nav2_params_path,
            'autostart': 'true',
            'default_bt_xml_path': os.path.join(
                get_package_share_directory('nav2_bt_navigator'),
                'behavior_trees', 'navigate_w_replanning_and_recovery.xml'), # Default BT
            'robot_base_frame': 'humanoid_base_link',
            'odom_frame': 'odom',
        }.items(),
    )
    
    # Map server to serve the map generated by VSLAM
    map_server_node = Node(
        package='nav2_map_server',
        executable='map_server',
        output='screen',
        parameters=[{'yaml_filename': '/path/to/your/static_map.yaml'}], # If you use a static map
        remappings=[('/map', '/map')]
    )

    # Replace with your own robot's state publisher if needed
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': LaunchConfiguration('robot_description_content')}]
    )

    return LaunchDescription([
        # Add a DeclareLaunchArgument for robot_description_content if using it
        # DeclareLaunchArgument(
        #     'robot_description_content',
        #     default_value=robot_description_content, # Your robot URDF/Xacro
        #     description='Robot description content'
        # ),
        nav2_launch,
        # map_server_node, # Uncomment if using a static map and not VSLAM's map
        # robot_state_publisher_node, # Uncomment if you have your own
    ])
```

## 1.4 Running the Nav2 Demo for Humanoids

### Step 1: Start Isaac Sim with Humanoid Environment

1.  Launch Isaac Sim.
2.  Run `humanoid_nav_env.py` (from `frontend/src/isaac_sim_examples/`) in the Script Editor. This sets up the robot, sensors, and environment.

### Step 2: Launch Isaac ROS VSLAM

1.  Open an Isaac ROS Docker container (as per `00-setup-isaac.md`).
2.  Inside the container, source your workspace and launch the VSLAM node:
    ```bash
    ros2 launch isaac_ros_examples vslam.launch.py
    ```
    This will start building a map and providing localization (`/map`, `/tf`).

### Step 3: Launch Nav2 Stack

1.  Open another Isaac ROS Docker container.
2.  Inside the container, source your workspace and launch Nav2:
    ```bash
    ros2 launch isaac_ros_examples nav2_setup/humanoid_nav2_bringup.launch.py
    ```
    This will bring up all Nav2 components, relying on VSLAM for map and pose.

### Step 4: Visualize and Navigate with RViz2

1.  Open a new terminal (either on host or another container) and launch RViz2:
    ```bash
    ros2 run rviz2 rviz2
    ```
2.  **Configure RViz2**:
    *   Set `Fixed Frame` to `map`.
    *   Add `RobotModel`, `Map`, `Amcl (PoseArray)`, `Path`, `GlobalPlan`, `LocalPlan`, `Goal` displays.
    *   Add `TF` to see the robot's pose.
    *   Use `2D Pose Estimate` to set the initial pose of your robot on the map.
    *   Use `2D Nav Goal` to send navigation goals to your humanoid robot.

Observe your humanoid robot autonomously moving through the Isaac Sim environment, avoiding obstacles, and reaching its goals.

## Summary

This chapter provided a comprehensive guide to integrating the ROS 2 Navigation Stack (Nav2) with Isaac Sim for autonomous navigation of humanoid robots using Visual SLAM (VSLAM). You learned how to set up a navigation-ready Isaac Sim environment, integrate Isaac ROS VSLAM for localization and mapping, and configure Nav2 for a humanoid robot. This advanced integration enables the development and testing of complex AI-driven navigation behaviors for bipedal systems in high-fidelity simulations.

## Review Questions

1.  What unique challenges does navigating a humanoid robot present for Nav2 compared to a wheeled robot?
2.  How does the `humanoid_nav_env.py` script contribute to setting up the navigation scenario in Isaac Sim?
3.  Which Isaac ROS module is used for VSLAM in this chapter, and what is its primary output?
4.  Why is a custom `nav2_params.yaml` often necessary when configuring Nav2 for a humanoid robot?
5.  Describe the sequence of launching Isaac Sim, VSLAM, and Nav2 to achieve autonomous navigation.
6.  How do you send a navigation goal to the humanoid robot in RViz2, and what are the expected visual cues?