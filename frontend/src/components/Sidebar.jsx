
import {
  BrainCircuit,
  Layers,
  Newspaper,
  Cpu,
  TrendingUp,
  Globe,
  UserRound,
} from "lucide-react";

const menuItems = [
  { label: "Overview", icon: Layers, value: "Overview" },
  { label: "News Intelligence", icon: Newspaper, value: "News Intelligence" },
  { label: "Technology", icon: Cpu, value: "Technology" },
  { label: "Business", icon: TrendingUp, value: "Business" },
  { label: "Other News", icon: Globe, value: "Other News" },
];

export default function Sidebar({
  activeMenu = "Overview",
  onMenuChange = () => {},
}) {
  return (
    <aside className="sidebar">
      <div className="sidebar-brand">
        <div className="brand-icon">
          <BrainCircuit size={30} />
        </div>
        <div>
          <h2>NEWSGEN<span>AI</span></h2>
          <p>INTELLIGENCE OS</p>
        </div>
      </div>

      <div className="sidebar-section">
        <p className="sidebar-heading">WORKSPACE</p>

        <nav className="sidebar-nav">
          {menuItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeMenu === item.value;

            return (
              <button
                key={item.value}
                className={`sidebar-item ${isActive ? "active" : ""}`}
                onClick={() => onMenuChange(item.value)}
                type="button"
              >
                <Icon size={21} />
                <span>{item.label}</span>
                {isActive && <span className="active-dot" />}
              </button>
            );
          })}
        </nav>
      </div>

      <div className="sidebar-bottom">
        <div className="sidebar-user-icon">
          <UserRound size={20} />
        </div>
        <div>
          <strong>NewsGen AI</strong>
          <p>Personal workspace</p>
        </div>
      </div>
    </aside>
  );
}
