# Isaac ROS Perception Pipeline - Manual Setup

This directory is intended to contain configuration and launch files for a basic Isaac ROS perception module, such as `stereo_image_proc` or `object_detection`. Isaac ROS modules typically run within Docker containers and require a specialized development environment (NVIDIA GPU, specific Ubuntu version, ROS 2 installation).

## Steps for Setup:

1.  **Ensure Isaac ROS Environment**: Verify you have a correctly set up Isaac ROS development environment, including Docker and NVIDIA Container Toolkit.
2.  **Refer to Isaac ROS Documentation**: Consult the official [Isaac ROS Documentation](https://nvidia-isaac-ros.github.io/index.html) for detailed instructions on specific modules.
3.  **Create ROS 2 Workspace**: If not already done, set up a ROS 2 workspace.
4.  **Integrate Isaac ROS Modules**:
    *   Clone or download the relevant Isaac ROS package (e.g., `isaac_ros_stereo_image_proc`).
    *   Place it in your ROS 2 workspace (`ros2_ws/src/`).
    *   Create `config` and `launch` files as needed for your pipeline.

## Example `stereo_image_proc` Launch File (Conceptual)

```python
import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    # Declare arguments
    declare_namespace_cmd = DeclareLaunchArgument(
        'namespace',
        default_value='',
        description='Namespace for the nodes')

    # Example: Stereo Image Proc node
    stereo_image_proc_node = Node(
        package='isaac_ros_stereo_image_proc', # Example package
        executable='stereo_image_proc_node',    # Example executable
        name='stereo_image_proc',
        namespace=LaunchConfiguration('namespace'),
        parameters=[{
            # Example parameters
            'approximate_sync': True,
            'queue_size': 10
        }],
        remappings=[
            ('left/image_rect', 'front_stereo_camera/left/image_rect'),
            ('left/camera_info', 'front_stereo_camera/left/camera_info'),
            ('right/image_rect', 'front_stereo_camera/right/image_rect'),
            ('right/camera_info', 'front_stereo_camera/right/camera_info'),
            ('stereo_image_proc/depth', 'depth_map')
        ],
        output='screen'
    )

    ld = LaunchDescription()
    ld.add_action(declare_namespace_cmd)
    ld.add_action(stereo_image_proc_node)
    return ld
```

This conceptual example shows how an Isaac ROS module might be launched within ROS 2. Actual implementation details depend on the specific Isaac ROS package and hardware setup.
