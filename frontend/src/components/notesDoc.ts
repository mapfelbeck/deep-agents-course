// Utilities to interleave editable note blocks into a generated interview sheet
// and to (de)serialize those notes as a single plain-markdown document.

export interface SheetSegment {
  /** Stable key for this anchor within the (immutable) sheet. */
  key: string
  /** Markdown for this segment: the anchor line plus its body up to the next. */
  markdown: string
  /** Short label describing the anchor, shown on the note block. */
  label: string
}

export interface ParsedSheet {
  preamble: string
  segments: SheetSegment[]
}

// Anchors: section headings (## / ### / ####) and numbered questions ("1. ...").
const ANCHOR_RE = /^(#{2,4}\s+.+|\s*\d+\.\s+.+)$/

function anchorLabel(line: string): string {
  const text = line.replace(/^#{2,4}\s+/, '').replace(/^\s*\d+\.\s+/, '')
  const clean = text.replace(/[*_`]/g, '').trim()
  return clean.length > 80 ? `${clean.slice(0, 77)}…` : clean
}

/** Split a sheet into a preamble plus note-annotated segments. */
export function parseSheet(sheetMd: string): ParsedSheet {
  const lines = sheetMd.split('\n')
  const preambleLines: string[] = []
  const segments: SheetSegment[] = []

  let current: { label: string; lines: string[] } | null = null
  let index = 0

  const flush = () => {
    if (current) {
      segments.push({
        key: `a${index++}`,
        markdown: current.lines.join('\n'),
        label: current.label,
      })
    }
  }

  for (const line of lines) {
    if (ANCHOR_RE.test(line)) {
      flush()
      current = { label: anchorLabel(line), lines: [line] }
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
