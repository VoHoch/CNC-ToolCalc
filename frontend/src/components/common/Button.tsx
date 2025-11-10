/**
 * Button Component
 *
 * Consistent button styling across app
 * Variants: primary, secondary, ghost, danger
 *
 * Version: v0.1.0
 * WCAG 2.1 AA Compliant
 */

import React from 'react';
import './Button.css';

export interface ButtonProps {
  children: React.ReactNode;
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger';
  size?: 'small' | 'medium' | 'large';
  fullWidth?: boolean;
  disabled?: boolean;
  loading?: boolean;
  onClick?: () => void;
  type?: 'button' | 'submit' | 'reset';
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
}

export const Button: React.FC<ButtonProps> = ({
  children,
  variant = 'primary',
  size = 'medium',
  fullWidth = false,
  disabled = false,
  loading = false,
  onClick,
  type = 'button',
  leftIcon,
  rightIcon,
}) => {
  const classNames = [
    'button',
    `button--${variant}`,
    `button--${size}`,
    fullWidth && 'button--full-width',
    disabled && 'button--disabled',
    loading && 'button--loading',
  ]
    .filter(Boolean)
    .join(' ');

  return (
    <button
      type={type}
      className={classNames}
      onClick={onClick}
      disabled={disabled || loading}
    >
      {leftIcon && <span className="button__icon button__icon--left">{leftIcon}</span>}
      {loading ? 'Loading...' : children}
      {rightIcon && <span className="button__icon button__icon--right">{rightIcon}</span>}
    </button>
  );
};
