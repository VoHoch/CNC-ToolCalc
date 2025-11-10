/**
 * Card Component
 *
 * Container for tool/material/operation cards
 * Features: title/subtitle, hoverable, clickable, selectable
 *
 * Version: v0.1.0
 * WCAG 2.1 AA Compliant
 */

import React from 'react';
import './Card.css';

export interface CardProps {
  title?: string;
  subtitle?: string;
  children: React.ReactNode;
  footer?: React.ReactNode;
  variant?: 'default' | 'bordered' | 'elevated';
  padding?: 'none' | 'small' | 'medium' | 'large';
  hoverable?: boolean;
  clickable?: boolean;
  onClick?: () => void;
  selected?: boolean;
  icon?: React.ReactNode;
  badge?: string | number;
}

export const Card: React.FC<CardProps> = ({
  title,
  subtitle,
  children,
  footer,
  variant = 'default',
  padding = 'medium',
  hoverable = false,
  clickable = false,
  onClick,
  selected = false,
  icon,
  badge,
}) => {
  const classNames = [
    'card',
    `card--${variant}`,
    `card--padding-${padding}`,
    hoverable && 'card--hoverable',
    clickable && 'card--clickable',
    selected && 'card--selected',
  ]
    .filter(Boolean)
    .join(' ');

  const handleClick = () => {
    if (clickable && onClick) {
      onClick();
    }
  };

  return (
    <div className={classNames} onClick={handleClick}>
      {(title || icon || badge) && (
        <div className="card__header">
          {icon && <div className="card__icon">{icon}</div>}
          <div className="card__title-section">
            {title && <h3 className="card__title">{title}</h3>}
            {subtitle && <p className="card__subtitle">{subtitle}</p>}
          </div>
          {badge !== undefined && <div className="card__badge">{badge}</div>}
        </div>
      )}

      <div className="card__content">{children}</div>

      {footer && <div className="card__footer">{footer}</div>}
    </div>
  );
};
