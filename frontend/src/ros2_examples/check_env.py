import os
import sys

def check_ros2_environment():
    """Checks for common ROS 2 environment variables."""
    required_vars = ['ROS_VERSION', 'ROS_PYTHON_VERSION', 'ROS_DISTRO']
    missing_vars = [var for var in required_vars if var not in os.environ]

    if not missing_vars:
        print("ROS 2 environment variables are set.")
        print(f"ROS_VERSION={os.environ['ROS_VERSION']}")
        print(f"ROS_PYTHON_VERSION={os.environ['ROS_PYTHON_VERSION']}")
        print(f"ROS_DISTRO={os.environ['ROS_DISTRO']}")
        return True
    else:
        print("The following ROS 2 environment variables are not set:", ", ".join(missing_vars))
        print("Please source your ROS 2 installation.")
        return False

if __name__ == "__main__":
    if not check_ros2_environment():
        sys.exit(1)
