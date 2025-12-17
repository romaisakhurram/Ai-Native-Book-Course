
import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import styles from './styles.module.css';

interface Props {
  title: string;
  subtitle: string;
  ctaText: string;
  ctaLink: string;
  imageUrl?: string;
}

export default function Hero({ title, subtitle, ctaText, ctaLink, imageUrl }: Props): JSX.Element {
  const backgroundImageStyle = imageUrl ? {
    backgroundImage: `url(${imageUrl})`
  } : {};

  return (
    <header
      className={clsx('hero hero--primary', styles.heroBanner)}
      style={backgroundImageStyle}
    >
      <div className={styles.heroBannerContainer}>
        <h1 className="hero__title">{title}</h1>
        <p className="hero__subtitle">{subtitle}</p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to={ctaLink}>
            {ctaText}
          </Link>
          <Link
            className="button button--primary button--lg"
            to="/docs/intro">
            Explore Course
          </Link>
        </div>
      </div>
    </header>
  );
}
