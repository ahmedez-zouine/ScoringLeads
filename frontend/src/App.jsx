import { useEffect, useMemo, useState } from 'react'
import './App.css'
import { DashboardHeader } from './components/DashboardHeader'
import { MetricsGrid } from './components/MetricsGrid'
import { LeadsPieChart } from './components/LeadsPieChart'
import { ProfessionBarChart } from './components/ProfessionBarChart'
import { LeadsTable } from './components/LeadsTable'
import { DashboardFooter } from './components/DashboardFooter'

// In local dev: VITE_API_URL is undefined → fall back to http://localhost:8000.
const API_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

function App() {
  const [stats, setStats] = useState(null)
  const [leads, setLeads] = useState([])
  const [professions, setProfessions] = useState([])
  const [catFilter, setCatFilter] = useState('')
  const [profFilter, setProfFilter] = useState('')
  const [sortBy, setSortBy] = useState('lead_score')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    Promise.all([
      fetch(`${API_URL}/api/stats`).then(r => r.json()),
      fetch(`${API_URL}/api/professions`).then(r => r.json()),
    ])
      .then(([statsData, profsData]) => {
        setStats(statsData)
        setProfessions(profsData)
        setLoading(false)
      })
      .catch(() => {
        setError('API non disponible. Lancez: uvicorn api:app --reload')
        setLoading(false)
      })
  }, [])

  useEffect(() => {
    const params = new URLSearchParams({ sort_by: sortBy, order: 'desc' })
    if (catFilter) params.set('categorie', catFilter)
    if (profFilter) params.set('profession', profFilter)

    fetch(`${API_URL}/api/leads?${params}`)
      .then(r => r.json())
      .then(data => setLeads(data))
      .catch(() => { })
  }, [catFilter, profFilter, sortBy])

  if (loading) return <div className="loading">Chargement</div>
  if (error) return <div className="app"><div className="error">{error}</div></div>

  const pieData = useMemo(
    () => [
      { name: 'Chaud', value: stats.repartition.Chaud },
      { name: 'Tiede', value: stats.repartition.Tiede },
      { name: 'Froid', value: stats.repartition.Froid },
    ],
    [stats],
  )

  const barData = useMemo(
    () => Object.entries(stats.score_par_profession).map(([name, score]) => ({
      name: name.slice(0, 8),
      score,
    })),
    [stats],
  )

  return (
    <div className="app">
      <DashboardHeader />
      <MetricsGrid stats={stats} />

      <div className="charts-row">
        <LeadsPieChart data={pieData} />
        <ProfessionBarChart data={barData} />
      </div>
      <LeadsTable
        leads={leads}
        professions={professions}
        catFilter={catFilter}
        profFilter={profFilter}
        sortBy={sortBy}
        onCatFilterChange={setCatFilter}
        onProfFilterChange={setProfFilter}
        onSortByChange={setSortBy}
      />
      <DashboardFooter />
    </div>
  )
}

export default App
