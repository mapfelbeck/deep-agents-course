// Typed API client for the Interview Sheet backend.
// Uses relative /api paths; Vite proxies these to the FastAPI server in dev.

export interface Role {
  value: string
  label: string
  paths: string[]
}

export interface InterviewCreated {
  interview_id: string
  job_id: string
}

export type JobState = 'queued' | 'running' | 'done' | 'error'

export interface JobStatus {
  id: string
  interview_id: string
  status: JobState
  error: string | null
}

export type InterviewState = 'queued' | 'generating' | 'ready' | 'error'

export interface InterviewSummary {
  id: string
  role: string
  candidate: string | null
  status: InterviewState
  created_at: string
}

export interface InterviewDetail extends InterviewSummary {
  jd_paths: string[]
  sheet_md: string | null
  resume_md: string | null
  notes_md: string
  updated_at: string
}

export interface Notes {
  interview_id: string
  notes_md: string
  updated_at: string
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(path, init)
  if (!res.ok) {
    let detail = res.statusText
    try {
      const body = await res.json()
      if (body?.detail) detail = body.detail
    } catch {
      // ignore parse errors
    }
    throw new Error(detail)
  }
  if (res.status === 204) {
    return undefined as T
  }
  return (await res.json()) as T
}

export const api = {
  listRoles: () => request<Role[]>('/api/roles'),

  createInterview: (role: string, resume: File | null) => {
    const form = new FormData()
    form.append('role', role)
    if (resume) form.append('resume', resume)
    return request<InterviewCreated>('/api/interviews', {
      method: 'POST',
      body: form,
    })
  },

  getJob: (jobId: string) => request<JobStatus>(`/api/jobs/${jobId}`),

  listInterviews: () => request<InterviewSummary[]>('/api/interviews'),

  getInterview: (id: string) =>
    request<InterviewDetail>(`/api/interviews/${id}`),

  deleteInterview: (id: string) =>
    request<void>(`/api/interviews/${id}`, { method: 'DELETE' }),

  getNotes: (id: string) => request<Notes>(`/api/interviews/${id}/notes`),

  saveNotes: (id: string, notesMd: string) =>
    request<Notes>(`/api/interviews/${id}/notes`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ notes_md: notesMd }),
    }),
}
