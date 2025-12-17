# Setting up Isaac Sim and Isaac ROS Environments

This chapter provides a foundational guide for setting up your development environment to work with NVIDIA Isaac Sim and Isaac ROS. This powerful combination allows for advanced robotics simulation, photorealistic rendering, synthetic data generation, and hardware-accelerated AI perception.

## Learning Objectives

After completing this chapter, you will be able to:

-   Install NVIDIA Omniverse Launcher and Isaac Sim.
-   Install Docker and the NVIDIA Container Toolkit on your Ubuntu system.
-   Set up a ROS 2 workspace and pull necessary Isaac ROS Docker images.
-   Verify the integration of Isaac Sim and Isaac ROS environments.

## 1.1 Prerequisites

Before proceeding, ensure your system meets these critical requirements:

-   **Operating System**: Ubuntu 20.04 or 22.04 LTS (64-bit).
-   **NVIDIA GPU**: RTX 2060 or higher (RTX 30 Series, 40 Series, or NVIDIA A100/A6000 recommended).
-   **NVIDIA Driver**: Version 525.85.12 or newer.
-   **CPU**: Intel i7 or AMD Ryzen 7 (or newer).
-   **RAM**: 32 GB or more.
-   **Disk Space**: 100 GB SSD recommended.

## 1.2 Isaac Sim Installation

Isaac Sim is built on NVIDIA Omniverse. You'll first install the Omniverse Launcher, then use it to install Isaac Sim.

### Step 1: Install Omniverse Launcher

1.  **Download**: Go to the [NVIDIA Omniverse Download Center](https://www.nvidia.com/en-us/omniverse/download/) and download the Omniverse Launcher for Linux.
2.  **Install**: Open a terminal and navigate to your download directory. Make the installer executable and run it:
    ```bash
    chmod +x omniverse-launcher-linux.run
    ./omniverse-launcher-linux.run
    ```
    Follow the graphical installer prompts.

### Step 2: Install Isaac Sim

1.  **Launch Omniverse Launcher**: Open the NVIDIA Omniverse Launcher application.
2.  **Sign In**: Sign in with your NVIDIA account.
3.  **Exchange Tab**: Navigate to the "Exchange" tab.
4.  **Find Isaac Sim**: Search for "Isaac Sim".
5.  **Install**: Select the latest recommended version of Isaac Sim and click "Install". This will download and install Isaac Sim and its core dependencies.

### Step 3: Launch and Verify Isaac Sim

1.  Once installed, go to the "Library" tab in the Omniverse Launcher.
2.  Click "Launch" next to Isaac Sim.
3.  Ensure Isaac Sim opens correctly and you can navigate a default scene (e.g., the "Isaac Examples" or "Simple Room" scene).

## 1.3 Isaac ROS Installation

Isaac ROS modules run within Docker containers and rely on the NVIDIA Container Toolkit.

### Step 1: Install Docker

If you don't have Docker installed, follow these steps:

```bash
# Add Docker's official GPG key:
sudo apt update
sudo apt install ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# Add the Docker repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update

# Install Docker packages:
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Add your user to the docker group to run docker commands without sudo
sudo usermod -aG docker $USER
newgrp docker # Apply group changes without logging out
```

### Step 2: Install NVIDIA Container Toolkit

This toolkit allows Docker containers to access your NVIDIA GPU.

```bash
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
sudo apt update
sudo apt install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
```

### Step 3: Pull Isaac ROS Docker Images

Isaac ROS modules are pre-built within Docker images. You'll need to pull the base development image.

```bash
docker pull nvcr.io/nvidia/isaac-ros-dev:humble
# Use 'foxy' if you are on ROS 2 Foxy, 'galactic' for Galactic, etc.
# 'humble' is recommended for this book.
```

### Step 4: Create a ROS Workspace (Host System)

You'll need a standard ROS 2 workspace on your host system to store your code and build Isaac ROS packages that aren't provided in the Docker images.

```bash
mkdir -p ~/isaac_ros_ws/src
cd ~/isaac_ros_ws
# Install vcs if not already installed
sudo apt install python3-vcstool -y
# Download Isaac ROS repositories (replace with specific ones as needed)
vcs import src < https://raw.githubusercontent.com/NVIDIA-ISAAC-ROS/isaac_ros_common/humble/isaac_ros_common.repos
# Build the workspace (from within a dev container)
# colcon build --symlink-install
```

## 1.4 Verifying Your Setup

### Step 1: Launch Isaac Sim

Start Isaac Sim from the Omniverse Launcher. Load a sample scene, e.g., "Simple Room" or any of the Isaac Examples.

### Step 2: Launch Isaac ROS Development Container

Open a terminal on your host system and launch an Isaac ROS development container. This container will be where you run your ROS 2 nodes.

```bash
# Navigate to your isaac_ros_ws
cd ~/isaac_ros_ws
# Launch the dev container (adjust image tag if different)
# This example uses a script from isaac_ros_common if you cloned it
# If you don't have this script, you can manually run docker
docker run --rm -it --network host --privileged \
    -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -v ~/isaac_ros_ws:/workspaces/isaac_ros-dev \
    nvcr.io/nvidia/isaac-ros-dev:humble bash
```

Inside the Docker container, source your ROS 2 environment and build your workspace:

```bash
source /opt/ros/humble/setup.bash
colcon build --symlink-install
source install/setup.bash
```

### Step 3: Verify ROS 2 Communication

Now, you can test communication between Isaac Sim and the Isaac ROS container.

1.  **In Isaac Sim**: Load an example with a camera (e.g., `Isaac Examples -> ROS -> ROS_ImagePublisher`). Press play.
2.  **In Isaac ROS Container Terminal**:
    ```bash
    ros2 topic list
    ```
    You should see topics like `/front_stereo_camera/left/image_raw` or `/rgbd_camera/rgb/image_raw` being published by Isaac Sim.

    To visualize the image:
    ```bash
    ros2 run rviz2 rviz2
    ```
    Add an Image display in RViz2 and select the appropriate image topic. You should see the camera feed from Isaac Sim.

## Summary

This chapter guided you through the comprehensive setup of NVIDIA Isaac Sim and Isaac ROS environments. You installed the Omniverse Launcher, Isaac Sim, Docker, and the NVIDIA Container Toolkit. You also learned how to pull Isaac ROS Docker images, set up a ROS workspace, and verify the communication between Isaac Sim and Isaac ROS development containers. This powerful setup forms the foundation for developing advanced AI-driven robotics applications.

## Review Questions

1.  What is NVIDIA Isaac Sim, and what is its primary purpose in robotics development?
2.  What are the minimum hardware requirements for running Isaac Sim effectively?
3.  Why is the NVIDIA Container Toolkit essential for Isaac ROS?
4.  Describe the steps to launch an Isaac ROS development container and prepare it for ROS 2 development.
5.  How would you verify that Isaac Sim is publishing camera data that can be received by an Isaac ROS container?
6.  Explain the general workflow for developing an Isaac ROS perception node within a Docker container.