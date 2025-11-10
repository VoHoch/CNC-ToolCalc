import { useState } from 'react';
import { ToolSelection } from '@/screens/ToolSelection';
import { MaterialSelection } from '@/screens/MaterialSelection';

function App() {
  const [currentScreen, setCurrentScreen] = useState<'tools' | 'materials'>('tools');

  return (
    <div className="app">
      {currentScreen === 'tools' && (
        <ToolSelection onNext={() => setCurrentScreen('materials')} />
      )}
      {currentScreen === 'materials' && (
        <MaterialSelection
          onNext={() => console.log('Next screen')}
          onBack={() => setCurrentScreen('tools')}
        />
      )}
    </div>
  );
}

export default App;
