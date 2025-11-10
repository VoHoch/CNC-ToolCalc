/**
 * Slider Component
 *
 * Marker-based slider with gradient background (Blue → Green → Red)
 * Key Feature: NO visible thumb - uses markers instead
 *
 * Version: v0.1.0
 * WCAG 2.1 AA Compliant
 */

import React, { useId } from 'react';
import './Slider.css';

export interface MarkerDefinition {
  value: number;
  label: string;
  color?: string;
  active?: boolean;
}

export interface SliderProps {
  // Value
  min: number;
  max: number;
  value: number;
  defaultValue?: number;

  // Markers
  markers: MarkerDefinition[];

  // Appearance
  gradient?: [string, string, string]; // [start, middle, end] colors
  trackHeight?: number;                // Track height in px (default: 8)

  // Labels
  showValue?: boolean;
  valueFormatter?: (value: number) => string;
  leftLabel?: string;
  rightLabel?: string;

  // Behavior
  onChange: (value: number) => void;
  onChangeCommitted?: (value: number) => void;
  disabled?: boolean;
  step?: number;

  // Compact Mode
  compact?: boolean;

  // Accessibility
  ariaLabel?: string;
  id?: string;
}

export const Slider: React.FC<SliderProps> = ({
  min,
  max,
  value,
  markers,
  gradient = ['#3b82f6', '#22c55e', '#ef4444'],
  trackHeight,
  showValue = false,
  valueFormatter = (v) => v.toString(),
  leftLabel,
  rightLabel,
  onChange,
  onChangeCommitted,
  disabled = false,
  step = 1,
  compact = false,
  ariaLabel,
  id: providedId,
}) => {
  const autoId = useId();
  const id = providedId || autoId;

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = Number(e.target.value);
    onChange(newValue);
  };

  const handleMouseUp = () => {
    if (onChangeCommitted) {
      onChangeCommitted(value);
    }
  };

  const handleKeyUp = (e: React.KeyboardEvent<HTMLInputElement>) => {
    // Commit value on Enter or when arrow keys are released
    if (e.key === 'Enter' || e.key.startsWith('Arrow')) {
      if (onChangeCommitted) {
        onChangeCommitted(value);
      }
    }
  };

  // Calculate marker positions
  const getMarkerPosition = (markerValue: number): number => {
    return ((markerValue - min) / (max - min)) * 100;
  };

  const sliderClasses = [
    'slider',
    compact && 'slider--compact',
    disabled && 'slider--disabled',
  ]
    .filter(Boolean)
    .join(' ');

  return (
    <div className={sliderClasses}>
      {/* Top labels */}
      {(showValue || leftLabel || rightLabel) && (
        <div className="slider__labels">
          {leftLabel && <span className="slider__label slider__label--left">{leftLabel}</span>}
          {showValue && (
            <span className="slider__value" aria-live="polite">
              {valueFormatter(value)}
            </span>
          )}
          {rightLabel && <span className="slider__label slider__label--right">{rightLabel}</span>}
        </div>
      )}

      {/* Slider track container */}
      <div className="slider__container">
        {/* Gradient track overlay */}
        <div
          className="slider__track"
          style={{
            background: `linear-gradient(to right, ${gradient[0]}, ${gradient[1]}, ${gradient[2]})`,
            height: trackHeight ? `${trackHeight}px` : undefined,
          }}
        />

        {/* HTML range input (with invisible thumb) */}
        <input
          type="range"
          id={id}
          className="slider__input"
          min={min}
          max={max}
          value={value}
          step={step}
          onChange={handleChange}
          onMouseUp={handleMouseUp}
          onKeyUp={handleKeyUp}
          disabled={disabled}
          aria-label={ariaLabel || 'Slider'}
          aria-valuemin={min}
          aria-valuemax={max}
          aria-valuenow={value}
          aria-valuetext={valueFormatter(value)}
        />

        {/* Markers overlay */}
        <div className="slider__markers" aria-hidden="true">
          {markers.map((marker, index) => {
            const position = getMarkerPosition(marker.value);
            const isActive = value === marker.value;

            return (
              <div
                key={`${marker.value}-${index}`}
                className={`slider__marker ${isActive ? 'slider__marker--active' : ''}`}
                style={{
                  left: `${position}%`,
                  backgroundColor: marker.color,
                }}
              >
                <span className="slider__marker-label">{marker.label}</span>
              </div>
            );
          })}
        </div>
      </div>

      {/* Screen reader helper text */}
      <div className="visually-hidden" aria-live="polite">
        Current value: {valueFormatter(value)}
      </div>
    </div>
  );
};

Slider.displayName = 'Slider';

export default Slider;
