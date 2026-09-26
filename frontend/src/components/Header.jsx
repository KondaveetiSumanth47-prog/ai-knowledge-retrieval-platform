function Header({ title }) {
  return (
    <header className="topbar">
      <div className="topbar-title">{title}</div>

      <div className="topbar-actions">
        <button type="button" className="icon-button" aria-label="Notifications">
          🔔
        </button>
        <div className="user-pill">
          <span className="user-avatar">S</span>
          <span className="user-name">Student</span>
        </div>
      </div>
    </header>
  );
}

export default Header;
