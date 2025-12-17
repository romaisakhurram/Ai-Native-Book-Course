# Quickstart Guide: Book Module 1 - The Robotic Nervous System (ROS 2)

## Prerequisites

Before starting with Module 1, ensure you have:

1. **ROS 2 Humble Hawksbill** installed on your system
2. **Python 3.10+** (compatible with ROS 2 Humble)
3. **Docusaurus** development environment (for viewing the book locally)
4. **Basic Python knowledge** (functions, classes, modules)

## Setting Up the Environment

### 1. Install ROS 2 Humble Hawksbill

Follow the official installation guide for your OS:
- Ubuntu: http://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debians.html
- Windows: http://docs.ros.org/en/humble/Installation/Windows-Install-Binary.html
- macOS: http://docs.ros.org/en/humble/Installation/macOS-Install-Binary.html

### 2. Verify Installation

Open a terminal and run:

```bash
source /opt/ros/humble/setup.bash  # On Ubuntu
ros2 --version
```

### 3. Create a Workspace for Examples

```bash
mkdir -p ~/ros2_book_ws/src
cd ~/ros2_book_ws
colcon build
source install/setup.bash
```

## Running Code Examples

### 1. Clone the Example Repository

The code examples for this book are available in the `src/ros2_examples/` directory.

### 2. Run a Simple Publisher-Subscriber Example

```bash
# Terminal 1: Run the publisher
cd ~/ros2_book_ws
source install/setup.bash
python3 src/ros2_examples/simple_talker.py

# Terminal 2: Run the subscriber
cd ~/ros2_book_ws
source install/setup.bash
python3 src/ros2_examples/simple_listener.py
```

### 3. Testing Code Examples

All examples in this book follow these standards:
- Run in under 5 seconds on standard hardware
- Include comprehensive comments
- Follow ROS 2 security best practices
- Come with unit tests in `test_examples.py`

To run unit tests for examples:

```bash
cd ~/ros2_book_ws
source install/setup.bash
python3 -m pytest src/ros2_examples/test_examples.py
```

## Understanding the Module Structure

Module 1: The Robotic Nervous System (ROS 2) is organized into four chapters:

1. `00-intro.md` - Introduction to ROS 2 as the nervous system of humanoid robots
2. `01-architecture.md` - ROS 2 architecture: nodes, topics, services, and actions
3. `02-coding.md` - Practical rclpy coding with humanoid robot examples
4. `03-urdf.md` - Humanoid URDF structure and examples

## Diagrams Reference

The module includes three key diagrams:
- `static/img/ros2_architecture.mmd` - ROS 2 architecture diagram
- `static/img/ros2_communication.mmd` - Communication model diagram
- `static/img/humanoid_control.mmd` - Humanoid control pipeline diagram

## Viewing the Book Locally

To run the Docusaurus site locally:

```bash
cd /path/to/your/book/repository
npm install
npm start
```

The book will be available at http://localhost:3000

## Troubleshooting

- If ROS 2 commands are not found, make sure you've sourced the setup.bash file
- If Python examples fail, verify you're using Python 3.10+ and have rclpy installed
- For Docusaurus issues, check the npm installation and dependencies