# Building a Basic Digital Twin in Gazebo

This chapter will guide you through creating a basic robot digital twin model in Gazebo, configuring its physics and collision properties, and attaching simulated sensors like LiDAR and IMU.

## Robot Model (URDF)

We'll start by defining our robot model using URDF (Unified Robot Description Format). This file will include the robot's links, joints, physics properties, collision meshes, and sensor definitions.

Create `basic_robot.urdf` in `frontend/src/gazebo_examples/`:

```xml
<?xml version="1.0"?>
<robot name="basic_robot">

  <link name="base_link">
    <visual>
      <geometry>
        <box size="0.2 0.2 0.1"/>
      </geometry>
      <material name="blue">
        <color rgba="0 0 0.8 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <box size="0.2 0.2 0.1"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1.0"/>
      <inertia ixx="0.005" ixy="0.0" ixz="0.0" iyy="0.005" iyz="0.0" izz="0.005"/>
    </inertial>
  </link>

  <joint name="lidar_joint" type="fixed">
    <parent link="base_link"/>
    <child link="lidar_link"/>
    <origin xyz="0 0 0.05" rpy="0 0 0"/>
  </joint>

  <link name="lidar_link">
    <visual>
      <geometry>
        <cylinder radius="0.03" length="0.02"/>
      </geometry>
      <material name="black">
        <color rgba="0.1 0.1 0.1 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <cylinder radius="0.03" length="0.02"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="0.1"/>
      <inertia ixx="0.0001" ixy="0.0" ixz="0.0" iyy="0.0001" iyz="0.0" izz="0.0001"/>
    </inertial>
  </link>

  <!-- Gazebo specific tags for sensor simulation -->
  <gazebo reference="lidar_link">
    <sensor name="lidar" type="ray">
      <pose>0 0 0 0 0 0</pose>
      <visualize>true</visualize>
      <update_rate>10</update_rate>
      <ray>
        <scan>
          <horizontal>
            <samples>640</samples>
            <resolution>1</resolution>
            <min_angle>-2.2689</min_angle>
            <max_angle>2.2689</max_angle>
          </horizontal>
        </scan>
        <range>
          <min>0.1</min>
          <max>10.0</max>
          <resolution>0.01</resolution>
        </range>
      </ray>
      <plugin name="gazebo_ros_ray_sensor_controller" filename="libgazebo_ros_ray_sensor.so">
        <ros>
          <argument>~/out:=scan</argument>
          <argument>~/out_depth:=scan_depth</argument>
        </ros>
        <output_type>sensor_msgs/LaserScan</output_type>
        <frame_name>lidar_link</frame_name>
      </plugin>
    </sensor>
  </gazebo>

</robot>
```

### Explanation of the URDF

-   **`<link>`**: Defines a rigid body. `base_link` forms the main body, and `lidar_link` represents a LiDAR sensor.
    -   **`<visual>`**: Describes the visual appearance.
    -   **`<collision>`**: Defines the physical shape used for collision detection.
    -   **`<inertial>`**: Specifies the mass and inertia properties, crucial for realistic physics simulation.
-   **`<joint>`**: Connects links. Here, `lidar_joint` is `fixed` to the `base_link`.
-   **`<gazebo>`**: This block contains Gazebo-specific extensions.
    -   **`<sensor name="lidar" type="ray">`**: Defines a ray-based sensor (LiDAR).
    -   **`<plugin>`**: Loads a Gazebo plugin. `libgazebo_ros_ray_sensor.so` is a standard plugin that publishes sensor data to ROS 2 topics.

## Gazebo World File

To load our robot into a simulation, we need a Gazebo world file. This file defines the environment, including lighting, ground plane, and our robot.

Create `basic_world.sdf` in `frontend/src/gazebo_examples/`:

```xml
<?xml version="1.0" ?>
<sdf version="1.7">
  <world name="basic_digital_twin_world">
    <gravity>0 0 -9.8</gravity>

    <!-- Sun light source -->
    <include>
      <uri>model://sun</uri>
    </include>

    <!-- Ground plane -->
    <include>
      <uri>model://ground_plane</uri>
    </include>

    <!-- Our basic robot digital twin -->
    <include>
      <uri>file://basic_robot.urdf</uri>
      <name>basic_robot</name>
      <pose>0 0 0.5 0 0 0</pose>
    </include>

  </world>
</sdf>
```

### Explanation of the World File

-   **`<world>`**: The root element for a Gazebo world.
-   **`<gravity>`**: Sets the gravity vector.
-   **`<include>`**: Allows including predefined Gazebo models (like `sun` and `ground_plane`) or our custom robot model.
    -   **`<uri>file://basic_robot.urdf</uri>`**: Points to our URDF file.

## How to Run the Simulation

1.  Source your ROS 2 environment.
2.  Navigate to the `frontend/` directory.
3.  Launch Gazebo with your world file:
    ```bash
    gazebo --verbose frontend/src/gazebo_examples/basic_world.sdf
    ```
4.  In a new terminal, you can check for the LiDAR data:
    ```bash
    ros2 topic list
    ros2 topic echo /scan
    ```
    You should see your basic robot in Gazebo and be able to observe its simulated LiDAR data.
