import React from 'react';
import styles from './styles.module.css';
import clsx from 'clsx';

interface Props {
  type: 'info' | 'warning' | 'note';
  children: React.ReactNode;
}

export default function CalloutBox({ type, children }: Props): JSX.Element {
  return (
    <div className={clsx(styles.container, styles[type])}>
      {children}
    </div>
  );
}