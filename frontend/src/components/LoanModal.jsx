import React, { useState } from 'react';
import axios from 'axios';

const API = axios.create({ baseURL: import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000' });

export default function LoanModal({ loan, onClose }) {
  const [currentStatus, setCurrentStatus] = useState(loan?.status || 'Pending');
  const [loading, setLoading] = useState(false);

  React.useEffect(() => {
    setCurrentStatus(loan?.status || 'Pending');
  }, [loan]);

  if (!loan) return null;

  const handleDecision = async (status) => {
    setLoading(true);
    try {
        await API.put(`/loans/${loan.id}`, { status });
        setCurrentStatus(status);
        // We could trigger a refresh of the parent list here, but for now local state update is fine for the modal
    } catch (e) {
        alert("Error updating status");
    }
    setLoading(false);
  };

  return (
    <div className="modal-overlay" onClick={() => onClose(currentStatus !== (loan.status || 'Pending'))}>
      <div className="modal-content" onClick={e => e.stopPropagation()}>
        <div className="modal-header">
            <div>
                <h2 style={{ marginBottom: '5px' }}>Confidential Case File: #{loan.id}</h2>
                <div style={{ 
                    display: 'inline-block',
                    padding: '2px 8px',
                    borderRadius: '4px',
                    fontSize: '0.8rem',
                    fontWeight: 'bold',
                    background: currentStatus === 'Approved' ? 'var(--success)' : (currentStatus === 'Rejected' ? 'var(--danger)' : '#64748b'),
                    color: 'white'
                }}>
                    STATUS: {currentStatus.toUpperCase()}
                </div>
            </div>
            <button className="btn close-btn" onClick={() => onClose(currentStatus !== (loan.status || 'Pending'))}>&times;</button>
        </div>
        
        <div className="modal-body">
            {/* ... profile section ... */}
            <div className="profile-section">
                <div className="avatar-placeholder">
                    {loan.name.charAt(0)}
                </div>
                <div>
                    <h3>{loan.name}</h3>
                    <div className={`risk-badge risk-${loan.risk_level}`} style={{display:'inline-block'}}>
                        {loan.risk_level} Risk
                    </div>
                </div>
            </div>

            {/* ... stats grid ... */}
            <div className="grid-col-2" style={{ marginTop: '20px' }}>
                <div>
                    <small>Annual Income</small>
                    <p style={{ fontSize: '1.2rem', fontWeight: 'bold' }}>${loan.annual_income.toLocaleString()}</p>
                </div>
                <div>
                    <small>Loan Requested</small>
                    <p style={{ fontSize: '1.2rem', fontWeight: 'bold' }}>${loan.loan_amount.toLocaleString()}</p>
                </div>
                <div>
                    <small>Credit Score</small>
                    <p style={{ fontSize: '1.2rem', fontWeight: 'bold' }}>{loan.credit_score}</p>
                </div>
                <div>
                    <small>AI Safety Score</small>
                    <p style={{ fontSize: '1.2rem', fontWeight: 'bold' }}>{loan.score}/100</p>
                </div>
            </div>

            <div style={{ marginTop: '20px', padding: '15px', background: 'rgba(255,255,255,0.05)', borderRadius: '8px' }}>
                <small style={{ textTransform: 'uppercase', color: 'var(--text-secondary)' }}>AI Reasoning</small>
                <p style={{ marginTop: '5px' }}>{loan.reasoning}</p>
                
                {loan.alerts && loan.alerts.length > 0 && (
                    <div style={{ marginTop: '10px' }}>
                        {loan.alerts.map((alert, idx) => (
                             <div key={idx} className="fraud-alert">⚠ {alert}</div>
                        ))}
                    </div>
                )}
            </div>

            <div style={{ marginTop: '30px', borderTop: '1px solid var(--border-color)', paddingTop: '20px' }}>
                <small>Manual Override Actions</small>
                {currentStatus === 'Pending' ? (
                    <div style={{ display: 'flex', gap: '10px', marginTop: '10px' }}>
                        <button 
                            className="btn" 
                            style={{ flex: 1, background: 'var(--success)', color: 'white', opacity: loading ? 0.7 : 1 }}
                            onClick={() => handleDecision('Approved')}
                            disabled={loading}
                        >
                            ✓ Approve Application
                        </button>
                        <button 
                            className="btn" 
                            style={{ flex: 1, background: 'var(--danger)', color: 'white', opacity: loading ? 0.7 : 1 }}
                            onClick={() => handleDecision('Rejected')}
                            disabled={loading}
                        >
                            ✕ Reject Application
                        </button>
                    </div>
                ) : (
                    <div style={{ marginTop: '10px', textAlign: 'center', padding: '10px', background: 'rgba(255,255,255,0.05)', borderRadius: '8px' }}>
                        <p style={{ margin: 0, fontWeight: 'bold', color: currentStatus === 'Approved' ? 'var(--success)' : 'var(--danger)' }}>
                            Application {currentStatus}
                        </p>
                    </div>
                )}
            </div>
        </div>
      </div>
    </div>
  );
}
