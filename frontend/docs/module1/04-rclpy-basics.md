# Controlling ROS 2 with Python using rclpy

This chapter will teach you how to use the `rclpy` library to create ROS 2 nodes, publishers, and subscribers in Python.

## Creating a Simple Publisher

A publisher node sends messages to a topic. Here's an example of a simple publisher that sends "Hello World" messages.

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class SimplePublisher(Node):

    def __init__(self):
        super().__init__('simple_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = 'Hello World: %d' % self.i
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1

def main(args=None):
    rclpy.init(args=args)
    simple_publisher = SimplePublisher()
    rclpy.spin(simple_publisher)
    simple_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Explanation

-   **`rclpy.init(args=args)`**: Initializes the ROS 2 Python client library.
-   **`Node('simple_publisher')`**: Creates a new node named `simple_publisher`.
-   **`create_publisher(String, 'topic', 10)`**: Creates a publisher that sends `String` messages to a topic named `topic` with a queue size of 10.
-   **`create_timer(timer_period, self.timer_callback)`**: Sets up a timer to call `timer_callback` every 0.5 seconds.
-   **`publisher_.publish(msg)`**: Publishes the message to the topic.
-   **`rclpy.spin(simple_publisher)`**: Keeps the node alive until it's explicitly shut down.

## Creating a Simple Subscriber

A subscriber node receives messages from a topic. Here's an example of a simple subscriber that listens for "Hello World" messages.

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class SimpleSubscriber(Node):

    def __init__(self):
        super().__init__('simple_subscriber')
        self.subscription = self.create_subscription(
            String,
            'topic',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.data)

def main(args=None):
    rclpy.init(args=args)
    simple_subscriber = SimpleSubscriber()
    rclpy.spin(simple_subscriber)
    simple_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Explanation

-   **`create_subscription(String, 'topic', self.listener_callback, 10)`**: Creates a subscriber that listens for `String` messages on the `topic` topic and calls `listener_callback` when a message is received.
-   **`listener_callback(self, msg)`**: This function is called every time a new message is received. It logs the received message.
