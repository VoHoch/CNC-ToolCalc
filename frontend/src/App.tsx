import React, { useState } from 'react';
import { ToolSelection } from './screens/ToolSelection';
import { MaterialSelection } from './screens/MaterialSelection';
import { OperationSelection } from './screens/OperationSelection';
import { ParameterConfiguration } from './screens/ParameterConfiguration';
import { Results } from './screens/Results';
import { Export } from './screens/Export';

function App() {
  const [currentScreen, setCurrentScreen] = useState(0);

  const screens = [
    <ToolSelection onNext={() => setCurrentScreen(1)} />,
    <MaterialSelection onNext={() => setCurrentScreen(2)} onBack={() => setCurrentScreen(0)} />,
    <OperationSelection onNext={() => setCurrentScreen(3)} onBack={() => setCurrentScreen(1)} />,
    <ParameterConfiguration onNext={() => setCurrentScreen(4)} onBack={() => setCurrentScreen(2)} />,
    <Results onNext={() => setCurrentScreen(5)} onBack={() => setCurrentScreen(3)} />,
    <Export onBack={() => setCurrentScreen(4)} />,
  ];

  const screenTitles = [
    '1. Tool Selection',
    '2. Material Selection',
    '3. Operation Selection',
    '4. Parameters',
    '5. Results',
    '6. Export',
  ];

  return (
    <div style={{
      minHeight: '100vh',
      backgroundColor: '#0b0f15',
      color: '#e2e8f0',
      padding: '20px'
    }}>
      <header style={{ marginBottom: '40px' }}>
        <h1 style={{ fontSize: '32px', fontWeight: 600 }}>CNC-ToolCalc</h1>
        <div style={{ display: 'flex', gap: '10px', marginTop: '20px' }}>
          {screenTitles.map((title, i) => (
            <span
              key={i}
              style={{
                padding: '8px 16px',
                borderRadius: '4px',
                backgroundColor: i === currentScreen ? '#6366f1' : '#1a1f27',
                fontSize: '14px',
                cursor: 'pointer',
              }}
              onClick={() => setCurrentScreen(i)}
            >
              {title}
            </span>
          ))}
        </div>
      </header>

      <main>{screens[currentScreen]}</main>
    </div>
  );
}

export default App;
