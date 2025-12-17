# Data Model: Book Module 1 - The Robotic Nervous System (ROS 2)

## Core Entities

### Chapter
- **Name**: String (e.g., "Introduction to ROS 2")
- **Path**: String (e.g., "docs/module1/00-intro.md")
- **Content**: Markdown text with textbook-style explanations
- **Diagrams**: List of diagram references
- **Code Examples**: List of embedded Python code blocks
- **Learning Objectives**: List of educational goals
- **Prerequisites**: List of required knowledge
- **Success Indicators**: List of measurable outcomes

### ROS 2 Entity
- **Node**: Software component that performs computation
  - Name: String
  - Namespace: String (optional)
  - Parameters: Dictionary of configuration values
  - Publishers: List of topics published to
  - Subscribers: List of topics subscribed to
  - Services: List of services provided
  - Clients: List of services called

- **Topic**: Data stream for communication between nodes
  - Name: String
  - Type: Message type (e.g., std_msgs/String)
  - Quality of Service: QoS settings
  - Publisher Count: Number of publishers
  - Subscriber Count: Number of subscribers

- **Service**: Request-response communication pattern
  - Name: String
  - Type: Service type (e.g., std_srvs/SetBool)
  - Server: Node providing the service
  - Clients: List of nodes calling the service

- **Action**: Goal-based communication with feedback
  - Name: String
  - Type: Action type (e.g., example_interfaces/Fibonacci)
  - Server: Node providing the action
  - Clients: List of nodes using the action

### URDF Entity
- **Robot**: Top-level definition of a robot
  - Name: String
  - Links: List of rigid body parts
  - Joints: List of connections between links
  - Materials: List of visualization materials
  - Transmissions: List of actuator interfaces

- **Link**: Rigid body part of the robot
  - Name: String
  - Inertial: Mass, center of mass, and inertia properties
  - Visual: Geometry and material for visualization
  - Collision: Geometry for collision detection

- **Joint**: Connection between two links
  - Name: String
  - Type: Joint type (revolute, continuous, prismatic, fixed, etc.)
  - Parent: Parent link name
  - Child: Child link name
  - Origin: Position and orientation relative to parent
  - Axis: Rotation or translation axis
  - Limits: Joint limits for revolute and prismatic joints

### Code Example
- **Name**: String identifier
- **Path**: File path (e.g., src/ros2_examples/simple_talker.py)
- **Language**: Programming language (Python)
- **Dependencies**: List of required packages/libraries
- **Execution Time**: Expected runtime (≤ 5 seconds)
- **Security Rating**: Compliance with ROS 2 security best practices
- **Comments Quality**: Level of explanatory comments
- **Test Coverage**: Unit tests status

## Relationships

### Chapter Contains Code Examples
- A Chapter contains multiple Code Example entities
- Each Code Example is embedded within the Chapter's content
- The Code Examples demonstrate concepts explained in the Chapter

### Code Example Uses ROS 2 Entities
- A Code Example typically implements one or more ROS 2 Entities
- e.g., A publisher example implements a Node and Publisher
- e.g., A service client example implements a Node and Client

### URDF Defines Robot Structure
- A URDF Entity defines the structure of a humanoid robot
- Links and Joints form the kinematic chain of the robot
- The Robot entity contains both Links and Joints

### Humanoid Robot Context
- All examples and explanations use humanoid robot context
- ROS 2 Entities are demonstrated in humanoid robot scenarios
- URDF Entities represent parts of a humanoid robot

## Validation Rules

- All Code Examples must run in under 5 seconds
- All Code Examples must follow ROS 2 security best practices
- All Code Examples must include comprehensive comments
- All URDF files must be syntactically correct
- All Chapter content must be in textbook-style instructional tone
- All content must be compatible with Docusaurus markdown format
- Diagrams must be in Mermaid or ASCII format

## State Transitions

### Content Development States
- Draft → Review → Approved → Published
- Code Example: Created → Tested → Documented → Integrated
- Diagram: Conceptualized → Created → Reviewed → Embedded