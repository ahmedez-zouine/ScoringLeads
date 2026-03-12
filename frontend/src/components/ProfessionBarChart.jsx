import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts'
import { CustomTooltip } from './CustomTooltip'

function getBarColor(score) {
  if (score >= 60) return '#818cf8'
  if (score >= 45) return '#a78bfa'
  return '#64748b'
}

export function ProfessionBarChart({ data }) {
  return (
    <div className="chart-card">
      <h3>Score Moyen par Profession</h3>
      <ResponsiveContainer width="100%" height={280}>
        <BarChart data={data} layout="vertical" margin={{ left: 10 }}>
          <XAxis type="number" stroke="#334155" fontSize={11} tickLine={false} axisLine={false} />
          <YAxis dataKey="name" type="category" width={80} stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} />
          <Tooltip content={<CustomTooltip />} />
          <Bar dataKey="score" radius={[0, 6, 6, 0]} animationDuration={1200}>
            {data.map((entry, index) => (
              <Cell key={index} fill={getBarColor(entry.score)} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}