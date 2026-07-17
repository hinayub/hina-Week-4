import SourceList from "./SourceList";

export default function ResultCard({ result }) {
  return (
    <div className="card">
      <div className="q-label">Question</div>
      <h2 className="q-text">{result.query}</h2>
      <div className="answer">
        {result.answer || (
          <em className="muted">No answer was returned for this query.</em>
        )}
      </div>
      <SourceList sources={result.sources ?? []} />
    </div>
  );
}
