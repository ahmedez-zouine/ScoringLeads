import { useState, useEffect } from 'react'
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, AreaChart, Area } from 'recharts'
import './App.css'

// In Docker: VITE_API_URL="" → nginx proxies /api/* to the API container.
// In local dev: VITE_API_URL is undefined → fall back to http://localhost:8000.
const API_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    return (
      <div style={{
        background: 'rgba(15, 23, 42, 0.95)',
        border: '1px solid rgba(148, 163, 184, 0.1)',
        borderRadius: 12,
        padding: '10px 14px',
        boxShadow: '0 8px 32px rgba(0,0,0,0.4)',
        backdropFilter: 'blur(10px)',
      }}>
        <p style={{ color: '#f1f5f9', fontWeight: 600, fontSize: 13 }}>{label || payload[0].name}</p>
        <p style={{ color: '#818cf8', fontSize: 13 }}>{payload[0].value}</p>
      </div>
    )
  }
  return null
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

  const pieData = [
    { name: 'Chaud', value: stats.repartition.Chaud },
    { name: 'Tiede', value: stats.repartition.Tiede },
    { name: 'Froid', value: stats.repartition.Froid },
  ]

  const barData = Object.entries(stats.score_par_profession).map(([name, score]) => ({
    name: name.slice(0, 8),
    score,
  }))

  const COLORS = ['#f43f5e', '#f59e0b', '#38bdf8']

  const renderCustomLabel = ({ cx, cy, midAngle, innerRadius, outerRadius, name, percent }) => {
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

  return (
    <div className="app">
      <div className="header">
        <h1>Lead Scoring Dashboard</h1>
        <p>Analyse et priorisation des leads commerciaux</p>
      </div>

      <div className="metrics">
        <div className="metric-card" style={{ animationDelay: '0.1s' }}>
          <span className="icon">📊</span>
          <div className="value" style={{ color: '#818cf8' }}>{stats.total_leads}</div>
          <div className="label">Total Leads</div>
        </div>
        <div className="metric-card" style={{ animationDelay: '0.2s' }}>
          <span className="icon">⚡</span>
          <div className="value" style={{ color: '#34d399' }}>{stats.score_moyen}</div>
          <div className="label">Score Moyen</div>
        </div>
        <div className="metric-card" style={{ animationDelay: '0.3s' }}>
          <span className="icon">🔥</span>
          <div className="value" style={{ color: '#f43f5e' }}>{stats.repartition.Chaud}</div>
          <div className="label">Leads Chauds</div>
        </div>
        <div className="metric-card" style={{ animationDelay: '0.4s' }}>
          <span className="icon">❄️</span>
          <div className="value" style={{ color: '#38bdf8' }}>{stats.repartition.Froid}</div>
          <div className="label">Leads Froids</div>
        </div>
      </div>

      <div className="charts-row">
        <div className="chart-card">
          <h3>Repartition des Leads</h3>
          <ResponsiveContainer width="100%" height={280}>
            <PieChart>
              <Pie
                data={pieData}
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
                {pieData.map((_, i) => <Cell key={i} fill={COLORS[i]} />)}
              </Pie>
              <Tooltip content={<CustomTooltip />} />
            </PieChart>
          </ResponsiveContainer>
        </div>
        <div className="chart-card">
          <h3>Score Moyen par Profession</h3>
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={barData} layout="vertical" margin={{ left: 10 }}>
              <XAxis type="number" stroke="#334155" fontSize={11} tickLine={false} axisLine={false} />
              <YAxis dataKey="name" type="category" width={80} stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} />
              <Tooltip content={<CustomTooltip />} />
              <Bar dataKey="score" radius={[0, 6, 6, 0]} animationDuration={1200}>
                {barData.map((entry, i) => (
                  <Cell key={i} fill={entry.score >= 60 ? '#818cf8' : entry.score >= 45 ? '#a78bfa' : '#64748b'} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="table-card">
        <h3>Liste des Leads</h3>
        <div className="filters">
          <select value={catFilter} onChange={e => setCatFilter(e.target.value)}>
            <option value="">Toutes les categories</option>
            <option value="Chaud">🔥 Chaud</option>
            <option value="Tiede">🟡 Tiede</option>
            <option value="Froid">❄️ Froid</option>
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
        <div className="table-wrapper">
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
              {leads.map((lead, idx) => (
                <tr key={lead.id} style={{ animationDelay: `${idx * 0.02}s` }}>
                  <td><span className="client-name">{lead.nom}</span></td>
                  <td><span className="profession-tag">{lead.profession}</span></td>
                  <td style={{ color: '#f1f5f9', fontWeight: 500 }}>{lead.revenu_mensuel.toLocaleString()} €</td>
                  <td style={{ color: lead.score_interet >= 70 ? '#34d399' : '#94a3b8' }}>{lead.score_interet}</td>
                  <td>
                    <div className="score-cell">
                      <span className="score-value" style={{
                        color: lead.lead_score >= 70 ? '#f43f5e' : lead.lead_score >= 40 ? '#f59e0b' : '#38bdf8'
                      }}>{lead.lead_score}</span>
                      <div className="score-bar">
                        <div className="score-bar-fill" style={{
                          width: `${lead.lead_score}%`,
                          background: lead.lead_score >= 70
                            ? 'linear-gradient(90deg, #f43f5e, #fb7185)'
                            : lead.lead_score >= 40
                              ? 'linear-gradient(90deg, #f59e0b, #fbbf24)'
                              : 'linear-gradient(90deg, #38bdf8, #7dd3fc)'
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

      <div className="footer">
        Lead Scoring Dashboard — AI Associates
      </div>
    </div>
  )
}

export default App
