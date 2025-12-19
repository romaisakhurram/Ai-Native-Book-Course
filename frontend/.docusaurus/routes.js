import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/ai-native-book-course/__docusaurus/debug',
    component: ComponentCreator('/ai-native-book-course/__docusaurus/debug', '5df'),
    exact: true
  },
  {
    path: '/ai-native-book-course/__docusaurus/debug/config',
    component: ComponentCreator('/ai-native-book-course/__docusaurus/debug/config', '3a9'),
    exact: true
  },
  {
    path: '/ai-native-book-course/__docusaurus/debug/content',
    component: ComponentCreator('/ai-native-book-course/__docusaurus/debug/content', '3d7'),
    exact: true
  },
  {
    path: '/ai-native-book-course/__docusaurus/debug/globalData',
    component: ComponentCreator('/ai-native-book-course/__docusaurus/debug/globalData', '2c5'),
    exact: true
  },
  {
    path: '/ai-native-book-course/__docusaurus/debug/metadata',
    component: ComponentCreator('/ai-native-book-course/__docusaurus/debug/metadata', 'd01'),
    exact: true
  },
  {
    path: '/ai-native-book-course/__docusaurus/debug/registry',
    component: ComponentCreator('/ai-native-book-course/__docusaurus/debug/registry', 'f99'),
    exact: true
  },
  {
    path: '/ai-native-book-course/__docusaurus/debug/routes',
    component: ComponentCreator('/ai-native-book-course/__docusaurus/debug/routes', 'c1c'),
    exact: true
  },
  {
    path: '/ai-native-book-course/blog',
    component: ComponentCreator('/ai-native-book-course/blog', '35a'),
    exact: true
  },
  {
    path: '/ai-native-book-course/blog/archive',
    component: ComponentCreator('/ai-native-book-course/blog/archive', 'b21'),
    exact: true
  },
  {
    path: '/ai-native-book-course/blog/authors',
    component: ComponentCreator('/ai-native-book-course/blog/authors', 'e53'),
    exact: true
  },
  {
    path: '/ai-native-book-course/blog/authors/all-sebastien-lorber-articles',
    component: ComponentCreator('/ai-native-book-course/blog/authors/all-sebastien-lorber-articles', '454'),
    exact: true
  },
  {
    path: '/ai-native-book-course/blog/authors/yangshun',
    component: ComponentCreator('/ai-native-book-course/blog/authors/yangshun', '345'),
    exact: true
  },
  {
    path: '/ai-native-book-course/blog/first-blog-post',
    component: ComponentCreator('/ai-native-book-course/blog/first-blog-post', 'ff4'),
    exact: true
  },
  {
    path: '/ai-native-book-course/blog/long-blog-post',
    component: ComponentCreator('/ai-native-book-course/blog/long-blog-post', 'f3f'),
    exact: true
  },
  {
    path: '/ai-native-book-course/blog/mdx-blog-post',
    component: ComponentCreator('/ai-native-book-course/blog/mdx-blog-post', '6f1'),
    exact: true
  },
  {
    path: '/ai-native-book-course/blog/tags',
    component: ComponentCreator('/ai-native-book-course/blog/tags', 'ddb'),
    exact: true
  },
  {
    path: '/ai-native-book-course/blog/tags/docusaurus',
    component: ComponentCreator('/ai-native-book-course/blog/tags/docusaurus', '004'),
    exact: true
  },
  {
    path: '/ai-native-book-course/blog/tags/facebook',
    component: ComponentCreator('/ai-native-book-course/blog/tags/facebook', '446'),
    exact: true
  },
  {
    path: '/ai-native-book-course/blog/tags/hello',
    component: ComponentCreator('/ai-native-book-course/blog/tags/hello', '466'),
    exact: true
  },
  {
    path: '/ai-native-book-course/blog/tags/hola',
    component: ComponentCreator('/ai-native-book-course/blog/tags/hola', '92d'),
    exact: true
  },
  {
    path: '/ai-native-book-course/blog/welcome',
    component: ComponentCreator('/ai-native-book-course/blog/welcome', 'ac7'),
    exact: true
  },
  {
    path: '/ai-native-book-course/markdown-page',
    component: ComponentCreator('/ai-native-book-course/markdown-page', '23b'),
    exact: true
  },
  {
    path: '/ai-native-book-course/docs',
    component: ComponentCreator('/ai-native-book-course/docs', 'c1e'),
    routes: [
      {
        path: '/ai-native-book-course/docs',
        component: ComponentCreator('/ai-native-book-course/docs', 'cd2'),
        routes: [
          {
            path: '/ai-native-book-course/docs',
            component: ComponentCreator('/ai-native-book-course/docs', 'b5f'),
            routes: [
              {
                path: '/ai-native-book-course/docs/intro',
                component: ComponentCreator('/ai-native-book-course/docs/intro', '4b5'),
                exact: true,
                sidebar: "bookSidebar"
              },
              {
                path: '/ai-native-book-course/docs/module1/nodes',
                component: ComponentCreator('/ai-native-book-course/docs/module1/nodes', '129'),
                exact: true,
                sidebar: "bookSidebar"
              },
              {
                path: '/ai-native-book-course/docs/module1/rclpy-basics',
                component: ComponentCreator('/ai-native-book-course/docs/module1/rclpy-basics', '3b2'),
                exact: true,
                sidebar: "bookSidebar"
              },
              {
                path: '/ai-native-book-course/docs/module1/services',
                component: ComponentCreator('/ai-native-book-course/docs/module1/services', '5a1'),
                exact: true,
                sidebar: "bookSidebar"
              },
              {
                path: '/ai-native-book-course/docs/module1/setup',
                component: ComponentCreator('/ai-native-book-course/docs/module1/setup', '97f'),
                exact: true,
                sidebar: "bookSidebar"
              },
              {
                path: '/ai-native-book-course/docs/module1/topics',
                component: ComponentCreator('/ai-native-book-course/docs/module1/topics', '154'),
                exact: true,
                sidebar: "bookSidebar"
              },
              {
                path: '/ai-native-book-course/docs/module1/urdf-basics',
                component: ComponentCreator('/ai-native-book-course/docs/module1/urdf-basics', 'b67'),
                exact: true,
                sidebar: "bookSidebar"
              },
              {
                path: '/ai-native-book-course/docs/module2/gazebo-digital-twin',
                component: ComponentCreator('/ai-native-book-course/docs/module2/gazebo-digital-twin', 'a35'),
                exact: true,
                sidebar: "bookSidebar"
              },
              {
                path: '/ai-native-book-course/docs/module2/physics-collision',
                component: ComponentCreator('/ai-native-book-course/docs/module2/physics-collision', '872'),
                exact: true,
                sidebar: "bookSidebar"
              },
              {
                path: '/ai-native-book-course/docs/module2/sensor-sim',
                component: ComponentCreator('/ai-native-book-course/docs/module2/sensor-sim', 'e0e'),
                exact: true,
                sidebar: "bookSidebar"
              },
              {
                path: '/ai-native-book-course/docs/module2/setup-gazebo',
                component: ComponentCreator('/ai-native-book-course/docs/module2/setup-gazebo', '114'),
                exact: true,
                sidebar: "bookSidebar"
              },
              {
                path: '/ai-native-book-course/docs/module2/setup-unity',
                component: ComponentCreator('/ai-native-book-course/docs/module2/setup-unity', 'efc'),
                exact: true,
                sidebar: "bookSidebar"
              },
              {
                path: '/ai-native-book-course/docs/module2/unity-hri',
                component: ComponentCreator('/ai-native-book-course/docs/module2/unity-hri', 'a70'),
                exact: true,
                sidebar: "bookSidebar"
              },
              {
                path: '/ai-native-book-course/docs/module3/isaac-ros-perception',
                component: ComponentCreator('/ai-native-book-course/docs/module3/isaac-ros-perception', 'fd3'),
                exact: true,
                sidebar: "bookSidebar"
              },
              {
                path: '/ai-native-book-course/docs/module3/isaac-ros-pipeline',
                component: ComponentCreator('/ai-native-book-course/docs/module3/isaac-ros-pipeline', '747'),
                exact: true,
                sidebar: "bookSidebar"
              },
              {
                path: '/ai-native-book-course/docs/module3/isaac-sim-basics',
                component: ComponentCreator('/ai-native-book-course/docs/module3/isaac-sim-basics', '34c'),
                exact: true,
                sidebar: "bookSidebar"
              },
              {
                path: '/ai-native-book-course/docs/module3/nav2-humanoid-isaac',
                component: ComponentCreator('/ai-native-book-course/docs/module3/nav2-humanoid-isaac', '8ec'),
                exact: true,
                sidebar: "bookSidebar"
              },
              {
                path: '/ai-native-book-course/docs/module3/setup-isaac',
                component: ComponentCreator('/ai-native-book-course/docs/module3/setup-isaac', 'c05'),
                exact: true,
                sidebar: "bookSidebar"
              },
              {
                path: '/ai-native-book-course/docs/module4/capstone-architecture',
                component: ComponentCreator('/ai-native-book-course/docs/module4/capstone-architecture', '43f'),
                exact: true,
                sidebar: "bookSidebar"
              },
              {
                path: '/ai-native-book-course/docs/module4/intro',
                component: ComponentCreator('/ai-native-book-course/docs/module4/intro', '551'),
                exact: true,
                sidebar: "bookSidebar"
              },
              {
                path: '/ai-native-book-course/docs/module4/llm-planning',
                component: ComponentCreator('/ai-native-book-course/docs/module4/llm-planning', '68e'),
                exact: true,
                sidebar: "bookSidebar"
              },
              {
                path: '/ai-native-book-course/docs/module4/ros2-mapping',
                component: ComponentCreator('/ai-native-book-course/docs/module4/ros2-mapping', 'bae'),
                exact: true,
                sidebar: "bookSidebar"
              },
              {
                path: '/ai-native-book-course/docs/module4/whisper-vision',
                component: ComponentCreator('/ai-native-book-course/docs/module4/whisper-vision', '6a0'),
                exact: true,
                sidebar: "bookSidebar"
              },
              {
                path: '/ai-native-book-course/docs/tutorial-basics/congratulations',
                component: ComponentCreator('/ai-native-book-course/docs/tutorial-basics/congratulations', '088'),
                exact: true
              },
              {
                path: '/ai-native-book-course/docs/tutorial-basics/create-a-blog-post',
                component: ComponentCreator('/ai-native-book-course/docs/tutorial-basics/create-a-blog-post', 'f1e'),
                exact: true
              },
              {
                path: '/ai-native-book-course/docs/tutorial-basics/create-a-document',
                component: ComponentCreator('/ai-native-book-course/docs/tutorial-basics/create-a-document', '4e5'),
                exact: true
              },
              {
                path: '/ai-native-book-course/docs/tutorial-basics/create-a-page',
                component: ComponentCreator('/ai-native-book-course/docs/tutorial-basics/create-a-page', 'beb'),
                exact: true
              },
              {
                path: '/ai-native-book-course/docs/tutorial-basics/deploy-your-site',
                component: ComponentCreator('/ai-native-book-course/docs/tutorial-basics/deploy-your-site', 'c35'),
                exact: true
              },
              {
                path: '/ai-native-book-course/docs/tutorial-basics/markdown-features',
                component: ComponentCreator('/ai-native-book-course/docs/tutorial-basics/markdown-features', '5e2'),
                exact: true
              },
              {
                path: '/ai-native-book-course/docs/tutorial-extras/manage-docs-versions',
                component: ComponentCreator('/ai-native-book-course/docs/tutorial-extras/manage-docs-versions', '5d2'),
                exact: true
              },
              {
                path: '/ai-native-book-course/docs/tutorial-extras/translate-your-site',
                component: ComponentCreator('/ai-native-book-course/docs/tutorial-extras/translate-your-site', '2c8'),
                exact: true
              }
            ]
          }
        ]
      }
    ]
  },
  {
    path: '/ai-native-book-course/',
    component: ComponentCreator('/ai-native-book-course/', '282'),
    exact: true
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
