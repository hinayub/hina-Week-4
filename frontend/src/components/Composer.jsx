import { useState } from 'react'

const EXAMPLES = [
  'Latest advances in fusion energy',
  'Who won the most recent Nobel Prize in Physics?',
  'Compare Rust and Go for backend services',
]

export default function Composer({ onSubmit, loading }) {
  const [value, setValue] = useState('')

  const submit = (q) => {
    const trimmed = q.trim()
    if (!trimmed || loading) return
    onSubmit(trimmed)
  }

  return (
    <div className="composer-wrap">
      <div className="composer">
        <textarea
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onKeyDown={(e) => {
            if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') submit(value)
          }}
          placeholder="What would you like to research?"
          rows={2}
          disabled={loading}
        />
        <div className="composer-actions">
          <span className="hint">
            Press <kbd>⌘/Ctrl</kbd> + <kbd>Enter</kbd> to research
          </span>
          <button
            className="primary"
            onClick={() => submit(value)}
            disabled={loading || !value.trim()}
          >
            {loading ? 'Researching…' : 'Research'}
          </button>
        </div>
      </div>

      <div className="examples">
        {EXAMPLES.map((ex) => (
          <button
            key={ex}
            className="chip"
            disabled={loading}
            onClick={() => {
              setValue(ex)
              submit(ex)
            }}
          >
            {ex}
          </button>
        ))}
      </div>
    </div>
  )
}
