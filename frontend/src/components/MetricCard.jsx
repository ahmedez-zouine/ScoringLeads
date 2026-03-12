export function MetricCard({ icon, value, label, valueColor, animationDelay }) {
  return (
    <div className="metric-card" style={{ animationDelay }}>
      <span className="icon">{icon}</span>
      <div className="value" style={{ color: valueColor }}>{value}</div>
      <div className="label">{label}</div>
    </div>
  )
}