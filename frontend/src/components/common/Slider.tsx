import React from 'react';

export interface MarkerDefinition {
  value: number;
  label: string;
}

export interface SliderProps {
  min: number;
  max: number;
  value: number;
  onChange: (value: number) => void;
  markers: MarkerDefinition[];
}

export const Slider: React.FC<SliderProps> = ({ min, max, value, onChange, markers }) => {
  return (
    <div style={{ padding: '20px' }}>
      <input
        type="range"
        min={min}
        max={max}
        value={value}
        onChange={(e) => onChange(Number(e.target.value))}
        style={{ width: '100%' }}
      />
      <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '8px' }}>
        {markers.map((m, i) => (
          <span key={i} style={{ fontSize: '12px', color: '#aaa' }}>
            {m.label}
          </span>
        ))}
      </div>
    </div>
  );
};
