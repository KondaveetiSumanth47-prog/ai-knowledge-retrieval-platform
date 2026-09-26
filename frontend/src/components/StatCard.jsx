function StatCard({ title, value, icon }) {
  return (
    <div className="stat-card">
      <div className="stat-icon" aria-hidden="true">{icon}</div>
      <div>
        <div className="stat-title">{title}</div>
        <div className="stat-value">{value}</div>
      </div>
    </div>
  );
}

export default StatCard;
