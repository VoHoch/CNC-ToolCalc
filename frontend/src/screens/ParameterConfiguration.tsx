import React from 'react';
import { useCalculationStore } from '@/state/calculationStore';
import { Button } from '@/components/common';
import type { CoatingType, SurfaceQuality, CoolantType } from '@/types/api';

interface ParameterConfigurationProps {
  onNext: () => void;
  onBack: () => void;
}

export const ParameterConfiguration: React.FC<ParameterConfigurationProps> = ({ onNext, onBack }) => {
  const { coatingType, surfaceQuality, coolantType, setCoating, setSurfaceQuality, setCoolant } =
    useCalculationStore();

  const coatings: CoatingType[] = ['none', 'tin', 'tialn', 'altin', 'diamond', 'carbide'];
  const qualities: SurfaceQuality[] = ['roughing', 'standard', 'finishing', 'high_finish'];
  const coolants: CoolantType[] = ['wet', 'dry', 'mql'];

  return (
    <div className="screen">
      <h2>Coating + Surface Quality</h2>

      <div>
        <h3>Coating</h3>
        {coatings.map(c => (
          <button key={c} className={coatingType === c ? 'active' : ''} onClick={() => setCoating(c)}>
            {c.toUpperCase()}
          </button>
        ))}
      </div>

      <div>
        <h3>Surface Quality</h3>
        {qualities.map(q => (
          <button key={q} className={surfaceQuality === q ? 'active' : ''} onClick={() => setSurfaceQuality(q)}>
            {q.replace('_', ' ').toUpperCase()}
          </button>
        ))}
      </div>

      <div>
        <h3>Coolant</h3>
        {coolants.map(c => (
          <button key={c} className={coolantType === c ? 'active' : ''} onClick={() => setCoolant(c)}>
            {c.toUpperCase()}
          </button>
        ))}
      </div>

      <Button onClick={onBack}>Back</Button>
      <Button onClick={onNext}>Next: Calculate</Button>
    </div>
  );
};
