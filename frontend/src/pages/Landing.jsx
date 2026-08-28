import { Link, useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { ArrowRight, BookOpen, Zap, FileDown, RefreshCw, Sparkles } from "lucide-react";
import { useAuth } from "@/lib/auth";
import { useI18n } from "@/lib/i18n";
import LangToggle from "@/components/LangToggle";

export default function Landing() {
  const nav = useNavigate();
  const { user } = useAuth();
  const { t } = useI18n();

  return (
    <div className="min-h-screen bg-black text-white font-body relative overflow-x-hidden">
      {/* NAV */}
      <nav className="sticky top-0 z-40 backdrop-blur-xl bg-black/70 border-b border-zinc-900">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <Link to="/" className="flex items-center gap-3" data-testid="nav-logo-link">
            <img src="/teachkit-logo.webp" alt="THE TEACHKIT" className="h-10 w-10" />
            <span className="font-display font-bold text-lg tracking-tight">
              <span className="text-lime">[THE]</span> TEACHKIT
            </span>
          </Link>
          <div className="flex items-center gap-3">
            <LangToggle variant="dark" />
            {user ? (
              <Button data-testid="nav-dashboard-btn" onClick={() => nav("/dashboard")} className="bg-lime text-black hover:bg-[#8BC926] rounded-full px-5 hover-lift">
                {t("nav.dashboard")} <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
            ) : (
              <>
                <Button data-testid="nav-login-btn" onClick={() => nav("/auth?mode=login")} variant="ghost" className="text-white hover:bg-zinc-900 rounded-full">{t("nav.login")}</Button>
                <Button data-testid="nav-signup-btn" onClick={() => nav("/auth?mode=signup")} className="bg-lime text-black hover:bg-[#8BC926] rounded-full px-5 hover-lift">{t("nav.signup")}</Button>
              </>
            )}
          </div>
        </div>
      </nav>

      {/* HERO */}
      <section className="relative grain">
        <div className="max-w-7xl mx-auto px-6 pt-20 pb-28 relative z-10">
          <div className="grid lg:grid-cols-12 gap-12 items-center">
            <div className="lg:col-span-7 animate-slide-up">
              <div className="inline-flex items-center gap-2 px-3 py-1 border border-zinc-800 rounded-full text-xs uppercase tracking-widest text-zinc-400 mb-8">
                <Sparkles className="h-3.5 w-3.5 text-lime" />
                {t("landing.badge")}
              </div>
              <h1 className="font-display font-bold text-5xl sm:text-6xl lg:text-7xl leading-[0.95] tracking-tight">
                {t("landing.hero_title_a")}<br />
                {t("landing.hero_title_b")}<br />
                {t("landing.hero_title_c")}<br />
                <span className="text-lime">{t("landing.hero_title_d")}</span>
              </h1>
              <p className="mt-8 text-lg text-zinc-400 max-w-xl leading-relaxed">
                {t("landing.hero_desc")}
              </p>
              <div className="mt-10 flex flex-wrap gap-4">
                <Button data-testid="hero-cta-btn" onClick={() => nav(user ? "/dashboard" : "/auth?mode=signup")} className="bg-lime text-black hover:bg-[#8BC926] rounded-full px-7 py-6 text-base font-semibold hover-lift">
                  {t("landing.cta_primary")} <ArrowRight className="ml-2 h-5 w-5" />
                </Button>
                <Button data-testid="hero-secondary-btn" onClick={() => document.getElementById("features")?.scrollIntoView({ behavior: "smooth" })} variant="ghost" className="text-white border border-zinc-800 hover:bg-zinc-900 rounded-full px-7 py-6 text-base">
                  {t("landing.cta_secondary")}
                </Button>
              </div>
              <div className="mt-12 flex items-center gap-8 text-xs uppercase tracking-widest text-zinc-500">
                <div><span className="text-lime text-lg font-display font-bold">32</span> weeks</div>
                <div><span className="text-lime text-lg font-display font-bold">A1→A2</span> CECRL</div>
                <div><span className="text-lime text-lg font-display font-bold">PPP</span> framework</div>
              </div>
            </div>

            <div className="lg:col-span-5 relative">
              <div className="relative aspect-square w-full max-w-lg mx-auto">
                <div className="absolute inset-0 bg-lime rounded-none rotate-3 opacity-90" />
                <div className="absolute inset-0 bg-white -rotate-2 flex items-center justify-center p-10 shadow-2xl">
                  <img src="/teachkit-logo.webp" alt="THE TEACHKIT logo" className="max-w-full max-h-full object-contain" data-testid="hero-logo-img" />
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* FEATURES */}
      <section id="features" className="border-t border-zinc-900 bg-black">
        <div className="max-w-7xl mx-auto px-6 py-24">
          <div className="text-xs uppercase tracking-widest text-lime mb-3">What you get</div>
          <h2 className="font-display font-bold text-4xl sm:text-5xl tracking-tight max-w-2xl">
            A dashboard that respects your time.
          </h2>

          <div className="mt-16 grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[
              { icon: Zap, title: "Instant Syllabus", desc: "Generate 32 weeks of themed lessons aligned with the French national curriculum in one click." },
              { icon: BookOpen, title: "PPP Framework", desc: "Every lesson follows Presentation → Practice → Production, with timings, activities and skill focus." },
              { icon: RefreshCw, title: "Swap Activities", desc: "Don't like an activity? Ask the AI for a fresh alternative — same phase, same skill, brand new idea." },
              { icon: FileDown, title: "Professional PDFs", desc: "Export a beautifully branded lesson or the entire syllabus as a print-ready PDF in seconds." },
              { icon: Sparkles, title: "Priority Skills", desc: "Rank Speaking, Listening, Reading, Writing — the generator tailors activities to what matters to you." },
              { icon: BookOpen, title: "Current-Week Auto", desc: "Your dashboard opens on this week's lesson, every time. No scrolling, no searching." },
            ].map((f, i) => (
              <div key={i} data-testid={`feature-card-${i}`} className="bg-white text-black p-8 border border-zinc-200 hover-lift">
                <f.icon className="h-8 w-8 text-black" strokeWidth={1.5} />
                <h3 className="font-display font-bold text-xl mt-6 tracking-tight">{f.title}</h3>
                <p className="mt-3 text-sm text-zinc-600 leading-relaxed">{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="border-t border-zinc-900">
        <div className="max-w-7xl mx-auto px-6 py-24 text-center">
          <h2 className="font-display font-bold text-4xl sm:text-5xl tracking-tight">
            Ready to reclaim your Sunday nights?
          </h2>
          <p className="mt-4 text-zinc-400 max-w-xl mx-auto">Join teachers who plan smarter, not harder.</p>
          <Button data-testid="footer-cta-btn" onClick={() => nav(user ? "/dashboard" : "/auth?mode=signup")} className="mt-10 bg-lime text-black hover:bg-[#8BC926] rounded-full px-8 py-6 text-base font-semibold hover-lift">
            Get started free <ArrowRight className="ml-2 h-5 w-5" />
          </Button>
        </div>
      </section>

      <footer className="border-t border-zinc-900">
        <div className="max-w-7xl mx-auto px-6 py-10 flex flex-col md:flex-row items-center justify-between gap-4 text-sm text-zinc-500">
          <div className="flex items-center gap-3">
            <img src="/teachkit-logo.webp" alt="" className="h-7 w-7" />
            <span>© {new Date().getFullYear()} THE TEACHKIT</span>
          </div>
          <Link to="/gallery" data-testid="footer-gallery-link" className="text-lime hover:underline uppercase tracking-widest text-xs">
            {t("gallery.link")} →
          </Link>
          <div className="uppercase tracking-widest text-xs">Made for French classrooms · Loved by teachers</div>
        </div>
      </footer>
    </div>
  );
}
