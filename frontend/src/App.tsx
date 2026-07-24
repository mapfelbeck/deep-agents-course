import { NavLink, Outlet } from 'react-router-dom'

function App() {
  return (
    <div className="app-shell">
      <header className="app-header">
        <NavLink to="/" className="brand">
          Interview Sheets
        </NavLink>
        <nav className="app-nav">
          <NavLink to="/" end>
            New interview
          </NavLink>
          <NavLink to="/history">History</NavLink>
        </nav>
      </header>
      <main className="app-main">
        <Outlet />
      </main>
    </div>
  )
}

export default App
