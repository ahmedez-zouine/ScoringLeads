import { MetricCard } from './MetricCard'

export function MetricsGrid({ stats }) {
  return (
    <div className="metrics">
      <MetricCard
        icon=""
        value={stats.total_leads}
        label="Total Leads"
        valueColor="#818cf8"
        animationDelay="0.1s"
      />
      <MetricCard
        icon=""
        value={stats.score_moyen}
        label="Score Moyen"
        valueColor="#34d399"
        animationDelay="0.2s"
      />
      <MetricCard
        icon=""
        value={stats.repartition.Chaud}
        label="Leads Chauds"
        valueColor="#f43f5e"
        animationDelay="0.3s"
      />
      <MetricCard
        icon=""
        value={stats.repartition.Froid}
        label="Leads Froids"
        valueColor="#38bdf8"
        animationDelay="0.4s"
      />
    </div>
  )
}