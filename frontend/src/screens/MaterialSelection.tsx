import React, { useState, useEffect } from 'react';
import { useToolStore } from '@/state/toolStore';
import { useMaterialStore } from '@/state/materialStore';
import { Card, Button } from '@/components/common';
import { apiClient } from '@/api/client';
import type { Material } from '@/types/api';
import './MaterialSelection.css';

interface MaterialSelectionProps {
  onNext: () => void;
  onBack: () => void;
}

export const MaterialSelection: React.FC<MaterialSelectionProps> = ({
  onNext,
  onBack,
}) => {
  const { selectedToolIds, allTools } = useToolStore();
  const {
    materialsByTool,
    allMaterials,
    loadMaterials,
    toggleMaterialForTool,
  } = useMaterialStore();

  const [currentToolIndex, setCurrentToolIndex] = useState(0);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Load materials from API
    const fetchMaterials = async () => {
      setLoading(true);
      try {
        const response = await apiClient.getMaterials();
        loadMaterials(response.materials);
      } catch (error) {
        console.error('Failed to load materials:', error);
      } finally {
        setLoading(false);
      }
    };

    if (allMaterials.length === 0) {
      fetchMaterials();
    }
  }, []);

  const currentToolId = selectedToolIds[currentToolIndex];
  const currentTool = allTools.find((t) => t.id === currentToolId);
  const currentMaterials = materialsByTool[currentToolId] || [];

  const handleNext = () => {
    // Check if at least one material is selected for all tools
    const allToolsHaveMaterials = selectedToolIds.every(
      (toolId) => (materialsByTool[toolId] || []).length > 0
    );

    if (!allToolsHaveMaterials) {
      alert('Please select at least one material for each tool');
      return;
    }

    onNext();
  };

  const handleToolSwitch = (index: number) => {
    setCurrentToolIndex(index);
  };

  const getMaterialHardnessColor = (hardness: number): string => {
    // Color scale from soft (green) to hard (red)
    if (hardness <= 2) return '#22c55e'; // Soft - Green
    if (hardness <= 4) return '#f59e0b'; // Medium - Orange
    return '#ef4444'; // Hard - Red
  };

  const getTotalSelectedMaterials = () => {
    return Object.values(materialsByTool).reduce(
      (total, mats) => total + mats.length,
      0
    );
  };

  if (loading) {
    return (
      <div className="screen material-selection">
        <div className="screen__header">
          <h2>Loading materials...</h2>
        </div>
      </div>
    );
  }

  return (
    <div className="screen material-selection">
      <div className="screen__header">
        <h2>Material Selection (Per Tool)</h2>
        <p className="screen__description">
          IMPORTANT: Select applicable materials for EACH tool separately.
          Different tools may work with different materials.
        </p>
      </div>

      {/* Tool Switcher (if multiple tools) */}
      {selectedToolIds.length > 1 && (
        <div className="tool-tabs">
          {selectedToolIds.map((toolId, index) => {
            const tool = allTools.find((t) => t.id === toolId);
            const materialCount = (materialsByTool[toolId] || []).length;
            const isActive = index === currentToolIndex;

            return (
              <button
                key={toolId}
                className={`tool-tab ${isActive ? 'tool-tab--active' : ''}`}
                onClick={() => handleToolSwitch(index)}
              >
                <span className="tool-tab__name">
                  {tool?.name || toolId}
                </span>
                <span className="tool-tab__count">
                  {materialCount} material{materialCount !== 1 ? 's' : ''}
                </span>
              </button>
            );
          })}
        </div>
      )}

      {/* Current Tool Info */}
      {currentTool && (
        <div className="current-tool-info">
          <h3>
            Selecting materials for: <strong>{currentTool.name}</strong>
          </h3>
          <div className="current-tool-specs">
            <span>DC: {currentTool.geometry.DC}mm</span>
            <span>•</span>
            <span>LCF: {currentTool.geometry.LCF}mm</span>
            <span>•</span>
            <span>{currentTool.type}</span>
          </div>
        </div>
      )}

      {/* Material Grid */}
      <div className="material-grid">
        {allMaterials
          .sort((a, b) => a.hardness_order - b.hardness_order)
          .map((material) => {
            const isSelected = currentMaterials.includes(material.id);
            const hardnessColor = getMaterialHardnessColor(material.hardness_order);

            return (
              <Card
                key={material.id}
                variant="bordered"
                hoverable
                clickable
                selected={isSelected}
                onClick={() => toggleMaterialForTool(currentToolId, material.id)}
              >
                <div className="material-card__content">
                  <div className="material-card__header">
                    <h3 className="material-card__title">{material.name}</h3>
                    {isSelected && (
                      <span className="material-card__badge">Selected</span>
                    )}
                  </div>

                  <div className="material-card__details">
                    <div className="material-card__hardness">
                      <span className="material-card__label">Hardness:</span>
                      <div className="material-card__hardness-bar">
                        <div
                          className="material-card__hardness-fill"
                          style={{
                            width: `${(material.hardness_order / 7) * 100}%`,
                            backgroundColor: hardnessColor,
                          }}
                        />
                        <span className="material-card__hardness-value">
                          {material.hardness_order}/7
                        </span>
                      </div>
                    </div>

                    <div className="material-card__detail">
                      <span className="material-card__label">Category:</span>
                      <span
                        className="material-card__category"
                        style={{ color: material.color }}
                      >
                        {material.category}
                      </span>
                    </div>
                  </div>
                </div>
              </Card>
            );
          })}
      </div>

      {/* Summary Sidebar */}
      <div className="screen__sidebar">
        <div className="selection-summary">
          <h4>Selected Materials per Tool</h4>

          <div className="selection-summary__stats">
            <div className="stat">
              <span className="stat__label">Total Materials:</span>
              <span className="stat__value">{getTotalSelectedMaterials()}</span>
            </div>
          </div>

          <div className="tool-material-summary">
            {selectedToolIds.map((toolId) => {
              const tool = allTools.find((t) => t.id === toolId);
              const materials = materialsByTool[toolId] || [];

              return (
                <div key={toolId} className="tool-material-item">
                  <div className="tool-material-item__header">
                    <strong>{tool?.name || toolId}</strong>
                    <span className="tool-material-item__count">
                      {materials.length}
                    </span>
                  </div>
                  <div className="tool-material-item__list">
                    {materials.length === 0 ? (
                      <span className="tool-material-item__empty">
                        No materials selected
                      </span>
                    ) : (
                      materials.map((matId) => {
                        const mat = allMaterials.find((m) => m.id === matId);
                        return mat ? (
                          <span key={matId} className="tool-material-item__tag">
                            {mat.name}
                          </span>
                        ) : null;
                      })
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* Navigation Footer */}
      <div className="screen__footer">
        <Button variant="secondary" onClick={onBack}>
          Back
        </Button>
        <Button
          variant="primary"
          onClick={handleNext}
        >
          Next: Operations
        </Button>
      </div>
    </div>
  );
};

export default MaterialSelection;
