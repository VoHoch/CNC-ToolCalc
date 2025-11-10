import React, { useState, useEffect } from 'react';
import { useToolStore } from '@/state/toolStore';
import { useMaterialStore } from '@/state/materialStore';
import { Card, Button } from '@/components/common';
import { apiClient } from '@/api/client';

interface MaterialSelectionProps {
  onNext: () => void;
  onBack: () => void;
}

export const MaterialSelection: React.FC<MaterialSelectionProps> = ({ onNext, onBack }) => {
  const { selectedToolIds, allTools } = useToolStore();
  const { materialsByTool, allMaterials, loadMaterials, toggleMaterialForTool } = useMaterialStore();
  const [currentToolIndex, setCurrentToolIndex] = useState(0);

  useEffect(() => {
    apiClient.getMaterials().then(res => loadMaterials(res.materials));
  }, []);

  const currentToolId = selectedToolIds[currentToolIndex];
  const currentMaterials = materialsByTool[currentToolId] || [];

  return (
    <div className="screen">
      <h2>Material Selection (Per Tool)</h2>
      {selectedToolIds.length > 1 && (
        <div className="tool-tabs">
          {selectedToolIds.map((id, i) => (
            <button
              key={id}
              className={i === currentToolIndex ? 'active' : ''}
              onClick={() => setCurrentToolIndex(i)}
            >
              {allTools.find(t => t.id === id)?.name}
            </button>
          ))}
        </div>
      )}
      <div className="material-grid">
        {allMaterials.map((mat) => (
          <Card
            key={mat.id}
            clickable
            selected={currentMaterials.includes(mat.id)}
            onClick={() => toggleMaterialForTool(currentToolId, mat.id)}
          >
            <h3>{mat.name}</h3>
            <p>Hardness: {mat.hardness_order}/7</p>
          </Card>
        ))}
      </div>
      <Button onClick={onBack}>Back</Button>
      <Button onClick={onNext}>Next: Operations</Button>
    </div>
  );
};
