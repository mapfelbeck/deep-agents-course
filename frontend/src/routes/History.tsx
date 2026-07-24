import { Link } from 'react-router-dom'
import { useInterviews } from '../api/hooks'

function formatDate(iso: string): string {
  const d = new Date(iso)
  return Number.isNaN(d.getTime()) ? iso : d.toLocaleString()
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
            <li key={it.id} className="card" style={{ padding: '1rem' }}>
              <Link to={`/interviews/${it.id}`}>
                <span>
                  <span className="interview-role">{it.role}</span>
                  <br />
                  <span className="muted">
                    {it.candidate ?? 'No resume'} · {formatDate(it.created_at)}
                  </span>
                </span>
                <span className={`pill ${it.status}`}>{it.status}</span>
              </Link>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
