# Understanding ROS 2 Services

While ROS 2 topics provide a flexible publish/subscribe mechanism for continuous data streams, **services** offer a **request/response** communication pattern. This is ideal for situations where a node needs to send a request to another node and wait for a specific response.

## How Services Work

1.  **Service Server**: A node that offers a particular functionality creates a **service server**. It defines a service type (request and response message structures) and registers a callback function to handle incoming requests.
2.  **Service Client**: A node that needs to use that functionality creates a **service client**. It sends a request message to the service server and blocks (or waits asynchronously) until it receives a response message.
3.  **Synchronous**: Unlike topics, services are typically synchronous (from the client's perspective). The client sends a request and pauses its operation until a response is received from the server. Asynchronous client calls are also possible, allowing the client to continue other tasks while waiting for the response.

## Key Characteristics of Services

-   **Request/Response**: Designed for explicit communication where a client expects an immediate answer to a request.
-   **One-to-One**: Typically, a single client makes a request to a single server.
-   **Blocking (Client-side)**: The client often waits for the server to process the request and send back a response before proceeding.
-   **Discrete Operations**: Best suited for discrete, one-time operations rather than continuous data streams. Examples include:
    -   Triggering an action (e.g., "take a picture", "start navigation").
    -   Querying a state (e.g., "get robot status", "what's the current map?").
    -   Performing a calculation (e.g., "solve inverse kinematics").

## Service Types

Similar to messages, services also have defined types, which specify the structure of both the request and the response. Service types are defined in `.srv` files.

A `.srv` file is essentially two `.msg` definitions separated by `---`. The first part is the request message, and the second is the response message.

**Example of a `.srv` file (e.g., `AddTwoInts.srv`):**

```
int64 a
int64 b
---
int64 sum
```

## Creating a Service Server (rclpy)

```python
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts # Import the service type

class MinimalService(Node):

    def __init__(self):
        super().__init__('minimal_service')
        # Create a service server: service type, service name, callback function
        self.srv = self.create_service(AddTwoInts, 'add_two_ints', self.add_two_ints_callback)
        self.get_logger().info('Service server for "add_two_ints" is ready.')

    def add_two_ints_callback(self, request, response):
        response.sum = request.a + request.b
        self.get_logger().info(f'Incoming request: a={request.a}, b={request.b}. Sending response: sum={response.sum}')
        return response

def main(args=None):
    rclpy.init(args=args)
    minimal_service = MinimalService()
    rclpy.spin(minimal_service)
    minimal_service.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Creating a Service Client (rclpy)

```python
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts
import sys

class MinimalClientAsync(Node):

    def __init__(self):
        super().__init__('minimal_client_async')
        # Create a service client: service type, service name
        self.cli = self.create_client(AddTwoInts, 'add_two_ints')
        # Wait until the service is available
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service not available, waiting again...')
        self.req = AddTwoInts.Request()

    def send_request(self, a, b):
        self.req.a = a
        self.req.b = b
        self.future = self.cli.call_async(self.req) # Asynchronously call the service
        # rclpy.spin_until_future_complete(self, self.future) # To wait synchronously
        return self.future

def main(args=None):
    rclpy.init(args=args)

    minimal_client = MinimalClientAsync()
    response_future = minimal_client.send_request(int(sys.argv[1]), int(sys.argv[2]))
    
    rclpy.spin_until_future_complete(minimal_client, response_future)

    if response_future.result() is not None:
        minimal_client.get_logger().info(
            f'Result of add_two_ints: for {minimal_client.req.a} + {minimal_client.req.b} = {response_future.result().sum}')
    else:
        minimal_client.get_logger().error('Service call failed :(')

    minimal_client.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: ros2 run minimal_client_async minimal_client_async <int> <int>')
        sys.exit(1)
    main()
```

## Service Management

ROS 2 provides command-line tools to interact with services:

-   **`ros2 service list`**: Lists all active services in the ROS 2 graph.
-   **`ros2 service type <service_name>`**: Shows the type of a service.
-   **`ros2 service find <service_type>`**: Finds services of a specific type.
-   **`ros2 service call <service_name> <service_type> <arguments>`**: Calls a service from the command line.

Services are crucial for implementing functionalities that require immediate feedback or discrete actions, complementing the continuous data flow provided by topics.
