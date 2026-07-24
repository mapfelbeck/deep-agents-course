import { Link, useParams } from 'react-router-dom'
import { useInterview } from '../api/hooks'
import { AnnotatedSheet } from '../components/AnnotatedSheet'
import { Markdown } from '../components/Markdown'
import { Tabs } from '../components/Tabs'

export function InterviewSheet() {
  const { id = '' } = useParams()
  const interview = useInterview(id)

  if (interview.isLoading) {
    return (
      <div className="card">
        <span className="spinner" aria-hidden="true" /> Loading interview…
      </div>
    )
  }

  if (interview.isError || !interview.data) {
    return (
      <div className="card">
        <div className="error-banner" role="alert">
          Could not load interview:{' '}
          {(interview.error as Error)?.message ?? 'Not found'}
        </div>
        <Link className="btn btn-ghost" to="/history">
          Back to history
        </Link>
      </div>
    )
  }

  const data = interview.data

  if (data.status !== 'ready') {
    return (
      <div className="card">
        <p className="eyebrow">{data.role}</p>
        <h1>Interview sheet</h1>
        <p className="muted">
          This interview is <span className={`pill ${data.status}`}>{data.status}</span>.
        </p>
        {data.status !== 'error' && (
          <Link
            className="btn btn-primary"
            to={`/interviews/${data.id}/generating`}
          >
            View progress
          </Link>
        )}
      </div>
    )
  }

  return (
    <div>
      <div style={{ marginBottom: '1rem' }}>
        <p className="eyebrow">Interview sheet</p>
        <h1>{data.role}</h1>
        <p className="muted">
          {data.candidate ? `Candidate: ${data.candidate}` : 'No resume provided'}
        </p>
      </div>

      <Tabs
        items={[
          {
            id: 'sheet',
            label: 'Interview Sheet',
            content: (
              <div className="card">
                <AnnotatedSheet
                  interviewId={data.id}
                  sheetMd={data.sheet_md ?? ''}
                  initialNotesMd={data.notes_md}
                />
              </div>
            ),
          },
          {
            id: 'resume',
            label: 'Redacted Resume',
            content: (
              <div className="card">
                {data.resume_md ? (
                  <Markdown>{data.resume_md}</Markdown>
                ) : (
                  <p className="muted">No resume was provided for this interview.</p>
                )}
              </div>
            ),
          },
        ]}
      />
    </div>
  )
}
