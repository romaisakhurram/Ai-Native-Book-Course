
import React, { JSX } from 'react';
import {clsx} from 'clsx';
import Link from '@docusaurus/Link';
import styles from './styles.module.css';

interface Props {
  title: string;
  description: string;
  link: string;
  imageUrl?: string;
}

export default function ModuleCard({ title, description, link }: Props): JSX.Element {
  return (
    <Link to={`/docs/${link}`} className={clsx('card', styles.moduleCard)}>
      <div className={styles.cardContent}>
        <h3>📚{title}</h3>
        <p>{description}</p>
        <div className={styles.cardFooter}>
          <span className="button button--outline button--sm">
            Explore Module
          </span>
        </div>
      </div>
    </Link>
  );
}
