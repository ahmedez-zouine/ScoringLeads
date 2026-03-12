function getLeadScoreColor(score) {
  if (score >= 70) return '#f43f5e'
  if (score >= 40) return '#f59e0b'
  return '#38bdf8'
}

function getLeadScoreBackground(score) {
  if (score >= 70) return 'linear-gradient(90deg, #f43f5e, #fb7185)'
  if (score >= 40) return 'linear-gradient(90deg, #f59e0b, #fbbf24)'
  return 'linear-gradient(90deg, #38bdf8, #7dd3fc)'
}

export function LeadsTable({
  leads,
  professions,
  catFilter,
  profFilter,
  sortBy,
  onCatFilterChange,
  onProfFilterChange,
  onSortByChange,
}) {
  return (
    <div className="table-card">
      <h3>Liste des Leads</h3>
      <div className="filters">
        <select value={catFilter} onChange={(event) => onCatFilterChange(event.target.value)}>
          <option value="">Toutes les categories</option>
          <option value="Chaud">🔥 Chaud</option>
          <option value="Tiede">🟡 Tiede</option>
          <option value="Froid">❄️ Froid</option>
        </select>
        <select value={profFilter} onChange={(event) => onProfFilterChange(event.target.value)}>
          <option value="">Toutes les professions</option>
          {professions.map((profession) => (
            <option key={profession} value={profession}>
              {profession}
            </option>
          ))}
        </select>
        <select value={sortBy} onChange={(event) => onSortByChange(event.target.value)}>
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
            {leads.map((lead, index) => (
              <tr key={lead.id} style={{ animationDelay: `${index * 0.02}s` }}>
                <td><span className="client-name">{lead.nom}</span></td>
                <td><span className="profession-tag">{lead.profession}</span></td>
                <td style={{ color: '#f1f5f9', fontWeight: 500 }}>{lead.revenu_mensuel.toLocaleString()} €</td>
                <td style={{ color: lead.score_interet >= 70 ? '#34d399' : '#94a3b8' }}>{lead.score_interet}</td>
                <td>
                  <div className="score-cell">
                    <span className="score-value" style={{ color: getLeadScoreColor(lead.lead_score) }}>
                      {lead.lead_score}
                    </span>
                    <div className="score-bar">
                      <div
                        className="score-bar-fill"
                        style={{
                          width: `${lead.lead_score}%`,
                          background: getLeadScoreBackground(lead.lead_score),
                        }}
                      />
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