# Modeling a Simple Humanoid with URDF

This chapter will guide you through creating a simple humanoid robot model using URDF (Unified Robot Description Format) and visualizing it in RViz2.

## What is URDF?

URDF (Unified Robot Description Format) is an XML format for describing robots. It's used in ROS to define the robot's kinematics (links and joints), visual properties, and collision properties.

## Creating a Simple Humanoid URDF

Let's create a basic URDF file for a simple humanoid robot with a base and a head.

First, create a file named `simple_humanoid.urdf` in `src/urdf/`.

```xml
<?xml version="1.0"?>
<robot name="simple_humanoid">

  <link name="base_link">
    <visual>
      <geometry>
        <box size="0.1 0.1 0.2"/>
      </geometry>
      <material name="blue">
        <color rgba="0 0 0.8 1"/>
      </material>
    </visual>
  </link>

  <joint name="head_joint" type="revolute">
    <parent link="base_link"/>
    <child link="head_link"/>
    <origin xyz="0 0 0.15"/>
    <axis xyz="0 0 1"/>
    <limit lower="-1.57" upper="1.57" effort="100" velocity="100"/>
  </joint>

  <link name="head_link">
    <visual>
      <geometry>
        <sphere radius="0.05"/>
      </geometry>
      <material name="red">
        <color rgba="0.8 0 0 1"/>
      </material>
    </visual>
  </link>

</robot>
```

### Explanation

-   **`<robot>`**: The root element of every URDF file. It has a `name` attribute.
-   **`<link>`**: Represents a rigid body part of the robot. `base_link` is the main body, and `head_link` is the head.
-   **`<visual>`**: Defines the visual properties of the link, including its geometry (e.g., `box`, `sphere`) and `material` (color).
-   **`<joint>`**: Connects two links. `head_joint` connects `base_link` (parent) to `head_link` (child).
    -   **`type="revolute"`**: Specifies a rotational joint.
    -   **`origin xyz`**: Defines the joint's position relative to the parent link.
    -   **`axis xyz`**: Defines the axis of rotation.
    -   **`limit`**: Sets the lower and upper bounds for the joint's movement.

## Publishing Joint States

To make our robot move, we need to publish joint states. We'll create a Python script to publish a sinusoidal motion for the `head_joint`.

Create a file named `joint_state_publisher.py` in `src/ros2_examples/`.

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import Header
import math

class JointStatePublisher(Node):

    def __init__(self):
        super().__init__('joint_state_publisher')
        self.publisher_ = self.create_publisher(JointState, 'joint_states', 10)
        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0.0

    def timer_callback(self):
        joint_state = JointState()
        joint_state.header = Header()
        joint_state.header.stamp = self.get_clock().now().to_msg()
        joint_state.name = ['head_joint']
        joint_state.position = [math.sin(self.i)]
        self.publisher_.publish(joint_state)
        self.i += 0.05
        self.get_logger().info(f'Publishing joint state: head_joint={joint_state.position[0]:.2f}')

def main(args=None):
    rclpy.init(args=args)
    joint_state_publisher = JointStatePublisher()
    rclpy.spin(joint_state_publisher)
    joint_state_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Visualizing with RViz2

To see our robot model and its movement, we use RViz2. We'll create a launch file to simplify this process.

Create a file named `display.launch.py` in `src/ros2_examples/`.

```python
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    urdf_file = os.path.join(
        os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'urdf')),
        'simple_humanoid.urdf'
    )

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
```

### How to Run

1.  Source your ROS 2 environment.
2.  Navigate to the `frontend/` directory.
3.  Run the launch file:
    ```bash
    ros2 launch ros2_examples display.launch.py
    ```
4.  Run the joint state publisher script:
    ```bash
    ros2 run ros2_examples joint_state_publisher
    ```
    You should see your simple humanoid model in RViz2, with its head rotating.
