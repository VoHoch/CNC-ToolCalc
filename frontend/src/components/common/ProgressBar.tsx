/**
 * ProgressBar Component
 *
 * Real-time calculation progress indicator
 * Features: step counter, percentage, animated
 *
 * Version: v0.1.0
 * WCAG 2.1 AA Compliant
 */

import React from 'react';
import './ProgressBar.css';

export interface ProgressBarProps {
  current: number;
  total: number;
  currentStepLabel?: string;
  showPercentage?: boolean;
  height?: number;
  color?: string;
  animated?: boolean;
}

export const ProgressBar: React.FC<ProgressBarProps> = ({
  current,
  total,
  currentStepLabel,
  showPercentage = false,
  height = 8,
  color = 'var(--accent-primary)',
  animated = true,
}) => {
  const percentage = Math.min(100, Math.max(0, (current / total) * 100));

  return (
    <div className="progress-bar">
      {(currentStepLabel || showPercentage) && (
        <div className="progress-bar__header">
          {currentStepLabel && (
            <div className="progress-bar__label">{currentStepLabel}</div>
          )}
          {showPercentage && (
            <div className="progress-bar__percentage">{Math.round(percentage)}%</div>
          )}
        </div>
      )}

      <div
        className="progress-bar__track"
        style={{ height: `${height}px` }}
      >
        <div
          className={`progress-bar__fill ${animated ? 'progress-bar__fill--animated' : ''}`}
          style={{
            width: `${percentage}%`,
            backgroundColor: color,
          }}
        />
      </div>

      {total > 0 && (
        <div className="progress-bar__steps">
          {current} / {total}
        </div>
      )}
    </div>
  );
};
