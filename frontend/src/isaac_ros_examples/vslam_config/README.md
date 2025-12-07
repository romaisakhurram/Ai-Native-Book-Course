# Isaac ROS VSLAM Configuration - Manual Setup

This directory is intended to contain configuration files for Isaac ROS VSLAM (Visual SLAM) integration. VSLAM modules typically run within Docker containers and require a specialized development environment (NVIDIA GPU, specific Ubuntu version, ROS 2 installation).

## Steps for Setup:

1.  **Ensure Isaac ROS Environment**: Verify you have a correctly set up Isaac ROS development environment, including Docker and NVIDIA Container Toolkit.
2.  **Refer to Isaac ROS VSLAM Documentation**: Consult the official [Isaac ROS Visual SLAM Documentation](https://nvidia-isaac-ros.github.io/documents/vslam/vslam.html) for detailed instructions.
3.  **Create Configuration Files**: Depending on the specific VSLAM module (e.g., `isaac_ros_vslam`), you will need to create and configure YAML files for parameters such as camera intrinsics, extrinsic calibration, and VSLAM specific settings.

## Example VSLAM Configuration File (Conceptual)

```yaml
# Example parameters for isaac_ros_vslam node
vslam:
  ros__parameters:
    denoise_input_images: True
    flow_detector_type: "orb" # or "harris"
    orb_grid_size: [8, 8]
    orb_num_features: 2000
    track_max_skip_frames: 2
    map_frame: "map"
    odom_frame: "odom"
    base_frame: "base_link"
    input_imu_frame: "imu_link"
    enable_imu_fusion: False # Set to True if IMU is available and calibrated
    # ... more parameters
```

This conceptual example shows typical parameters for an Isaac ROS VSLAM node. Actual implementation details depend on the specific Isaac ROS package and hardware setup.
