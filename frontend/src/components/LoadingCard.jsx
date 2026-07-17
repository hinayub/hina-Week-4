export default function LoadingCard() {
  return (
    <div className="card">
      <div className="loading">
        <span className="spinner" /> Searching the web and reasoning…
      </div>
      <div className="skeleton" style={{ width: "92%" }} />
      <div className="skeleton" style={{ width: "82%" }} />
      <div className="skeleton" style={{ width: "64%" }} />
    </div>
  );
}
