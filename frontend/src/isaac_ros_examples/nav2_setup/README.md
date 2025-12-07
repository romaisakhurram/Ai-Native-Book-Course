# ROS 2/Nav2 Setup for Humanoid Navigation - Manual Setup

This directory is intended to contain launch files and configuration for setting up basic autonomous navigation using the ROS 2 Navigation Stack (Nav2) with a humanoid robot. Nav2 requires detailed knowledge of the robot's kinematics, sensor configurations, and a map of the environment.

## Steps for Setup:

1.  **Ensure ROS 2 and Nav2 Environment**: Verify you have a correctly set up ROS 2 environment with Nav2 installed.
2.  **Refer to Nav2 Documentation**: Consult the official [Nav2 Documentation](https://navigation.ros.org/documentation/index.html) for detailed instructions.
3.  **Prepare Robot URDF/Description**: Ensure your humanoid robot has a complete URDF/XACRO description with all relevant links, joints, and sensor definitions.
4.  **Create Map**: Generate a map of your environment (e.g., using SLAM tools).
5.  **Create Nav2 Configuration Files**: You will need to create and configure YAML files for:
    *   **Planner parameters**: e.g., `planner_server.yaml`
    *   **Controller parameters**: e.g., `controller_server.yaml`
    *   **Behavior Tree parameters**: e.g., `bt_navigator.yaml`
    *   **Filter mask parameters**: e.g., `filters.yaml`
6.  **Create Nav2 Launch File**: A ROS 2 launch file will orchestrate all the necessary nodes (map server, AMCL/localization, planner server, controller server, etc.) for navigation.

## Example Nav2 Launch File (Conceptual)

```python
import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, ThisLaunchFileDir
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # Declare arguments
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    map_yaml_file = LaunchConfiguration('map', default=os.path.join(
        get_package_share_directory('nav2_bringup'), 'maps', 'turtlebot3_world.yaml'))
    params_file = LaunchConfiguration('params_file', default=os.path.join(
        get_package_share_directory('nav2_bringup'), 'params', 'nav2_params.yaml')) # Placeholder

    # Robot state publisher node
    robot_state_publisher_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('nav2_bringup'), 'launch', 'tb3_rsp_launch.py')), # Placeholder
        launch_arguments={'use_sim_time': use_sim_time}.items()
    )

    # Nav2 bringup
    nav2_bringup_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('nav2_bringup'), 'launch', 'navigation_launch.py')),
        launch_arguments={
            'map': map_yaml_file,
            'use_sim_time': use_sim_time,
            'params_file': params_file}.items()
    )

    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='true', description='Use simulation (Gazebo) clock if true'),
        DeclareLaunchArgument('map', default_value=map_yaml_file, description='Full path to map yaml file to load'),
        DeclareLaunchArgument('params_file', default_value=params_file, description='Full path to param file to load'),
        robot_state_publisher_cmd,
        nav2_bringup_cmd
    ])
```

This conceptual example shows how Nav2 might be launched. Actual implementation details depend on the specific robot, sensors, and environment setup.
