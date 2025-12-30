import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts';

export default function RiskChart({ stats }) {
  if (!stats || !stats.risk_distribution) return <div>No Data</div>;

  const data = Object.keys(stats.risk_distribution).map(key => ({
    name: key,
    value: stats.risk_distribution[key]
  }));

  const COLORS = {
    'Low': '#10b981',
    'Medium': '#f59e0b',
    'High': '#ef4444'
  };

  return (
    <ResponsiveContainer width="100%" height="100%">
      <PieChart>
        <Pie
          data={data}
          cx="50%"
          cy="50%"
          innerRadius={40}
          outerRadius={80}
          paddingAngle={5}
          dataKey="value"
        >
          {data.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={COLORS[entry.name] || '#ccc'} />
          ))}
        </Pie>
        <Tooltip />
        <Legend />
      </PieChart>
    </ResponsiveContainer>
  );
}
