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
    'preface', // This refers to docs/preface.md
    {
      type: 'category',
      label: 'Module 1: The Robotic Nervous System (ROS 2)',
      items: [
        'module1/00-setup',
        'module1/01-nodes',
        'module1/02-topics',
        'module1/03-services',
        'module1/04-rclpy-basics',
        'module1/05-urdf-basics',
      ],
    },
    {
      type: 'category',
      label: 'Module 2: The Digital Twin (Gazebo & Unity)',
      items: [
        'module2/00-setup-gazebo',
        'module2/00-setup-unity',
        'module2/01-physics-collision',
        'module2/02-sensor-sim',
        'module2/03-gazebo-digital-twin',
        'module2/04-unity-hri',
      ],
    },
    {
      type: 'category',
      label: 'Module 3: The AI-Robot Brain (NVIDIA Isaac)',
      items: [
        'module3/00-setup-isaac',
        'module3/01-isaac-sim-basics',
        'module3/02-isaac-ros-perception',
        'module3/03-isaac-ros-pipeline',
        'module3/04-nav2-humanoid-isaac',
      ],
    },
  ],
};

export default sidebars;
