import { useEffect } from 'react'
import { useNavigate, useParams, useSearchParams } from 'react-router-dom'
import { useJob } from '../api/hooks'

export function Generating() {
  const { id = '' } = useParams()
  const [params] = useSearchParams()
  const jobId = params.get('job') ?? ''
  const navigate = useNavigate()
  const job = useJob(jobId, true)

  useEffect(() => {
    if (job.data?.status === 'done') {
      navigate(`/interviews/${id}`, { replace: true })
    }
  }, [job.data?.status, id, navigate])

  const failed = job.data?.status === 'error'

  return (
    <div className="card">
      <p className="eyebrow">Generating</p>
      <h1>Building your interview sheet</h1>

      {!failed && (
        <p className="muted">
          <span className="spinner" aria-hidden="true" /> This can take a
          moment while we redact the resume and assemble questions from the
          Slalom guidelines…
        </p>
      )}

      {failed && (
        <>
          <div className="error-banner" role="alert">
            Generation failed: {job.data?.error ?? 'Unknown error'}
          </div>
          <button
            type="button"
            className="btn btn-ghost"
            onClick={() => navigate('/')}
          >
            Start over
          </button>
        </>
      )}

      {job.isError && (
        <div className="error-banner" role="alert">
          Could not check status: {(job.error as Error).message}
        </div>
      )}
    </div>
  )
}
