import { useState, useEffect } from 'react'
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts'
import './App.css'

const API_URL = 'http://localhost:8000'

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
      .catch(() => {})
  }, [catFilter, profFilter, sortBy])

  if (loading) return <div className="loading">Chargement...</div>
  if (error) return <div className="app"><div className="error">{error}</div></div>

  const pieData = [
    { name: 'Chaud', value: stats.repartition.Chaud },
    { name: 'Tiede', value: stats.repartition.Tiede },
    { name: 'Froid', value: stats.repartition.Froid },
  ]

  const barData = Object.entries(stats.score_par_profession).map(([name, score]) => ({
    name,
    score,
  }))

  const COLORS = ['#ef4444', '#f59e0b', '#3b82f6']

  return (
    <div className="app">
      <div className="header">
        <h1>Lead Scoring Dashboard</h1>
        <p>Analyse et priorisation des leads commerciaux</p>
      </div>

      <div className="metrics">
        <div className="metric-card">
          <div className="value" style={{ color: '#6366f1' }}>{stats.total_leads}</div>
          <div className="label">Total Leads</div>
        </div>
        <div className="metric-card">
          <div className="value" style={{ color: '#22c55e' }}>{stats.score_moyen}</div>
          <div className="label">Score Moyen</div>
        </div>
        <div className="metric-card">
          <div className="value" style={{ color: '#ef4444' }}>{stats.repartition.Chaud}</div>
          <div className="label">Leads Chauds</div>
        </div>
        <div className="metric-card">
          <div className="value" style={{ color: '#3b82f6' }}>{stats.repartition.Froid}</div>
          <div className="label">Leads Froids</div>
        </div>
      </div>

      <div className="charts-row">
        <div className="chart-card">
          <h3>Repartition des Leads</h3>
          <ResponsiveContainer width="100%" height={250}>
            <PieChart>
              <Pie data={pieData} cx="50%" cy="50%" outerRadius={90} dataKey="value" label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}>
                {pieData.map((_, i) => <Cell key={i} fill={COLORS[i]} />)}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
        <div className="chart-card">
          <h3>Score Moyen par Profession</h3>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={barData} layout="vertical">
              <XAxis type="number" stroke="#94a3b8" fontSize={12} />
              <YAxis dataKey="name" type="category" width={90} stroke="#94a3b8" fontSize={12} />
              <Tooltip contentStyle={{ background: '#1e293b', border: '1px solid #334155', borderRadius: 8 }} />
              <Bar dataKey="score" fill="#6366f1" radius={[0, 4, 4, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="table-card">
        <h3>Liste des Leads</h3>
        <div className="filters">
          <select value={catFilter} onChange={e => setCatFilter(e.target.value)}>
            <option value="">Toutes les categories</option>
            <option value="Chaud">Chaud</option>
            <option value="Tiede">Tiede</option>
            <option value="Froid">Froid</option>
          </select>
          <select value={profFilter} onChange={e => setProfFilter(e.target.value)}>
            <option value="">Toutes les professions</option>
            {professions.map(p => <option key={p} value={p}>{p}</option>)}
          </select>
          <select value={sortBy} onChange={e => setSortBy(e.target.value)}>
            <option value="lead_score">Trier par Score</option>
            <option value="revenu_mensuel">Trier par Revenu</option>
            <option value="score_interet">Trier par Interet</option>
          </select>
        </div>
        <table>
          <thead>
            <tr>
              <th>Nom</th>
              <th>Profession</th>
              <th>Revenu</th>
              <th>Interet</th>
              <th>Lead Score</th>
              <th>Categorie</th>
            </tr>
          </thead>
          <tbody>
            {leads.map(lead => (
              <tr key={lead.id}>
                <td>{lead.nom}</td>
                <td>{lead.profession}</td>
                <td>{lead.revenu_mensuel.toLocaleString()}</td>
                <td>{lead.score_interet}</td>
                <td>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                    <span>{lead.lead_score}</span>
                    <div className="score-bar" style={{ width: 60 }}>
                      <div className="score-bar-fill" style={{
                        width: `${lead.lead_score}%`,
                        background: lead.lead_score >= 70 ? '#ef4444' : lead.lead_score >= 40 ? '#f59e0b' : '#3b82f6'
                      }} />
                    </div>
                  </div>
                </td>
                <td>
                  <span className={`badge badge-${lead.categorie.toLowerCase()}`}>
                    {lead.categorie}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default App
