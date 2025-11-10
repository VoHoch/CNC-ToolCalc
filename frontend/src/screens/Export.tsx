import React from 'react';
import { useCalculationStore } from '@/state/calculationStore';
import { useExportStore } from '@/state/exportStore';
import { Button } from '@/components/common';

interface ExportProps {
  onBack: () => void;
}

export const Export: React.FC<ExportProps> = ({ onBack }) => {
  const { calculationResults } = useCalculationStore();
  const { exportFormat, selectExportFormat, toggleResultSelection, selectedResultIds, exportFusion, downloadExport } =
    useExportStore();

  const results = Object.values(calculationResults);

  const handleExport = async () => {
    if (exportFormat === 'fusion') {
      const blob = await exportFusion();
      downloadExport(blob, 'cnc-toolcalc-export.tools');
    }
  };

  return (
    <div className="screen">
      <h2>Export Results</h2>

      <div>
        <h3>Export Format</h3>
        <button className={exportFormat === 'fusion' ? 'active' : ''} onClick={() => selectExportFormat('fusion')}>
          Fusion 360
        </button>
        <button className={exportFormat === 'underscott' ? 'active' : ''} onClick={() => selectExportFormat('underscott')}>
          Underscott CSV
        </button>
      </div>

      <div>
        <h3>Select Results</h3>
        {results.map(r => (
          <label key={r.calculation_id}>
            <input
              type="checkbox"
              checked={selectedResultIds.includes(r.calculation_id)}
              onChange={() => toggleResultSelection(r.calculation_id)}
            />
            {r.tool.name} - {r.input.material} - {r.input.operation}
          </label>
        ))}
      </div>

      <Button onClick={onBack}>Back</Button>
      <Button onClick={handleExport} disabled={selectedResultIds.length === 0}>
        Export
      </Button>
    </div>
  );
};
