import React, { useState, useEffect } from 'react';
import axios from 'axios';
import LoanModal from './LoanModal';

const API = axios.create({ baseURL: import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000' });

export default function History() {
  const [loans, setLoans] = useState([]);
  const [filter, setFilter] = useState('All');
  const [showFraudOnly, setShowFraudOnly] = useState(false);
  const [selectedLoan, setSelectedLoan] = useState(null);

  useEffect(() => {
    API.get('/loans').then(res => setLoans(res.data));
  }, []);

  // ... (filtering logic same as before) ...
  const filteredLoans = loans.filter(loan => {
    if (showFraudOnly && !loan.is_fraud) return false;
    if (filter !== 'All' && (loan.status || 'Pending') !== filter) return false;
    return true;
  });

  // ... (csv logic same as before) ...
  const downloadCSV = () => {
    const headers = ["ID,Name,Risk Score,Risk Level,Income,Loan Amount,Fraud,Reasoning"];
    const rows = filteredLoans.map(l => 
      `${l.id},"${l.name}",${l.score},${l.risk_level},${l.annual_income},${l.loan_amount},${l.is_fraud},"${l.reasoning}"`
    );
    const csvContent = "data:text/csv;charset=utf-8," + [headers, ...rows].join("\n");
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", "lendshield_history.csv");
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const handleModalClose = (updated) => {
    setSelectedLoan(null);
    if (updated) {
        API.get('/loans').then(res => setLoans(res.data));
    }
  };

  return (
    <>
    <div className="card">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
          <div>
            <h2>Application Management</h2>
            <div style={{ display: 'flex', gap: '8px', marginTop: '10px' }}>
                {['All', 'Pending', 'Approved', 'Rejected'].map(status => (
                    <button
                        key={status}
                        onClick={() => setFilter(status)}
                        className="btn"
                        style={{
                            padding: '6px 16px',
                            fontSize: '0.9rem',
                            background: filter === status ? 'var(--accent-blue)' : 'rgba(255,255,255,0.05)',
                            color: filter === status ? 'white' : 'var(--text-secondary)',
                            border: 'none'
                        }}
                    >
                        {status}
                    </button>
                ))}
            </div>
          </div>
          <div style={{ display: 'flex', gap: '10px' }}>
            <button className="btn" onClick={downloadCSV} style={{ border: '1px solid var(--border-color)' }}>
              📥 Export CSV
            </button>
            <button 
                className="btn"
                style={{ 
                    background: showFraudOnly ? 'var(--danger)' : 'transparent', 
                    border: '1px solid var(--danger)',
                    color: showFraudOnly ? 'white' : 'var(--danger)'
                }}
                onClick={() => setShowFraudOnly(!showFraudOnly)}
            >
                {showFraudOnly ? 'Showing Fraud Only' : 'Show Fraud Only'}
            </button>
          </div>
      </div>
      
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Status</th>
            <th>Risk Score</th>
            <th>Level</th>
            <th>Income</th>
            <th>Loan</th>
            <th>Reasoning</th>
          </tr>
        </thead>
        <tbody>
          {filteredLoans.map(loan => (
            <tr 
                key={loan.id} 
                onClick={() => setSelectedLoan(loan)}
                style={{ cursor: 'pointer', transition: 'background 0.2s' }}
                onMouseEnter={(e) => e.currentTarget.style.background = 'rgba(255,255,255,0.05)'}
                onMouseLeave={(e) => e.currentTarget.style.background = 'transparent'}
            >
              <td>#{loan.id}</td>
              <td>{loan.name}</td>
              <td>
                <span style={{ 
                    fontWeight: 'bold', 
                    color: loan.status === 'Approved' ? 'var(--success)' : (loan.status === 'Rejected' ? 'var(--danger)' : 'var(--text-secondary)')
                }}>
                    {loan.status || 'Pending'}
                </span>
              </td>
              <td>{loan.score}</td>
              <td>
                <span className={`risk-badge risk-${loan.risk_level}`}>
                  {loan.risk_level}
                </span>
              </td>
              <td>${loan.annual_income.toLocaleString()}</td>
              <td>${loan.loan_amount.toLocaleString()}</td>
              <td style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
                 {loan.reasoning.substring(0, 50)}...
                 {loan.is_fraud && <div className="fraud-alert" style={{marginTop: '4px'}}>FRAUD ALERT</div>}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
    
    <LoanModal loan={selectedLoan} onClose={handleModalClose} />
    </>
  );
}
