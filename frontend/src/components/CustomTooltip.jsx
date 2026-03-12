export function CustomTooltip({ active, payload, label }) {
  if (!(active && payload && payload.length)) return null

  return (
    <div
      style={{
        background: 'rgba(15, 23, 42, 0.95)',
        border: '1px solid rgba(148, 163, 184, 0.1)',
        borderRadius: 12,
        padding: '10px 14px',
        boxShadow: '0 8px 32px rgba(0,0,0,0.4)',
        backdropFilter: 'blur(10px)',
      }}
    >
      <p style={{ color: '#f1f5f9', fontWeight: 600, fontSize: 13 }}>{label || payload[0].name}</p>
      <p style={{ color: '#818cf8', fontSize: 13 }}>{payload[0].value}</p>
    </div>
  )
}