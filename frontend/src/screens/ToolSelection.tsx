import React from 'react';
import { useToolStore } from '@/state/toolStore';
import { Card, Button } from '@/components/common';

interface ToolSelectionProps {
  onNext: () => void;
}

export const ToolSelection: React.FC<ToolSelectionProps> = ({ onNext }) => {
  const { allTools, selectedToolIds, toggleTool } = useToolStore();

  return (
    <div className="screen">
      <h2>Select Tools</h2>
      <div className="tool-grid">
        {allTools.map((tool) => (
          <Card
            key={tool.id}
            clickable
            selected={selectedToolIds.includes(tool.id)}
            onClick={() => toggleTool(tool.id)}
          >
            <h3>{tool.name}</h3>
            <p>DC: {tool.geometry.DC}mm, LCF: {tool.geometry.LCF}mm</p>
            <p>L/D: {tool.ld_ratio.toFixed(2)} ({tool.ld_classification})</p>
          </Card>
        ))}
      </div>
      <Button onClick={onNext} disabled={selectedToolIds.length === 0}>
        Next: Materials
      </Button>
    </div>
  );
};
