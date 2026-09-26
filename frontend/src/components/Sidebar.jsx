const navItems = [
  { id: 'dashboard', label: 'Dashboard', icon: '⌂' },
  { id: 'knowledge-base', label: 'Knowledge Base', icon: '▣' },
  { id: 'ask-ai', label: 'Ask AI', icon: '✦' },
  { id: 'search-history', label: 'Search History', icon: '◫' },
  { id: 'settings', label: 'Settings', icon: '⚙' },
];

function Sidebar({ activePage, onNavigate }) {
  return (
    <aside className="sidebar">
      <div className="brand-block">
        <div className="brand-mark">AI</div>
        <div>
          <h1 className="brand-name">AI Knowledge Hub</h1>
          <p className="brand-subtitle">Knowledge Retrieval Platform</p>
        </div>
      </div>

      <nav className="sidebar-nav" aria-label="Main navigation">
        {navItems.map((item) => (
          <button
            key={item.id}
            type="button"
            className={`nav-item ${activePage === item.id ? 'active' : ''}`}
            onClick={() => onNavigate(item.id)}
          >
            <span className="nav-icon" aria-hidden="true">{item.icon}</span>
            <span>{item.label}</span>
          </button>
        ))}
      </nav>

      <div className="profile-box">
        <div className="profile-avatar">S</div>
        <div>
          <div className="profile-name">User</div>
          <div className="profile-role">Student</div>
        </div>
      </div>
    </aside>
  );
}

export default Sidebar;
