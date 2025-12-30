import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';

const API = axios.create({ baseURL: 'http://127.0.0.1:8000' });

export default function Analytics() {
  const [data, setData] = useState([]);

  useEffect(() => {
    API.get('/loans').then(res => {
        // Take top 10 recent loans for the chart to keep it readable
        setData(res.data.slice(0, 10));
    });
  }, []);

  return (
    <div>
        <div className="card">
            <h2>Recent Loan Analysis (Income vs Amount)</h2>
            <p style={{ marginBottom: '20px', color: 'var(--text-secondary)' }}>Comparing Annual Income against Requested Loan Amount for recent applications.</p>
            
            <div style={{ height: '400px' }}>
                <ResponsiveContainer width="100%" height="100%">
                    <BarChart
                    data={data}
                    layout="vertical"
                    margin={{ top: 5, right: 30, left: 40, bottom: 5 }}
                    >
                        <CartesianGrid strokeDasharray="3 3" stroke="var(--border-color)" horizontal={false} />
                        <XAxis type="number" stroke="var(--text-secondary)" />
                        <YAxis dataKey="name" type="category" width={100} stroke="var(--text-secondary)" />
                        <Tooltip 
                            contentStyle={{ backgroundColor: 'var(--bg-card)', borderColor: 'var(--border-color)', borderRadius: '8px' }}
                            itemStyle={{ color: 'var(--text-primary)' }}
                        />
                        <Legend />
                        <Bar dataKey="annual_income" fill="var(--success)" name="Annual Income" barSize={10} radius={[0, 4, 4, 0]} />
                        <Bar dataKey="loan_amount" fill="var(--accent-blue)" name="Loan Amount" barSize={10} radius={[0, 4, 4, 0]} />
                    </BarChart>
                </ResponsiveContainer>
            </div>
        </div>
    </div>
  );
}
