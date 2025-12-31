import React, { useState, useEffect } from 'react';
import axios from 'axios';
import RiskChart from './RiskChart';

// Configure Axios base URL
const API = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'
});

export default function Dashboard() {
  const [loans, setLoans] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [latestAnalysis, setLatestAnalysis] = useState(null);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [loansRes, statsRes] = await Promise.all([
        API.get('/loans'),
        API.get('/portfolio')
      ]);
      setLoans(loansRes.data);
      setStats(statsRes.data);
    } catch (err) {
      console.error("Failed to fetch data", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleSimulate = async () => {
    // 1. Generate Random Profile
    const names = ["James Smith", "Maria Garcia", "Robert Johnson", "Sarah Davis", "Michael Wilson", "Emily Brown", "David Miller", "Jennifer Taylor"];
    const randomName = names[Math.floor(Math.random() * names.length)];
    
    const monthlyIncome = Math.floor(Math.random() * (10000 - 2000) + 2000); // 2k to 10k monthly
    const loanAmountThousands = Math.floor(Math.random() * (300 - 50) + 50); // 50k to 300k
    const creditHistory = Math.random() > 0.2 ? 1.0 : 0.0; // 80% chance of good credit
    
    // 2. newLoanInput matches Backend Pydantic Model (LoanApplication)
    const newLoanInput = {
      name: randomName,
      gender: Math.random() > 0.5 ? "Male" : "Female",
      married: Math.random() > 0.5 ? "Yes" : "No",
      dependents: Math.floor(Math.random() * 4), // 0 to 3
      education: Math.random() > 0.3 ? "Graduate" : "Not Graduate",
      self_employed: Math.random() > 0.8 ? "Yes" : "No", // 20% self employed
      applicant_income: monthlyIncome,
      coapplicant_income: Math.random() > 0.7 ? Math.floor(Math.random() * 3000) : 0,
      loan_amount: loanAmountThousands,
      loan_term: 360,
      credit_history: creditHistory,
      property_area: ["Urban", "Semiurban", "Rural"][Math.floor(Math.random() * 3)],
      doc_id_match: Math.random() > 0.05 // 95% match rate
    };
    
    try {
        const res = await API.post('/analyze', newLoanInput);
        setLatestAnalysis(res.data);
        fetchData(); // Refresh list
    } catch (e) {
        console.error("Simulation failed:", e);
        alert("Verification check failed. Ensure Backend is running the new version.");
    }
  };

  if (loading) return <div>Loading AI Models...</div>;

  return (
    <div>
      <div className="grid-col-2">
        <div className="card">
          <h2>Portfolio Overview</h2>
          {stats && (
            <div style={{ display: 'flex', gap: '20px', justifyContent: 'space-around' }}>
               <div style={{ textAlign: 'center' }}>
                 <h3>{stats.total_loans}</h3>
                 <small style={{ color: 'var(--text-secondary)' }}>Total Apps</small>
               </div>
               <div style={{ textAlign: 'center' }}>
                 <h3>{stats.status_distribution?.Approved || 0}</h3>
                 <small style={{ color: 'var(--success)' }}>Approved</small>
               </div>
               <div style={{ textAlign: 'center' }}>
                 <h3>{stats.status_distribution?.Rejected || 0}</h3>
                 <small style={{ color: 'var(--danger)' }}>Rejected</small>
               </div>
               <div style={{ textAlign: 'center', color: 'var(--warning)' }}>
                 <h3>{stats.fraud_cases}</h3>
                 <small>Fraud Alerts</small>
               </div>
            </div>
          )}
        </div>
        <div className="card">
            <h2>Risk Distribution</h2>
            <div style={{ height: '200px' }}>
                <RiskChart stats={stats} />
            </div>
        </div>
      </div>

      {latestAnalysis && (
        <div className="card" style={{ marginBottom: '24px', border: '1px solid var(--accent-blue)', background: 'rgba(59, 130, 246, 0.1)' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
                <div>
                    <h2 style={{ color: 'var(--accent-blue)', marginBottom: '10px' }}>🤖 AI Insight: New Application Analysis</h2>
                    <h3 style={{ margin: '0 0 5px 0' }}>{latestAnalysis.name}</h3>
                    <p style={{ fontSize: '1.1rem', margin: '0 0 10px 0' }}>
                        Risk Score: <strong style={{ color: `var(--${latestAnalysis.risk_level === 'High' ? 'danger' : (latestAnalysis.risk_level === 'Medium' ? 'warning' : 'success')})` }}>
                            {latestAnalysis.score}/100 ({latestAnalysis.risk_level})
                        </strong>
                    </p>
                    <p style={{ color: 'var(--text-primary)', background: 'rgba(0,0,0,0.2)', padding: '10px', borderRadius: '8px' }}>
                        " {latestAnalysis.reasoning} "
                    </p>
                </div>
                <div style={{ textAlign: 'right' }}>
                    <div style={{ marginBottom: '10px' }}>
                        {latestAnalysis.is_fraud ? (
                            <span className="fraud-alert" style={{ fontSize: '1.2rem' }}>⛔ FRAUD DETECTED</span>
                        ) : (
                            <span style={{ color: 'var(--success)', fontWeight: 'bold', fontSize: '1.2rem' }}>✓ LEGITIMATE</span>
                        )}
                    </div>
                </div>
            </div>
        </div>
      )}

      <div className="card">
        <div style={{display:'flex', justifyContent:'space-between', alignItems:'center'}}>
            <h2>Recent Applications</h2>
            <button className="btn btn-primary" onClick={handleSimulate}>+ Simulate New Application</button>
        </div>
        
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Score</th>
              <th>Risk</th>
              <th>Income</th>
              <th>Loan Amount</th>
              <th>Alerts</th>
            </tr>
          </thead>
          <tbody>
            {loans.map(loan => (
              <tr key={loan.id}>
                <td>#{loan.id}</td>
                <td>{loan.name}</td>
                <td>{loan.score}</td>
                <td>
                  <span className={`risk-badge risk-${loan.risk_level}`}>
                    {loan.risk_level}
                  </span>
                </td>
                <td>${loan.annual_income.toLocaleString()}</td>
                <td>${loan.loan_amount.toLocaleString()}</td>
                <td>
                  {loan.is_fraud ? (
                    <div style={{ color: 'red', fontSize: '0.8rem' }}>⚠ FRAUD DETECTED</div>
                  ) : (
                    <span style={{ color: 'green' }}>✓ Verified</span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
