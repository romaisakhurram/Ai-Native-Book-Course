# Setting up your ROS 2 Environment

This chapter will guide you through the process of setting up a ROS 2 development environment on Ubuntu Linux, which is the recommended operating system for ROS 2 development. A properly configured environment is crucial for building, running, and interacting with ROS 2 applications.

## Learning Objectives

After completing this chapter, you will be able to:

-   Prepare your Ubuntu system for ROS 2 installation.
-   Install the recommended ROS 2 distribution (Humble Hawksbill).
-   Configure your environment to use ROS 2 commands.
-   Verify your ROS 2 installation.

## 1.1 Prerequisites

Before installing ROS 2, ensure your system meets the following requirements:

-   **Operating System**: Ubuntu 22.04 (Jammy Jellyfish) 64-bit. While ROS 2 can run on other systems, Ubuntu provides the most straightforward setup experience.
-   **Internet Connection**: Required to download necessary packages.
-   **Terminal Access**: You'll be using the command line extensively.

## 1.2 Install ROS 2 Humble Hawksbill

Follow these step-by-step instructions to install ROS 2 Humble Hawksbill, the latest Long Term Support (LTS) release as of this book's publication.

### Step 1: Set up Locales

First, ensure you have a locale that supports UTF-8. If you're in a minimal environment, you might need to set one manually.

```bash
sudo apt update && sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8
```

:::tip
This step is crucial for ROS 2 to function correctly, especially with text processing and character encoding.
:::

### Step 2: Add ROS 2 apt Repositories

Now, add the ROS 2 GPG key and the repository to your system's sources list.

```bash
sudo apt install software-properties-common -y
sudo add-apt-repository universe -y

sudo apt update && sudo apt install curl -y
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://ريقياpackages.ros.org/ros2/ubuntu $(. /etc/os-release && echo UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
```

### Step 3: Install ROS 2 Packages

Update your package lists and then install the ROS 2 Humble Desktop environment. The Desktop version includes ROS, `rviz` (a 3D visualizer), demos, and tutorials.

```bash
sudo apt update
sudo apt upgrade -y
sudo apt install ros-humble-desktop -y
```

:::info
**Package Size**: The `ros-humble-desktop` package is quite large. This step may take some time depending on your internet connection.
:::

### Step 4: Environment Setup

ROS 2 relies on environment variables to locate its packages. You need to "source" the setup script in each new terminal session where you want to use ROS 2.

```bash
source /opt/ros/humble/setup.bash
```

To make this change permanent for new terminal sessions, add it to your `~/.bashrc` file:

```bash
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
```

If you are using Zsh, add it to `~/.zshrc`:

```bash
echo "source /opt/ros/humble/setup.zsh" >> ~/.zshrc
```

### Step 5: Install `rosdep`

`rosdep` is a tool for installing system dependencies for ROS packages. It's good practice to initialize and update it.

```bash
sudo apt install python3-rosdep -y
sudo rosdep init
rosdep update
```

## 1.3 Verification

To verify your ROS 2 installation, you can run a simple `talker` and `listener` demo. Open two separate terminal windows.

### Terminal 1 (Talker)

In the first terminal, source your ROS 2 setup and then run the `talker` node:

```bash
source /opt/ros/humble/setup.bash
ros2 run demo_nodes_cpp talker
```

You should see output similar to `Publishing: 'Hello World from C++: 1'`, with the number incrementing.

### Terminal 2 (Listener)

In the second terminal, source your ROS 2 setup and then run the `listener` node:

```bash
source /opt/ros/humble/setup.bash
ros2 run demo_nodes_py listener
```

You should see output similar to `I heard: [Hello World from C++: 1]`, confirming that the Python listener is receiving messages from the C++ talker.

If both nodes are publishing and subscribing correctly, your ROS 2 environment is successfully set up!

## 1.4 Troubleshooting Common Issues

-   **`command not found: ros2`**: This usually means you haven't sourced your `setup.bash`/`setup.zsh` file. Run `source /opt/ros/humble/setup.bash` (or `.zsh`) in your terminal.
-   **`rosdep update` fails**: Check your internet connection or try running `sudo rosdep init` again if it's a fresh install. Network issues or firewall settings can also cause this.
-   **Package installation errors**: Ensure your `apt` repositories are correctly added and up to date (`sudo apt update`).
-   **Slow downloads**: Use a mirror that is geographically closer to you if `apt` downloads are consistently slow.

## Summary

In this chapter, you successfully set up your ROS 2 Humble Hawksbill environment on Ubuntu. You learned how to configure locales, add ROS 2 repositories, install the necessary packages, set up your shell environment, and verify the installation using the demo nodes. A solid development environment is the foundation for all your future ROS 2 projects.

## Review Questions

1.  What is the recommended operating system for ROS 2 development?
2.  Which ROS 2 distribution did you install in this chapter, and why is it a good choice?
3.  Why is it important to "source" the `setup.bash` file after installing ROS 2?
4.  What command would you use to verify that your ROS 2 installation is working correctly? Describe the expected output.
5.  If you encounter a "command not found: ros2" error, what is the most likely cause and solution?
6.  Explain the purpose of `rosdep` in the ROS 2 ecosystem.