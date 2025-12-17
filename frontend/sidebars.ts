import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */
const sidebars: SidebarsConfig = {
  bookSidebar: [
    'intro', // This refers to docs/intro.md
    {
      type: 'category',
      label: 'Module 1: The Robotic Nervous System (ROS 2)',
      items: [
        'module1/setup',
        'module1/nodes',
        'module1/topics',
        'module1/services',
        'module1/rclpy-basics',
        'module1/urdf-basics',
      ],
    },
    {
      type: 'category',
      label: 'Module 2: The Digital Twin (Gazebo & Unity)',
      items: [
        'module2/setup-gazebo',
        'module2/setup-unity',
        'module2/physics-collision',
        'module2/sensor-sim',
        'module2/gazebo-digital-twin',
        'module2/unity-hri',
      ],
    },
    {
      type: 'category',
      label: 'Module 3: The AI-Robot Brain (NVIDIA Isaac)',
      items: [
        'module3/setup-isaac',
        'module3/isaac-sim-basics',
        'module3/isaac-ros-perception',
        'module3/isaac-ros-pipeline',
        'module3/nav2-humanoid-isaac',
      ],
    },
    {
      type: 'category',
      label: 'Module 4: Vision-Language-Action (VLA)',
      items: [
        'module4/intro',
        'module4/whisper-vision',
        'module4/llm-planning',
        'module4/ros2-mapping',
        'module4/capstone-architecture',
      ],
    },
  ],
};

export default sidebars;
