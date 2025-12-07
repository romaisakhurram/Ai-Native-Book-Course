# Understanding ROS 2 Topics

**Topics** are the most common communication mechanism in ROS 2. They implement a **publish/subscribe** messaging pattern, allowing nodes to exchange data asynchronously.

## How Topics Work

1.  **Publishers**: A node that wants to send data creates a **publisher** for a specific topic.
2.  **Subscribers**: A node that wants to receive data creates a **subscriber** for the same topic.
3.  **Messages**: Data is exchanged as **messages**. Each topic has a defined message type (e.g., `std_msgs/String`, `geometry_msgs/Twist`).
4.  **Asynchronous**: Publishers and subscribers operate independently. A publisher sends messages without knowing if any subscriber is listening, and subscribers receive messages whenever they are published.

This decoupled nature makes topics highly flexible and scalable.

## Key Characteristics of Topics

-   **One-to-Many / Many-to-One**: A single publisher can send messages to multiple subscribers, and multiple publishers can send messages to a single subscriber on the same topic.
-   **Anonymity**: Publishers and subscribers don't need to know about each other's existence. The ROS 2 middleware handles the connections.
-   **Loose Coupling**: Nodes are loosely coupled, making it easy to swap out or add new components without affecting the entire system.
-   **Data Streams**: Topics are best suited for continuous streams of data, such as sensor readings (lidar, camera, IMU), motor commands, or robot odometry.

## Message Types

Every message sent over a topic must conform to a specific message type. Message types are defined in `.msg` files and consist of a set of typed fields.

**Common Message Types:**
-   `std_msgs/String`: A simple string message.
-   `geometry_msgs/Twist`: Represents linear and angular velocity.
-   `sensor_msgs/Image`: Represents camera image data.

You can inspect message definitions using `ros2 interface show <message_type>`.

## Creating a Topic Publisher (rclpy)

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String # Import the message type

class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        # Create a publisher: message type, topic name, queue size
        self.publisher_ = self.create_publisher(String, 'chatter', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = 'Hello ROS 2: %d' % self.i
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data) # Log the published message
        self.i += 1

def main(args=None):
    rclpy.init(args=args)
    minimal_publisher = MinimalPublisher()
    rclpy.spin(minimal_publisher) # Keep node alive
    minimal_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Creating a Topic Subscriber (rclpy)

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String # Import the message type

class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        # Create a subscriber: message type, topic name, callback function, queue size
        self.subscription = self.create_subscription(
            String,
            'chatter',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.data) # Log the received message

def main(args=None):
    rclpy.init(args=args)
    minimal_subscriber = MinimalSubscriber()
    rclpy.spin(minimal_subscriber) # Keep node alive
    minimal_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Topic Management

ROS 2 provides command-line tools to interact with topics:

-   **`ros2 topic list`**: Lists all active topics in the ROS 2 graph.
-   **`ros2 topic info <topic_name>`**: Displays detailed information about a topic, including its message type and the number of publishers and subscribers.
-   **`ros2 topic echo <topic_name>`**: Subscribes to a topic and prints the messages it receives to the console.
-   **`ros2 topic pub <topic_name> <message_type> <message_values>`**: Publishes data to a topic from the command line.

Topics are essential for real-time data flow in a robotic system, enabling different components to share information efficiently and asynchronously.
