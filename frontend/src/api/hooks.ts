// TanStack Query hooks wrapping the API client.
import {
  useMutation,
  useQuery,
  useQueryClient,
  type UseQueryResult,
} from '@tanstack/react-query'
import {
  api,
  type InterviewDetail,
  type InterviewSummary,
  type JobStatus,
  type Role,
} from './client'

export function useRoles(): UseQueryResult<Role[]> {
  return useQuery({ queryKey: ['roles'], queryFn: api.listRoles })
}

export function useInterviews(): UseQueryResult<InterviewSummary[]> {
  return useQuery({ queryKey: ['interviews'], queryFn: api.listInterviews })
}

export function useInterview(id: string): UseQueryResult<InterviewDetail> {
  return useQuery({
    queryKey: ['interview', id],
    queryFn: () => api.getInterview(id),
    enabled: Boolean(id),
  })
}

export function useJob(
  jobId: string,
  poll: boolean,
): UseQueryResult<JobStatus> {
  return useQuery({
    queryKey: ['job', jobId],
    queryFn: () => api.getJob(jobId),
    enabled: Boolean(jobId),
    refetchInterval: (query) => {
      const state = query.state.data?.status
      return poll && state !== 'done' && state !== 'error' ? 1500 : false
    },
  })
}

export function useCreateInterview() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: ({ role, resume }: { role: string; resume: File | null }) =>
      api.createInterview(role, resume),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['interviews'] })
    },
  })
}

export function useDeleteInterview() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (id: string) => api.deleteInterview(id),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['interviews'] })
    },
  })
}

export function useSaveNotes(interviewId: string) {
  return useMutation({
    mutationFn: (notesMd: string) => api.saveNotes(interviewId, notesMd),
  })
}
