import React from 'react';

export interface CardProps {
  children: React.ReactNode;
  clickable?: boolean;
  selected?: boolean;
  onClick?: () => void;
}

export const Card: React.FC<CardProps> = ({ children, clickable, selected, onClick }) => {
  return (
    <div
      className={`card ${clickable ? 'card--clickable' : ''} ${selected ? 'card--selected' : ''}`}
      onClick={onClick}
      style={{
        padding: '16px',
        borderRadius: '8px',
        border: selected ? '2px solid #6366f1' : '1px solid rgba(255,255,255,0.12)',
        backgroundColor: '#12161d',
        cursor: clickable ? 'pointer' : 'default',
      }}
    >
      {children}
    </div>
  );
};
