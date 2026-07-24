import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { createBrowserRouter, Navigate, RouterProvider } from 'react-router-dom'
import './theme.css'
import App from './App.tsx'
import { NewInterview } from './routes/NewInterview.tsx'
import { Generating } from './routes/Generating.tsx'
import { InterviewSheet } from './routes/InterviewSheet.tsx'
import { History } from './routes/History.tsx'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      staleTime: 30_000,
    },
  },
})

const router = createBrowserRouter([
  {
    path: '/',
    element: <App />,
    children: [
      { index: true, element: <NewInterview /> },
      { path: 'history', element: <History /> },
      { path: 'interviews/:id', element: <InterviewSheet /> },
      { path: 'interviews/:id/generating', element: <Generating /> },
      { path: '*', element: <Navigate to="/" replace /> },
    ],
  },
])

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={router} />
    </QueryClientProvider>
  </StrictMode>,
)
