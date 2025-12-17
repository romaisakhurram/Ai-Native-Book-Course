# rclpy Basics: Building Robust ROS 2 Nodes in Python

This chapter delves into the fundamental aspects of `rclpy`, the Python client library for ROS 2. You will learn how to initialize and structure ROS 2 nodes, manage parameters, and understand the lifecycle of a ROS 2 application written in Python. This chapter complements the previous discussions on nodes, topics, and services by focusing on the `rclpy` programming interface.

## Learning Objectives

After completing this chapter, you will be able to:

-   Understand the core lifecycle of an `rclpy` node.
-   Declare and manage ROS 2 parameters within an `rclpy` node.
-   Utilize `rclpy`'s logging utilities for effective debugging.
-   Implement timer-based callbacks for periodic tasks.

## 1.1 The rclpy Node Lifecycle

Every ROS 2 Python application begins with initializing `rclpy`, creating one or more nodes, spinning them to process callbacks, and finally shutting them down.

### Initialization and Shutdown

-   **`rclpy.init(args=None)`**: This function initializes the `rclpy` client library. It must be called before creating any nodes or interacting with the ROS 2 system. The `args` parameter allows passing command-line arguments to the ROS 2 context.
-   **`rclpy.spin(node)`**: This is the core function that keeps a node alive and processing events. When you call `rclpy.spin()`, the node enters a loop, listening for incoming messages, service requests, timer events, and other callbacks. It blocks the execution of your program until the node is explicitly shut down (e.g., via Ctrl+C or `node.destroy_node()` followed by `rclpy.shutdown()`).
-   **`rclpy.spin_once(node, timeout_sec=None)`**: Processes any pending callbacks in the node's queue and then returns. Useful for non-blocking operations or custom spin loops.
-   **`node.destroy_node()`**: Releases all resources associated with the node (publishers, subscribers, services, timers, etc.). It should be called before `rclpy.shutdown()`.
-   **`rclpy.shutdown()`**: Deinitializes the `rclpy` library, cleaning up global resources. It should be the last `rclpy` function called.

### Basic Node Structure Revisited

```python
import rclpy
from rclpy.node import Node

class MinimalNode(Node):
    def __init__(self):
        super().__init__('minimal_node')
        self.get_logger().info('MinimalNode has been initialized!')

def main(args=None):
    rclpy.init(args=args) # Initialize rclpy
    node = MinimalNode()  # Create a node
    try:
        rclpy.spin(node)  # Keep the node alive and processing events
    except KeyboardInterrupt:
        node.get_logger().info('MinimalNode stopped cleanly')
    finally:
        node.destroy_node() # Destroy the node
        rclpy.shutdown()    # Shutdown rclpy
```

## 1.2 ROS 2 Parameters with rclpy

**Parameters** allow nodes to expose configurable values at runtime. They are key-value pairs that can be read, written, and observed by other nodes or by the user via command-line tools.

### Declaring Parameters

You declare parameters within your node's constructor.

```python
import rclpy
from rclpy.node import Node
from rcl_interfaces.msg import SetParametersResult

class ParameterNode(Node):
    def __init__(self):
        super().__init__('parameter_node')

        # Declare a parameter with a default value
        self.declare_parameter('my_parameter', 'default_value')
        
        # Declare an integer parameter with description and read-only property
        self.declare_parameter('update_frequency_hz', 1.0)
        
        # Get the value of a declared parameter
        param_value = self.get_parameter('my_parameter').get_parameter_value().string_value
        self.get_logger().info(f'my_parameter is: {param_value}')

        # Add a callback for parameter changes (optional but good practice)
        self.add_on_set_parameters_callback(self.parameter_callback)

    def parameter_callback(self, params):
        for param in params:
            if param.name == 'my_parameter':
                self.get_logger().info(f'Parameter "my_parameter" changed to: {param.value}')
            elif param.name == 'update_frequency_hz':
                self.get_logger().info(f'Parameter "update_frequency_hz" changed to: {param.value}')
        return SetParametersResult(successful=True)

def main(args=None):
    rclpy.init(args=args)
    node = ParameterNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
```

### Interacting with Parameters (CLI)

-   **`ros2 param list`**: Lists all parameters on all active nodes.
-   **`ros2 param get <node_name> <parameter_name>`**: Gets the current value of a parameter.
-   **`ros2 param set <node_name> <parameter_name> <value>`**: Sets the value of a parameter.
-   **`ros2 param dump <node_name>`**: Dumps all parameters of a node to a YAML file.

## 1.3 Timer Callbacks for Periodic Tasks

Timers are used to schedule functions to be called periodically. They are fundamental for tasks that need to run at a fixed rate, such as publishing sensor data or updating a robot's state.

```python
import rclpy
from rclpy.node import Node
import time

class TimerNode(Node):
    def __init__(self):
        super().__init__('timer_node')
        timer_period = 1.0  # seconds
        # Create a timer that calls the timer_callback every `timer_period` seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.counter = 0
        self.get_logger().info('TimerNode initialized with a 1-second timer.')

    def timer_callback(self):
        self.counter += 1
        self.get_logger().info(f'Timer triggered! Count: {self.counter}')

def main(args=None):
    rclpy.init(args=args)
    node = TimerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('TimerNode stopped cleanly')
    finally:
        node.destroy_node()
        rclpy.shutdown()
```

## 1.4 rclpy Logging

`rclpy` provides robust logging capabilities, allowing you to output messages with different severity levels. This is crucial for debugging, monitoring, and understanding your node's behavior.

-   **`self.get_logger().debug('Debug message')`**
-   **`self.get_logger().info('Informative message')`**
-   **`self.get_logger().warn('Warning message')`**
-   **`self.get_logger().error('Error message')`**
-   **`self.get_logger().fatal('Fatal error message')`**

You can configure the logging level of a node via parameters or command-line arguments.

## Summary

This chapter provided a deeper dive into `rclpy`, focusing on the lifecycle of a Python ROS 2 node, parameter management, timer-based callbacks, and effective logging. By mastering these `rclpy` fundamentals, you are better equipped to build more complex and robust ROS 2 applications in Python.

## Review Questions

1.  Explain the purpose of `rclpy.spin()` and how it differs from `rclpy.spin_once()`.
2.  How do you declare a parameter in `rclpy`, and how can you retrieve its value?
3.  Describe a scenario where using an `rclpy` timer would be more appropriate than a topic subscription.
4.  What are the different logging levels available in `rclpy`, and when would you use each?
5.  How can you dynamically change a parameter's value from the command line while an `rclpy` node is running?
6.  Why is it important to call `node.destroy_node()` and `rclpy.shutdown()`?