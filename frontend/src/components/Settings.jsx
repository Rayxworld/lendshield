import React, { useState } from 'react';
import axios from 'axios';

const API = axios.create({ baseURL: 'http://127.0.0.1:8000' });

export default function Settings() {
  const [status, setStatus] = useState('');

  const handleReset = async () => {
    if (confirm("Are you sure? This will delete all current data and generate 5 new sample loans.")) {
        setStatus('Resetting...');
        try {
            await API.delete('/loans');
            setStatus('Database reset successfully!');
            setTimeout(() => setStatus(''), 3000);
        } catch (e) {
            setStatus('Error resetting database.');
        }
    }
  };

  return (
    <div style={{ maxWidth: '600px', margin: '0 auto' }}>
        <div className="card">
            <h2>System Settings</h2>
            <p style={{ color: 'var(--text-secondary)', marginBottom: '24px' }}>
                Manage you local database and demo configurations.
            </p>

            <div style={{ padding: '20px', border: '1px solid var(--border-color)', borderRadius: '8px' }}>
                <h3 style={{ margin: '0 0 10px 0', color: 'var(--danger)' }}>Danger Zone</h3>
                <p style={{ fontSize: '0.9rem', marginBottom: '20px' }}>
                    Resetting the database is irreversible. Use this to clear the demo state for a new presentation.
                </p>
                <button 
                    onClick={handleReset}
                    className="btn"
                    style={{ background: 'rgba(239, 68, 68, 0.2)', color: '#f87171', border: '1px solid #ef4444' }}
                >
                    Reset Database & Restart Demo
                </button>
                
                {status && <p style={{ marginTop: '10px', color: 'var(--accent-blue)' }}>{status}</p>}
            </div>
        </div>
    </div>
  );
}
