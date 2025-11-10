import React, { useEffect } from 'react';
import { useCalculationStore } from '@/state/calculationStore';
import { Button } from '@/components/common';
import { apiClient } from '@/api/client';

interface OperationSelectionProps {
  onNext: () => void;
  onBack: () => void;
}

export const OperationSelection: React.FC<OperationSelectionProps> = ({ onNext, onBack }) => {
  const { selectedOperations, toggleOperation } = useCalculationStore();
  const [operationGroups, setOperationGroups] = React.useState<any[]>([]);

  useEffect(() => {
    apiClient.getOperations().then(res => setOperationGroups(res.operations));
  }, []);

  return (
    <div className="screen">
      <h2>Select Operations</h2>
      {operationGroups.map(group => (
        <div key={group.group}>
          <h3>{group.group}</h3>
          {group.operations.map((op: any) => (
            <label key={op.id}>
              <input
                type="checkbox"
                checked={selectedOperations.includes(op.id)}
                onChange={() => toggleOperation(op.id)}
              />
              {op.name}
            </label>
          ))}
        </div>
      ))}
      <Button onClick={onBack}>Back</Button>
      <Button onClick={onNext} disabled={selectedOperations.length === 0}>
        Next: Parameters
      </Button>
    </div>
  );
};
