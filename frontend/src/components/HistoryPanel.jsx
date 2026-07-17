function formatDate(iso) {
  try {
    return new Date(iso).toLocaleString(undefined, {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    })
  } catch {
    return ''
  }
}

export default function HistoryPanel({ items, activeId, onSelect, onRefresh, error }) {
  return (
    <section className="history">
      <div className="history-header">
        <h3>History</h3>
        <button className="refresh-btn" onClick={onRefresh}>
          Refresh
        </button>
      </div>

      {error ? (
        <div className="empty">{error}</div>
      ) : items.length === 0 ? (
        <div className="empty">No research yet. Ask your first question above.</div>
      ) : (
        items.map((item) => (
          <button
            key={item.id}
            className={`history-item${item.id === activeId ? ' active' : ''}`}
            onClick={() => onSelect(item)}
          >
            <span className="history-q">{item.query}</span>
            <span className="history-meta">
              {formatDate(item.created_at)} · {(item.sources ?? []).length} source(s)
            </span>
          </button>
        ))
      )}
    </section>
  )
}
