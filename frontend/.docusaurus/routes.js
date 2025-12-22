import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/__docusaurus/debug',
    component: ComponentCreator('/__docusaurus/debug', '5ff'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/config',
    component: ComponentCreator('/__docusaurus/debug/config', '5ba'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/content',
    component: ComponentCreator('/__docusaurus/debug/content', 'a2b'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/globalData',
    component: ComponentCreator('/__docusaurus/debug/globalData', 'c3c'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/metadata',
    component: ComponentCreator('/__docusaurus/debug/metadata', '156'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/registry',
    component: ComponentCreator('/__docusaurus/debug/registry', '88c'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/routes',
    component: ComponentCreator('/__docusaurus/debug/routes', '000'),
    exact: true
  },
  {
    path: '/blog',
    component: ComponentCreator('/blog', 'b2f'),
    exact: true
  },
  {
    path: '/blog/archive',
    component: ComponentCreator('/blog/archive', '182'),
    exact: true
  },
  {
    path: '/blog/authors',
    component: ComponentCreator('/blog/authors', '0b7'),
    exact: true
  },
  {
    path: '/blog/authors/all-sebastien-lorber-articles',
    component: ComponentCreator('/blog/authors/all-sebastien-lorber-articles', '4a1'),
    exact: true
  },
  {
    path: '/blog/authors/yangshun',
    component: ComponentCreator('/blog/authors/yangshun', 'a68'),
    exact: true
  },
  {
    path: '/blog/first-blog-post',
    component: ComponentCreator('/blog/first-blog-post', '89a'),
    exact: true
  },
  {
    path: '/blog/long-blog-post',
    component: ComponentCreator('/blog/long-blog-post', '9ad'),
    exact: true
  },
  {
    path: '/blog/mdx-blog-post',
    component: ComponentCreator('/blog/mdx-blog-post', 'e9f'),
    exact: true
  },
  {
    path: '/blog/tags',
    component: ComponentCreator('/blog/tags', '287'),
    exact: true
  },
  {
    path: '/blog/tags/docusaurus',
    component: ComponentCreator('/blog/tags/docusaurus', '704'),
    exact: true
  },
  {
    path: '/blog/tags/facebook',
    component: ComponentCreator('/blog/tags/facebook', '858'),
    exact: true
  },
  {
    path: '/blog/tags/hello',
    component: ComponentCreator('/blog/tags/hello', '299'),
    exact: true
  },
  {
    path: '/blog/tags/hola',
    component: ComponentCreator('/blog/tags/hola', '00d'),
    exact: true
  },
  {
    path: '/blog/welcome',
    component: ComponentCreator('/blog/welcome', 'd2b'),
    exact: true
  },
  {
    path: '/markdown-page',
    component: ComponentCreator('/markdown-page', '3d7'),
    exact: true
  },
  {
    path: '/docs',
    component: ComponentCreator('/docs', 'c36'),
    routes: [
      {
        path: '/docs',
        component: ComponentCreator('/docs', '792'),
        routes: [
          {
            path: '/docs',
            component: ComponentCreator('/docs', '0ac'),
            routes: [
              {
                path: '/docs/intro',
                component: ComponentCreator('/docs/intro', 'cda'),
                exact: true,
                sidebar: "bookSidebar"
              },
              {
                path: '/docs/module1/nodes',
                component: ComponentCreator('/docs/module1/nodes', '716'),
                exact: true,
                sidebar: "bookSidebar"
              },
              {
                path: '/docs/module1/rclpy-basics',
                component: ComponentCreator('/docs/module1/rclpy-basics', 'd40'),
                exact: true,
                sidebar: "bookSidebar"
              },
              {
                path: '/docs/module1/services',
                component: ComponentCreator('/docs/module1/services', '2e3'),
                exact: true,
                sidebar: "bookSidebar"
              },
              {
                path: '/docs/module1/setup',
                component: ComponentCreator('/docs/module1/setup', 'fec'),
                exact: true,
                sidebar: "bookSidebar"
              },
              {
                path: '/docs/module1/topics',
                component: ComponentCreator('/docs/module1/topics', 'e2c'),
                exact: true,
                sidebar: "bookSidebar"
              },
              {
                path: '/docs/module1/urdf-basics',
                component: ComponentCreator('/docs/module1/urdf-basics', '77b'),
                exact: true,
                sidebar: "bookSidebar"
              },
              {
                path: '/docs/module2/gazebo-digital-twin',
                component: ComponentCreator('/docs/module2/gazebo-digital-twin', 'f7a'),
                exact: true,
                sidebar: "bookSidebar"
              },
              {
                path: '/docs/module2/physics-collision',
                component: ComponentCreator('/docs/module2/physics-collision', 'c4b'),
                exact: true,
                sidebar: "bookSidebar"
              },
              {
                path: '/docs/module2/sensor-sim',
                component: ComponentCreator('/docs/module2/sensor-sim', 'd39'),
                exact: true,
                sidebar: "bookSidebar"
              },
              {
                path: '/docs/module2/setup-gazebo',
                component: ComponentCreator('/docs/module2/setup-gazebo', 'fc0'),
                exact: true,
                sidebar: "bookSidebar"
              },
              {
                path: '/docs/module2/setup-unity',
                component: ComponentCreator('/docs/module2/setup-unity', 'f44'),
                exact: true,
                sidebar: "bookSidebar"
              },
              {
                path: '/docs/module2/unity-hri',
                component: ComponentCreator('/docs/module2/unity-hri', 'e3a'),
                exact: true,
                sidebar: "bookSidebar"
              },
              {
                path: '/docs/module3/isaac-ros-perception',
                component: ComponentCreator('/docs/module3/isaac-ros-perception', '349'),
                exact: true,
                sidebar: "bookSidebar"
              },
              {
                path: '/docs/module3/isaac-ros-pipeline',
                component: ComponentCreator('/docs/module3/isaac-ros-pipeline', '201'),
                exact: true,
                sidebar: "bookSidebar"
              },
              {
                path: '/docs/module3/isaac-sim-basics',
                component: ComponentCreator('/docs/module3/isaac-sim-basics', 'b74'),
                exact: true,
                sidebar: "bookSidebar"
              },
              {
                path: '/docs/module3/nav2-humanoid-isaac',
                component: ComponentCreator('/docs/module3/nav2-humanoid-isaac', '4cf'),
                exact: true,
                sidebar: "bookSidebar"
              },
              {
                path: '/docs/module3/setup-isaac',
                component: ComponentCreator('/docs/module3/setup-isaac', '3c2'),
                exact: true,
                sidebar: "bookSidebar"
              },
              {
                path: '/docs/module4/capstone-architecture',
                component: ComponentCreator('/docs/module4/capstone-architecture', 'dc9'),
                exact: true,
                sidebar: "bookSidebar"
              },
              {
                path: '/docs/module4/intro',
                component: ComponentCreator('/docs/module4/intro', '0d4'),
                exact: true,
                sidebar: "bookSidebar"
              },
              {
                path: '/docs/module4/llm-planning',
                component: ComponentCreator('/docs/module4/llm-planning', '79d'),
                exact: true,
                sidebar: "bookSidebar"
              },
              {
                path: '/docs/module4/ros2-mapping',
                component: ComponentCreator('/docs/module4/ros2-mapping', '7b6'),
                exact: true,
                sidebar: "bookSidebar"
              },
              {
                path: '/docs/module4/whisper-vision',
                component: ComponentCreator('/docs/module4/whisper-vision', 'b66'),
                exact: true,
                sidebar: "bookSidebar"
              },
              {
                path: '/docs/tutorial-basics/congratulations',
                component: ComponentCreator('/docs/tutorial-basics/congratulations', '70e'),
                exact: true
              },
              {
                path: '/docs/tutorial-basics/create-a-blog-post',
                component: ComponentCreator('/docs/tutorial-basics/create-a-blog-post', '315'),
                exact: true
              },
              {
                path: '/docs/tutorial-basics/create-a-document',
                component: ComponentCreator('/docs/tutorial-basics/create-a-document', 'f86'),
                exact: true
              },
              {
                path: '/docs/tutorial-basics/create-a-page',
                component: ComponentCreator('/docs/tutorial-basics/create-a-page', '9f6'),
                exact: true
              },
              {
                path: '/docs/tutorial-basics/deploy-your-site',
                component: ComponentCreator('/docs/tutorial-basics/deploy-your-site', 'b91'),
                exact: true
              },
              {
                path: '/docs/tutorial-basics/markdown-features',
                component: ComponentCreator('/docs/tutorial-basics/markdown-features', '272'),
                exact: true
              },
              {
                path: '/docs/tutorial-extras/manage-docs-versions',
                component: ComponentCreator('/docs/tutorial-extras/manage-docs-versions', 'a34'),
                exact: true
              },
              {
                path: '/docs/tutorial-extras/translate-your-site',
                component: ComponentCreator('/docs/tutorial-extras/translate-your-site', '739'),
                exact: true
              }
            ]
          }
        ]
      }
    ]
  },
  {
    path: '/',
    component: ComponentCreator('/', 'e5f'),
    exact: true
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
