import { Link, useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "@/lib/auth";
import { useI18n } from "@/lib/i18n";
import { LayoutDashboard, UserCircle, LogOut } from "lucide-react";
import { Button } from "@/components/ui/button";
import LangToggle from "@/components/LangToggle";

export default function Layout({ children }) {
  const { user, logout } = useAuth();
  const { t } = useI18n();
  const nav = useNavigate();
  const loc = useLocation();

  const item = (to, icon, label, testid) => {
    const Icon = icon;
    const active = loc.pathname.startsWith(to);
    return (
      <Link to={to} data-testid={testid}
        className={`flex items-center gap-3 px-4 py-3 border-l-2 transition-colors text-sm ${active ? "border-lime text-white bg-zinc-950" : "border-transparent text-zinc-400 hover:text-white hover:bg-zinc-950"}`}>
        <Icon className="h-4 w-4" />
        <span className="uppercase tracking-widest text-xs">{label}</span>
      </Link>
    );
  };

  return (
    <div className="min-h-screen bg-black text-white font-body flex">
      <aside className="w-64 shrink-0 bg-black border-r border-zinc-900 flex flex-col sticky top-0 h-screen">
        <Link to="/dashboard" className="flex items-center gap-3 px-6 py-6 border-b border-zinc-900" data-testid="side-logo-link">
          <img src="/teachkit-logo.webp" alt="" className="h-10 w-10" />
          <div className="leading-tight">
            <div className="font-display font-bold"><span className="text-lime">[THE]</span> TEACHKIT</div>
            <div className="text-[10px] uppercase tracking-widest text-zinc-500">{t("side.lesson_planner")}</div>
          </div>
        </Link>
        <nav className="py-4 flex-1">
          {item("/dashboard", LayoutDashboard, t("side.syllabus"), "side-nav-dashboard")}
          {item("/profile", UserCircle, t("side.profile"), "side-nav-profile")}
        </nav>
        <div className="border-t border-zinc-900 p-4 space-y-3">
          <LangToggle variant="dark" />
          <div>
            <div className="text-xs text-zinc-500 mb-1">{t("side.signed_in_as")}</div>
            <div className="text-sm text-white truncate" data-testid="side-user-name">{user?.full_name}</div>
            <div className="text-xs text-zinc-500 truncate">{user?.email}</div>
          </div>
          <Button data-testid="side-logout-btn" onClick={() => { logout(); nav("/"); }} variant="ghost" size="sm"
            className="w-full justify-start text-zinc-400 hover:text-white hover:bg-zinc-950 rounded-none">
            <LogOut className="h-4 w-4 mr-2" /> {t("nav.logout")}
          </Button>
        </div>
      </aside>
      <main className="flex-1 min-w-0">{children}</main>
    </div>
  );
}
