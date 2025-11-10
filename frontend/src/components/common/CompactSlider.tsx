/**
 * CompactSlider Component
 *
 * Bidirectional slider for Expert Mode (-100% to +100%)
 * Key Feature: Center at 0%, visual distinction for negative/positive
 *
 * Visual:
 * Negative (Blue) │ Center (White) │ Positive (Orange)
 * ◄────────────●────────────────►
 * -100%        0%               +100%
 *
 * Version: v0.1.0
 * WCAG 2.1 AA Compliant
 */

import React, { useId } from 'react';
import './CompactSlider.css';

export interface CompactSliderProps {
  // Value
  min: number;                          // Typically -100
  max: number;                          // Typically +100
  value: number;                        // Current value
  centerValue?: number;                 // Center point (default: 0)

  // Appearance
  height?: number;                      // Track height (default: 6px)
  negativeColor?: string;               // Color for negative range
  positiveColor?: string;               // Color for positive range
  centerColor?: string;                 // Color at center

  // Labels
  label?: string;                       // Parameter label (e.g., "ae")
  unit?: string;                        // Unit (e.g., "mm", "%")
  showValue?: boolean;                  // Show numeric value

  // Behavior
  onChange: (value: number) => void;
  disabled?: boolean;
  step?: number;                        // Default: 1

  // Accessibility
  ariaLabel?: string;
  id?: string;
}

export const CompactSlider: React.FC<CompactSliderProps> = ({
  min,
  max,
  value,
  centerValue = 0,
  height,
  negativeColor = '#3b82f6',
  positiveColor = '#f97316',
  centerColor = '#ffffff',
  label,
  unit = '%',
  showValue = true,
  onChange,
  disabled = false,
  step = 1,
  ariaLabel,
  id: providedId,
}) => {
  const autoId = useId();
  const id = providedId || autoId;

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = Number(e.target.value);
    onChange(newValue);
  };

  // Calculate fill percentage and direction
  const range = max - min;
  const centerPercentage = ((centerValue - min) / range) * 100;
  const valuePercentage = ((value - min) / range) * 100;

  const isNegative = value < centerValue;
  const isPositive = value > centerValue;
  const isCentered = value === centerValue;

  // Fill bar styling
  let fillLeft: number;
  let fillWidth: number;
  let fillColor: string;

  if (isCentered) {
    fillLeft = centerPercentage;
    fillWidth = 0;
    fillColor = centerColor;
  } else if (isNegative) {
    fillLeft = valuePercentage;
    fillWidth = centerPercentage - valuePercentage;
    fillColor = negativeColor;
  } else {
    fillLeft = centerPercentage;
    fillWidth = valuePercentage - centerPercentage;
    fillColor = positiveColor;
  }

  const formatValue = (v: number): string => {
    const sign = v > 0 ? '+' : '';
    return `${sign}${v}${unit}`;
  };

  const sliderClasses = [
    'compact-slider',
    disabled && 'compact-slider--disabled',
  ]
    .filter(Boolean)
    .join(' ');

  return (
    <div className={sliderClasses}>
      {/* Label and value */}
      {(label || showValue) && (
        <div className="compact-slider__header">
          {label && <span className="compact-slider__label">{label}</span>}
          {showValue && (
            <span
              className={`compact-slider__value ${
                isNegative
                  ? 'compact-slider__value--negative'
                  : isPositive
                  ? 'compact-slider__value--positive'
                  : 'compact-slider__value--center'
              }`}
              aria-live="polite"
            >
              {formatValue(value)}
            </span>
          )}
        </div>
      )}

      {/* Slider track container */}
      <div className="compact-slider__container">
        {/* Background track */}
        <div
          className="compact-slider__track"
          style={{
            height: height ? `${height}px` : undefined,
          }}
        >
          {/* Center marker */}
          <div
            className="compact-slider__center-marker"
            style={{ left: `${centerPercentage}%` }}
          />

          {/* Fill bar */}
          {!isCentered && (
            <div
              className="compact-slider__fill"
              style={{
                left: `${fillLeft}%`,
                width: `${fillWidth}%`,
                backgroundColor: fillColor,
              }}
            />
          )}
        </div>

        {/* HTML range input */}
        <input
          type="range"
          id={id}
          className="compact-slider__input"
          min={min}
          max={max}
          value={value}
          step={step}
          onChange={handleChange}
          disabled={disabled}
          aria-label={ariaLabel || label || 'Compact slider'}
          aria-valuemin={min}
          aria-valuemax={max}
          aria-valuenow={value}
          aria-valuetext={formatValue(value)}
        />
      </div>

      {/* Range labels */}
      <div className="compact-slider__range-labels">
        <span className="compact-slider__range-label">{formatValue(min)}</span>
        <span className="compact-slider__range-label compact-slider__range-label--center">
          {formatValue(centerValue)}
        </span>
        <span className="compact-slider__range-label">{formatValue(max)}</span>
      </div>

      {/* Screen reader helper text */}
      <div className="visually-hidden" aria-live="polite">
        {label && `${label}: `}
        {formatValue(value)}
      </div>
    </div>
  );
};

CompactSlider.displayName = 'CompactSlider';

export default CompactSlider;
