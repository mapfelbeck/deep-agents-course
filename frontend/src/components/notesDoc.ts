// Utilities to interleave editable note blocks into a generated interview sheet
// and to (de)serialize those notes as a single plain-markdown document.

export interface SheetSegment {
  /** Stable key for this anchor within the (immutable) sheet. */
  key: string
  /** Markdown for this segment: the anchor line plus its body up to the next. */
  markdown: string
  /** Short label describing the anchor, shown on the note block. */
  label: string
  /** Whether this segment is a question (gets a Notes box) vs. a heading. */
  isQuestion: boolean
}

export interface ParsedSheet {
  preamble: string
  segments: SheetSegment[]
}

// Anchors that break the sheet into segments: section headings (## / ### / ####)
// and questions (numbered items, plus bullets under a "…Questions…" heading).
const HEADING_RE = /^#{2,4}\s+.+$/
const NUMBERED_RE = /^\s*\d+\.\s+.+$/
const BULLET_RE = /^\s*[-*]\s+.+$/

function anchorLabel(line: string): string {
  const text = line
    .replace(/^#{2,4}\s+/, '')
    .replace(/^\s*\d+\.\s+/, '')
    .replace(/^\s*[-*]\s+/, '')
  const clean = text.replace(/[*_`]/g, '').trim()
  return clean.length > 80 ? `${clean.slice(0, 77)}…` : clean
}

/** Split a sheet into a preamble plus note-annotated segments. */
export function parseSheet(sheetMd: string): ParsedSheet {
  const lines = sheetMd.split('\n')
  const preambleLines: string[] = []
  const segments: SheetSegment[] = []

  let current: { label: string; lines: string[]; isQuestion: boolean } | null =
    null
  let index = 0
  // Nearest preceding heading text, used to decide if a bullet is a question.
  let currentHeading = ''

  const flush = () => {
    if (current) {
      segments.push({
        key: `a${index++}`,
        markdown: current.lines.join('\n'),
        label: current.label,
        isQuestion: current.isQuestion,
      })
    }
  }

  for (const line of lines) {
    const isHeading = HEADING_RE.test(line)
    const isNumbered = NUMBERED_RE.test(line)
    const isQuestionBullet =
      BULLET_RE.test(line) && /question/i.test(currentHeading)

    if (isHeading || isNumbered || isQuestionBullet) {
      flush()
      current = {
        label: anchorLabel(line),
        lines: [line],
        isQuestion: isNumbered || isQuestionBullet,
      }
      if (isHeading) currentHeading = line
    } else if (current) {
      current.lines.push(line)
    } else {
      preambleLines.push(line)
    }
  }
  flush()

  return { preamble: preambleLines.join('\n'), segments }
}

const NOTE_BLOCK_RE = /<!--\s*note:([^\s]+)\s*-->\n([\s\S]*?)\n<!--\s*\/note\s*-->/g

/** Parse a saved notes markdown document into a { key: text } map. */
export function parseNotes(notesMd: string): Record<string, string> {
  const map: Record<string, string> = {}
  let match: RegExpExecArray | null
  NOTE_BLOCK_RE.lastIndex = 0
  while ((match = NOTE_BLOCK_RE.exec(notesMd)) !== null) {
    map[match[1]] = match[2]
  }
  return map
}

/** Serialize a { key: text } map back into one plain-markdown notes document. */
export function serializeNotes(
  notes: Record<string, string>,
  segments: SheetSegment[],
): string {
  const blocks: string[] = []
  for (const seg of segments) {
    const text = (notes[seg.key] ?? '').trim()
    if (!text) continue
    blocks.push(
      `<!-- note:${seg.key} -->\n${text}\n<!-- /note -->\n<!-- ${seg.label} -->`,
    )
  }
  return blocks.join('\n\n')
}
