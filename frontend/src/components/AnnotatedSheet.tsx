import { useEffect, useMemo, useRef, useState } from 'react'
import { useSaveNotes } from '../api/hooks'
import { Markdown } from './Markdown'
import { parseNotes, parseSheet, serializeNotes } from './notesDoc'

interface Props {
  interviewId: string
  sheetMd: string
  initialNotesMd: string
}

type SaveState = 'idle' | 'saving' | 'saved' | 'error'

const DEBOUNCE_MS = 800

export function AnnotatedSheet({ interviewId, sheetMd, initialNotesMd }: Props) {
  const { preamble, segments } = useMemo(() => parseSheet(sheetMd), [sheetMd])
  const [notes, setNotes] = useState<Record<string, string>>(() =>
    parseNotes(initialNotesMd),
  )
  const [saveState, setSaveState] = useState<SaveState>('idle')
  const saveNotes = useSaveNotes(interviewId)
  const timer = useRef<ReturnType<typeof setTimeout> | null>(null)

  useEffect(() => {
    return () => {
      if (timer.current) clearTimeout(timer.current)
    }
  }, [])

  const scheduleSave = (next: Record<string, string>) => {
    if (timer.current) clearTimeout(timer.current)
    setSaveState('saving')
    timer.current = setTimeout(() => {
      const doc = serializeNotes(next, segments)
      saveNotes.mutate(doc, {
        onSuccess: () => setSaveState('saved'),
        onError: () => setSaveState('error'),
      })
    }, DEBOUNCE_MS)
  }

  const onChange = (key: string, value: string) => {
    const next = { ...notes, [key]: value }
    setNotes(next)
    scheduleSave(next)
  }

  return (
    <div>
      <div className="save-status" role="status" aria-live="polite">
        {saveState === 'saving' && 'Saving notes…'}
        {saveState === 'saved' && 'Notes saved'}
        {saveState === 'error' && '⚠ Could not save notes — retrying on next edit'}
        {saveState === 'idle' && 'Notes autosave as you type'}
      </div>

      {preamble.trim() && <Markdown>{preamble}</Markdown>}

      {segments.map((seg) => (
        <section key={seg.key}>
          <Markdown>{seg.markdown}</Markdown>
          <div className="note-block">
            <label htmlFor={`note-${seg.key}`}>Notes</label>
            <textarea
              id={`note-${seg.key}`}
              placeholder={`Notes for “${seg.label}”`}
              value={notes[seg.key] ?? ''}
              onChange={(e) => onChange(seg.key, e.target.value)}
            />
          </div>
        </section>
      ))}
    </div>
  )
}
