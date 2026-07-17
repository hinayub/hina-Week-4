export default function SourceList({ sources }) {
  if (!sources.length) return null

  return (
    <div className="sources">
      <div className="sources-title">Sources ({sources.length})</div>
      {sources.map((s, i) => (
        <a
          key={s.link + i}
          className="source"
          href={s.link}
          target="_blank"
          rel="noopener noreferrer"
        >
          <span className="source-num">{i + 1}</span>
          <span className="source-body">
            <span className="source-title">{s.title || s.link}</span>
            <span className="source-link">{s.link}</span>
          </span>
        </a>
      ))}
    </div>
  )
}
