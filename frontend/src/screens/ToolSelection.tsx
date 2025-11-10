import React from 'react';
import { useToolStore } from '@/state/toolStore';
import { Card, Button } from '@/components/common';
import './ToolSelection.css';

interface ToolSelectionProps {
  onNext: () => void;
}

export const ToolSelection: React.FC<ToolSelectionProps> = ({ onNext }) => {
  const { allTools, selectedToolIds, toggleTool } = useToolStore();

  const handleNext = () => {
    if (selectedToolIds.length === 0) {
      alert('Please select at least one tool to continue');
      return;
    }
    onNext();
  };

  if (allTools.length === 0) {
    return (
      <div className="screen tool-selection">
        <div className="screen__header">
          <h2>Select Tools to Work With</h2>
          <p className="screen__description">
            No tools loaded. Please import a Fusion 360 .tools file or tool library.
          </p>
        </div>

        <div className="tool-selection__empty">
          <p>Import your tools to get started</p>
          <Button variant="primary">Import Tools</Button>
        </div>
      </div>
    );
  }

  return (
    <div className="screen tool-selection">
      <div className="screen__header">
        <h2>Select Tools to Work With</h2>
        <p className="screen__description">
          Choose one or more cutting tools for your operations. You can select multiple tools to calculate parameters for different configurations.
        </p>
      </div>

      <div className="tool-grid">
        {allTools.map((tool) => {
          const isSelected = selectedToolIds.includes(tool.id);

          return (
            <Card
              key={tool.id}
              variant="bordered"
              hoverable
              clickable
              selected={isSelected}
              onClick={() => toggleTool(tool.id)}
            >
              <div className="tool-card__content">
                <div className="tool-card__header">
                  <h3 className="tool-card__title">{tool.name}</h3>
                  {isSelected && (
                    <span className="tool-card__badge">Selected</span>
                  )}
                </div>

                <div className="tool-card__details">
                  <div className="tool-card__detail">
                    <span className="tool-card__label">Type:</span>
                    <span className="tool-card__value">{tool.type}</span>
                  </div>
                  <div className="tool-card__detail">
                    <span className="tool-card__label">DC:</span>
                    <span className="tool-card__value">{tool.geometry.DC} mm</span>
                  </div>
                  <div className="tool-card__detail">
                    <span className="tool-card__label">LCF:</span>
                    <span className="tool-card__value">{tool.geometry.LCF} mm</span>
                  </div>
                  <div className="tool-card__detail">
                    <span className="tool-card__label">Flutes:</span>
                    <span className="tool-card__value">{tool.geometry.NOF}</span>
                  </div>
                  <div className="tool-card__detail">
                    <span className="tool-card__label">L/D Ratio:</span>
                    <span className="tool-card__value">
                      {tool.ld_ratio.toFixed(2)} ({tool.ld_classification})
                    </span>
                  </div>
                </div>

                {tool.presets && tool.presets.length > 0 && (
                  <div className="tool-card__presets">
                    <span className="tool-card__presets-count">
                      {tool.presets.length} preset{tool.presets.length !== 1 ? 's' : ''} available
                    </span>
                  </div>
                )}
              </div>
            </Card>
          );
        })}
      </div>

      <div className="screen__sidebar">
        <div className="selection-summary">
          <h4>Selection Summary</h4>
          <p className="selection-summary__count">
            {selectedToolIds.length} tool{selectedToolIds.length !== 1 ? 's' : ''} selected
          </p>
          {selectedToolIds.length > 0 && (
            <ul className="selection-summary__list">
              {selectedToolIds.map((toolId) => {
                const tool = allTools.find((t) => t.id === toolId);
                return tool ? (
                  <li key={toolId}>
                    {tool.name} (DC: {tool.geometry.DC}mm)
                  </li>
                ) : null;
              })}
            </ul>
          )}
        </div>
      </div>

      <div className="screen__footer">
        <Button
          variant="primary"
          onClick={handleNext}
          disabled={selectedToolIds.length === 0}
        >
          Next: Material Selection
        </Button>
      </div>
    </div>
  );
};

export default ToolSelection;
