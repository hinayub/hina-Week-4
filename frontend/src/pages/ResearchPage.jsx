import { useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import {
  runResearch,
  fetchHistory,
  selectResult,
} from '../redux/actions/researchActions'
import Composer from '../components/Composer'
import ResultCard from '../components/ResultCard'
import LoadingCard from '../components/LoadingCard'
import HistoryPanel from '../components/HistoryPanel'

export default function ResearchPage() {
  const dispatch = useDispatch()
  const { loading, result, error, history, historyError } = useSelector(
    (state) => state.research,
  )

  useEffect(() => {
    dispatch(fetchHistory())
  }, [dispatch])

  const handleSubmit = (query) => dispatch(runResearch(query))

  const handleSelect = (item) => {
    dispatch(selectResult(item))
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  return (
    <div className="app">
      <header className="hero">
        <div className="logo">
          <div className="logo-mark">🔎</div>
          <h1>Research Agent</h1>
        </div>
        <p className="subtitle">
          Ask anything. The agent searches the web and answers with cited sources.
        </p>
      </header>

      <Composer onSubmit={handleSubmit} loading={loading} />

      {loading && <LoadingCard />}
      {error && <div className="error">⚠️ {error}</div>}
      {!loading && result && <ResultCard result={result} />}

      <HistoryPanel
        items={history}
        activeId={result?.id}
        onSelect={handleSelect}
        onRefresh={() => dispatch(fetchHistory())}
        error={historyError}
      />
    </div>
  )
}
