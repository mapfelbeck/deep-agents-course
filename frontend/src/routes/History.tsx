import { Link } from 'react-router-dom'
import { useDeleteInterview, useInterviews } from '../api/hooks'
import type { InterviewSummary } from '../api/client'

function formatDate(iso: string): string {
  const d = new Date(iso)
  return Number.isNaN(d.getTime()) ? iso : d.toLocaleString()
}

function HistoryItem({ it }: { it: InterviewSummary }) {
  const del = useDeleteInterview()

  function handleDelete() {
    const label = it.candidate ? `${it.role} — ${it.candidate}` : it.role
    if (!window.confirm(`Delete this interview?\n\n${label}`)) return
    del.mutate(it.id)
  }

  return (
    <li className="card interview-item" style={{ padding: '1rem' }}>
      <Link to={`/interviews/${it.id}`} className="interview-item-link">
        <span>
          <span className="interview-role">{it.role}</span>
          <br />
          <span className="muted">
            {it.candidate ?? 'No resume'} · {formatDate(it.created_at)}
          </span>
        </span>
        <span className={`pill ${it.status}`}>{it.status}</span>
      </Link>
      <button
        type="button"
        className="btn btn-danger"
        onClick={handleDelete}
        disabled={del.isPending}
        aria-label={`Delete interview for ${it.role}`}
      >
        {del.isPending ? 'Deleting…' : 'Delete'}
      </button>
    </li>
  )
}

export function History() {
  const interviews = useInterviews()

  return (
    <div className="card">
      <p className="eyebrow">History</p>
      <h1>Past interviews</h1>

      {interviews.isLoading && (
        <p className="muted">
          <span className="spinner" aria-hidden="true" /> Loading…
        </p>
      )}

      {interviews.isError && (
        <div className="error-banner" role="alert">
          Could not load interviews: {(interviews.error as Error).message}
        </div>
      )}

      {interviews.data && interviews.data.length === 0 && (
        <p className="muted">
          No interviews yet. <Link to="/">Create your first one.</Link>
        </p>
      )}

      {interviews.data && interviews.data.length > 0 && (
        <ul className="interview-list">
          {interviews.data.map((it) => (
            <HistoryItem key={it.id} it={it} />
          ))}
        </ul>
      )}
    </div>
  )
}
