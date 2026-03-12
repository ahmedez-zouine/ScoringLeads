import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from 'recharts'
import { CustomTooltip } from './CustomTooltip'

const COLORS = ['#f43f5e', '#f59e0b', '#38bdf8']

function renderCustomLabel({ cx, cy, midAngle, outerRadius, name, percent }) {
  const RADIAN = Math.PI / 180
  const radius = outerRadius + 25
  const x = cx + radius * Math.cos(-midAngle * RADIAN)
  const y = cy + radius * Math.sin(-midAngle * RADIAN)

  return (
    <text x={x} y={y} fill="#94a3b8" textAnchor={x > cx ? 'start' : 'end'} fontSize={12} fontWeight={500}>
      {`${name} ${(percent * 100).toFixed(0)}%`}
    </text>
  )
}

export function LeadsPieChart({ data }) {
  return (
    <div className="chart-card">
      <h3>Repartition des Leads</h3>
      <ResponsiveContainer width="100%" height={280}>
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            outerRadius={95}
            innerRadius={55}
            dataKey="value"
            label={renderCustomLabel}
            stroke="none"
            animationBegin={200}
            animationDuration={1000}
          >
            {data.map((_, index) => (
              <Cell key={index} fill={COLORS[index]} />
            ))}
          </Pie>
          <Tooltip content={<CustomTooltip />} />
        </PieChart>
      </ResponsiveContainer>
    </div>
  )
}