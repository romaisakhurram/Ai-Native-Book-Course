import React from 'react';
import type {ReactNode} from 'react';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Hero from '@site/src/components/Hero';
import ModuleCard from '@site/src/components/ModuleCard';
import clsx from 'clsx';

import styles from './index.module.css';

const MODULES = [
  {
    title: 'Module 1: ROS2 Basics',
    // imageUrl: 'img/Cute astronaut read a book icon illustration _ Free Vector.mhtml', // Replace with actual image path
    description: 'Learn the fundamentals of ROS2, including nodes, topics, and services.',
    link: '/docs/module1/00-setup',
  },
  {
    title: 'Module 2: Digital Twin Simulation',
    // imageUrl: 'img/Cute astronaut reading book cartoon vector icon illustration science education isolated flat vector _ Free Vector.mhtml',  Replace with actual image path
    description: 'Explore Gazebo and Unity for realistic robotics simulation.',
    link: '/docs/module2/00-setup-gazebo',
  },
  {
    title: 'Module 3: Isaac Perception & Navigation',
    // imageUrl: 'img/Flat artificial intelligence background _ Free Vector.mhtml',
    description: 'Dive into NVIDIA Isaac Sim for advanced robotics perception and navigation.',
    link: '/docs/module3/00-setup-isaac',
  },
   {
    title: 'Module 4: Advanced AI & Integration',
    // imageUrl: 'img/Machine learning book _ Free Vector.mhtml',
    description: 'Integrate learning-based perception, planning, and cloud native AI workflows.',
    link: '/docs/module4/00-introduction',
  },
];

function HomepageContent() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <main>
      <Hero
        title={siteConfig.title}
        subtitle={siteConfig.tagline}
        ctaText="START READING ⏱️"
        ctaLink="/docs/intro"
        imageUrl="img/stock-photo-cute-blue-robot-waving-hand-d-rendering-illustration-isolated-on-white-background-2056356791.jpg" // Replace with actual hero image path
      />

      <section className={styles.modules}>
        <div className="container">
          <div className="row">
            {MODULES.map((module, idx) => (
              <div key={idx} className={clsx('col col--4', styles.moduleCardCol)}>
                <ModuleCard {...module} />
              </div>
            ))}
          </div>
        </div>
      </section>
    </main>
  );
}

export default function Home(): ReactNode {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Hello from ${siteConfig.title}`}
      description="Description will go into a meta tag in <head />">
      <HomepageContent />
    </Layout>
  );
}
