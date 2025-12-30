import React, { useState, useEffect } from 'react';
import Dashboard from './components/Dashboard';
import History from './components/History';
import Analytics from './components/Analytics';
import Settings from './components/Settings';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');

  return (
    <div className="container">
      <header className="header">
        <div>
          <h1>LendShield</h1>
          <span style={{ color: 'var(--text-secondary)' }}>AI-Powered Risk Analyzer</span>
        </div>
        <div>
          <button 
            className={`btn ${activeTab === 'dashboard' ? 'btn-primary' : ''}`}
            onClick={() => setActiveTab('dashboard')}
            style={{ marginRight: '10px' }}
          >
            Dashboard
          </button>
          <button 
            className={`btn ${activeTab === 'analytics' ? 'btn-primary' : ''}`}
            onClick={() => setActiveTab('analytics')}
            style={{ marginRight: '10px' }}
          >
            Analytics
          </button>
          <button 
            className={`btn ${activeTab === 'history' ? 'btn-primary' : ''}`}
            onClick={() => setActiveTab('history')}
            style={{ marginRight: '10px' }}
          >
            History
          </button>
          <button 
            className={`btn ${activeTab === 'settings' ? 'btn-primary' : ''}`}
            onClick={() => setActiveTab('settings')}
          >
            Settings
          </button>
        </div>
      </header>

      <main>
        {activeTab === 'dashboard' && <Dashboard />}
        {activeTab === 'analytics' && <Analytics />}
        {activeTab === 'history' && <History />}
        {activeTab === 'settings' && <Settings />}
      </main>
    </div>
  );
}

export default App;
