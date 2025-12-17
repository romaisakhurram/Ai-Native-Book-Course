import React from 'react';
import styles from './styles.module.css';

interface Props {
  src: string;
  alt: string;
  caption: string;
}

export default function ImageWithCaption({ src, alt, caption }: Props): JSX.Element {
  return (
    <figure className={styles.container}>
      <img src={src} alt={alt} className={styles.image} />
      <figcaption className={styles.caption}>{caption}</figcaption>
    </figure>
  );
}