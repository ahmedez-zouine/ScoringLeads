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

async function fetchJson(url) {
  const response = await fetch(url)
  if (!response.ok) {
    const message = await response.text()
    throw new Error(message || `HTTP ${response.status}`)
  }
  return response.json()
}

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
      fetchJson(`${API_URL}/api/stats`),
      fetchJson(`${API_URL}/api/professions`),
    ])
      .then(([statsData, profsData]) => {
        if (!statsData?.repartition || !statsData?.score_par_profession) {
          throw new Error('Invalid stats payload')
        }
        if (!Array.isArray(profsData)) {
          throw new Error('Invalid professions payload')
        }
        setStats(statsData)
        setProfessions(profsData)
        setLoading(false)
      })
      .catch((err) => {
        console.error('Failed to load dashboard data:', err)
        setError('API non disponible ou erreur serveur. Vérifiez backend/Docker puis rechargez la page.')
        setLoading(false)
      })
  }, [])

  useEffect(() => {
    const params = new URLSearchParams({ sort_by: sortBy, order: 'desc' })
    if (catFilter) params.set('categorie', catFilter)
    if (profFilter) params.set('profession', profFilter)

    fetchJson(`${API_URL}/api/leads?${params}`)
      .then((data) => {
        setLeads(Array.isArray(data) ? data : [])
      })
      .catch((err) => {
        console.error('Failed to load leads:', err)
        setLeads([])
      })
  }, [catFilter, profFilter, sortBy])

  const pieData = useMemo(
    () => [
      { name: 'Chaud', value: stats?.repartition?.Chaud ?? 0 },
      { name: 'Tiede', value: stats?.repartition?.Tiede ?? 0 },
      { name: 'Froid', value: stats?.repartition?.Froid ?? 0 },
    ],
    [stats],
  )

  const barData = useMemo(
    () => Object.entries(stats?.score_par_profession ?? {}).map(([name, score]) => ({
      name: name.slice(0, 8),
      score,
    })),
    [stats],
  )

  if (loading) return <div className="loading">Chargement</div>
  if (error) return <div className="app"><div className="error">{error}</div></div>
  if (!stats?.repartition || !stats?.score_par_profession) {
    return <div className="app"><div className="error">Données statistiques invalides</div></div>
  }

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
