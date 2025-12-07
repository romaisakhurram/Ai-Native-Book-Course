import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    # Get the URDF file path
    # Assuming 'simple_humanoid.urdf' is directly in the package's share directory
    # For this example, we place it in frontend/src/urdf/
    urdf_file = os.path.join(
        os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'urdf')),
        'simple_humanoid.urdf'
    )

    # Check if URDF file exists
    if not os.path.exists(urdf_file):
        raise FileNotFoundError(f"URDF file not found at: {urdf_file}")

    with open(urdf_file, 'r') as infp:
        robot_desc = infp.read()

    return LaunchDescription([
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            parameters=[{'robot_description': robot_desc}],
            output='screen'),
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='joint_state_publisher_gui',
            output='screen'),
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            arguments=['-d', os.path.join(get_package_share_directory('rviz2'), 'config', 'rviz2_default.rviz')]
        )
    ])