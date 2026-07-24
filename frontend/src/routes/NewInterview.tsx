import { useMemo, useState, type FormEvent } from 'react'
import { useNavigate } from 'react-router-dom'
import { useCreateInterview, useRoles } from '../api/hooks'

export function NewInterview() {
  const navigate = useNavigate()
  const roles = useRoles()
  const create = useCreateInterview()

  const [role, setRole] = useState('')
  const [resume, setResume] = useState<File | null>(null)
  const [fileError, setFileError] = useState<string | null>(null)

  const sortedRoles = useMemo(
    () => (roles.data ? [...roles.data].sort((a, b) => a.label.localeCompare(b.label)) : []),
    [roles.data],
  )

  const onFileChange = (file: File | null) => {
    setFileError(null)
    if (file) {
      const name = file.name.toLowerCase()
      if (!name.endsWith('.pdf') && !name.endsWith('.md')) {
        setFileError('Please choose a .pdf or .md file.')
        setResume(null)
        return
      }
    }
    setResume(file)
  }

  const onSubmit = async (e: FormEvent) => {
    e.preventDefault()
    if (!role) return
    const selected = sortedRoles.find((r) => r.value === role)
    const created = await create.mutateAsync({
      role: selected?.label ?? role,
      resume,
    })
    navigate(`/interviews/${created.interview_id}/generating?job=${created.job_id}`)
  }

  return (
    <div className="card">
      <p className="eyebrow">New interview</p>
      <h1>Prepare an interview sheet</h1>
      <p className="muted">
        Choose the role and, optionally, upload the candidate resume. The resume
        is always PII-redacted before it is used or stored.
      </p>

      {roles.isError && (
        <div className="error-banner" role="alert">
          Could not load roles: {(roles.error as Error).message}
        </div>
      )}
      {create.isError && (
        <div className="error-banner" role="alert">
          Could not start generation: {(create.error as Error).message}
        </div>
      )}

      <form onSubmit={onSubmit}>
        <div className="field">
          <label htmlFor="role">Role</label>
          <select
            id="role"
            value={role}
            required
            disabled={roles.isLoading}
            onChange={(e) => setRole(e.target.value)}
          >
            <option value="" disabled>
              {roles.isLoading ? 'Loading roles…' : 'Select a role…'}
            </option>
            {sortedRoles.map((r) => (
              <option key={r.value} value={r.value}>
                {r.label}
              </option>
            ))}
          </select>
        </div>

        <div className="field">
          <label htmlFor="resume">Candidate resume (optional)</label>
          <input
            id="resume"
            type="file"
            accept=".pdf,.md"
            onChange={(e) => onFileChange(e.target.files?.[0] ?? null)}
          />
          <p className="help">Accepts .pdf or .md. Redacted automatically.</p>
          <p>If no resume is provided, the system will generate a general interview sheet for the role.</p>
          {fileError && (
            <p className="help" style={{ color: 'var(--color-accent-coral)' }}>
              {fileError}
            </p>
          )}
        </div>

        <button
          type="submit"
          className="btn btn-primary"
          disabled={!role || create.isPending}
        >
          {create.isPending ? 'Starting…' : 'Generate interview sheet'}
        </button>
      </form>
    </div>
  )
}
