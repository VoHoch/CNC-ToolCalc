import React, { useEffect } from 'react';
import { useToolStore } from '@/state/toolStore';
import { useMaterialStore } from '@/state/materialStore';
import { useCalculationStore } from '@/state/calculationStore';
import { useExpertModeStore } from '@/state/expertModeStore';
import { Button, Table, Slider } from '@/components/common';

interface ResultsProps {
  onNext: () => void;
  onBack: () => void;
}

export const Results: React.FC<ResultsProps> = ({ onNext, onBack }) => {
  const { selectedToolIds } = useToolStore();
  const { materialsByTool } = useMaterialStore();
  const { selectedOperations, calculationResults, calculate, isCalculating } = useCalculationStore();
  const { expertModeEnabled, toggleExpertMode, globalSlider, setGlobalSlider } = useExpertModeStore();

  useEffect(() => {
    // Auto-calculate
    selectedToolIds.forEach(toolId => {
      const mats = materialsByTool[toolId] || [];
      mats.forEach(matId => {
        selectedOperations.forEach(opId => {
          calculate(toolId, matId, opId);
        });
      });
    });
  }, []);

  const results = Object.values(calculationResults);

  return (
    <div className="screen">
      <h2>Calculation Results</h2>
      {isCalculating && <p>Calculating...</p>}

      <Table
        data={results}
        columns={[
          { key: 'tool', header: 'Tool', accessor: r => r.tool.name },
          { key: 'vc', header: 'vc (m/min)', accessor: r => r.results.vc_final.toFixed(1) },
          { key: 'n', header: 'n (RPM)', accessor: r => r.results.n_rpm },
          { key: 'vf', header: 'vf (mm/min)', accessor: r => r.results.vf_mm_min.toFixed(1) },
        ]}
      />

      <label>
        <input type="checkbox" checked={expertModeEnabled} onChange={toggleExpertMode} />
        Expert Mode
      </label>

      {expertModeEnabled && (
        <Slider
          min={-50}
          max={50}
          value={globalSlider}
          onChange={setGlobalSlider}
          markers={[
            { value: -50, label: 'Conservative' },
            { value: 0, label: 'Optimal' },
            { value: 50, label: 'Aggressive' },
          ]}
        />
      )}

      <Button onClick={onBack}>Back</Button>
      <Button onClick={onNext}>Next: Export</Button>
    </div>
  );
};
