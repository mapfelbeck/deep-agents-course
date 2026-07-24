import { type ReactNode, useId, useState } from 'react'

export interface TabItem {
  id: string
  label: string
  content: ReactNode
}

export function Tabs({ items }: { items: TabItem[] }) {
  const [active, setActive] = useState(items[0]?.id)
  const baseId = useId()

  return (
    <div>
      <div className="tabs" role="tablist" aria-label="Interview views">
        {items.map((item) => (
          <button
            key={item.id}
            type="button"
            role="tab"
            id={`${baseId}-tab-${item.id}`}
            aria-selected={active === item.id}
            aria-controls={`${baseId}-panel-${item.id}`}
            className="tab"
            onClick={() => setActive(item.id)}
          >
            {item.label}
          </button>
        ))}
      </div>
      {items.map((item) => (
        <div
          key={item.id}
          role="tabpanel"
          id={`${baseId}-panel-${item.id}`}
          aria-labelledby={`${baseId}-tab-${item.id}`}
          hidden={active !== item.id}
        >
          {active === item.id ? item.content : null}
        </div>
      ))}
    </div>
  )
}
