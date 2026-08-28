import { useEffect, useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import Layout from "@/components/Layout";
import api, { getErrorMessage } from "@/lib/api";
import { useAuth } from "@/lib/auth";
import { useI18n } from "@/lib/i18n";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";
import { getCurrentSchoolWeek } from "@/lib/schoolWeek";
import { exportSyllabusPdf } from "@/lib/pdfExport";
import { ArrowRight, FileDown, RefreshCw, Calendar, Sparkles, Package, Share2, Link as LinkIcon, BarChart3, Layers, Mail } from "lucide-react";
import { Switch } from "@/components/ui/switch";
import { Send } from "lucide-react";

export default function Dashboard() {
  const { user } = useAuth();
  const { t, lang } = useI18n();
  const nav = useNavigate();
  const [syllabus, setSyllabus] = useState(null);
  const [loading, setLoading] = useState(true);
  const [regenerating, setRegenerating] = useState(false);
  const [weekInfo, setWeekInfo] = useState({ current_week: 1, in_holiday: false, holiday_name: "", holidays: [] });
  const [batch, setBatch] = useState({ status: "idle", done: 0, total: 32, current_week: null });
  const [shareBusy, setShareBusy] = useState(false);
  const pollRef = useRef(null);
  const currentWeek = weekInfo.current_week || getCurrentSchoolWeek(user?.school_year_start);

  const load = async () => {
    try {
      const [sylRes, weekRes] = await Promise.all([
        api.get("/syllabus/active").catch((e) => { if (e.response?.status === 404) return null; throw e; }),
        api.get("/school-week").catch(() => null),
      ]);
      if (sylRes) setSyllabus(sylRes.data);
      if (weekRes) setWeekInfo(weekRes.data);
    } catch (e) {
      toast.error("Failed to load syllabus");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, []);

  useEffect(() => {
    if (syllabus) {
      // Scroll current week card into view
      setTimeout(() => {
        const el = document.querySelector(`[data-week="${currentWeek}"]`);
        el?.scrollIntoView({ behavior: "smooth", block: "center" });
      }, 200);
    }
  }, [syllabus, currentWeek]);

  const regenerate = async () => {
    setRegenerating(true);
    try {
      const r = await api.post("/syllabus/generate", {
        priorities: user.priorities,
        activity_types: user.activity_types,
      });
      setSyllabus(r.data);
      toast.success("Fresh syllabus generated!");
    } catch (e) {
      toast.error("Failed to regenerate");
    } finally {
      setRegenerating(false);
    }
  };

  const exportAll = () => {
    if (!syllabus) return;
    exportSyllabusPdf(syllabus, user);
    toast.success("Syllabus PDF downloaded");
  };

  // Batch pack generation
  const pollBatch = async () => {
    if (!syllabus) return;
    try {
      const r = await api.get(`/syllabus/${syllabus.id}/batch-status`);
      setBatch(r.data);
      if (r.data.status === "complete" || r.data.status === "idle") {
        clearInterval(pollRef.current);
        pollRef.current = null;
        if (r.data.status === "complete") {
          toast.success(`Generated ${r.data.done} teacher packs!`);
          load();
        }
      }
    } catch (e) { /* silent */ }
  };

  useEffect(() => {
    if (!syllabus) return;
    (async () => {
      try {
        const r = await api.get(`/syllabus/${syllabus.id}/batch-status`);
        setBatch(r.data);
        if (r.data.status === "running" && !pollRef.current) {
          pollRef.current = setInterval(pollBatch, 4000);
        }
      } catch (e) { /* silent */ }
    })();
    return () => { if (pollRef.current) { clearInterval(pollRef.current); pollRef.current = null; } };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [syllabus?.id]);

  const startBatch = async () => {
    try {
      const r = await api.post(`/syllabus/${syllabus.id}/batch-enrich`);
      setBatch(r.data);
      if (r.data.status === "started" || r.data.status === "running" || r.data.status === "already_running") {
        toast.info("Batch pack generation started — this can take 15-30 minutes.");
        if (!pollRef.current) pollRef.current = setInterval(pollBatch, 4000);
      } else if (r.data.status === "complete") {
        toast.success(r.data.message || "All packs already generated");
      }
    } catch (e) {
      toast.error(getErrorMessage(e, "Batch start failed"));
    }
  };

  const packedCount = syllabus ? syllabus.lessons.filter((l) => l.pack).length : 0;
  const homeworkCount = syllabus ? syllabus.lessons.filter((l) => l.homework).length : 0;
  const taughtCount = Math.max(0, Math.min(32, currentWeek - 1));
  const remainingCount = Math.max(0, 32 - currentWeek + 1);

  const toggleShare = async (enabled) => {
    setShareBusy(true);
    try {
      const r = await api.post(`/syllabus/${syllabus.id}/share`, { enabled });
      setSyllabus({ ...syllabus, share_enabled: r.data.share_enabled, share_token: r.data.share_token });
      if (enabled) {
        const url = `${window.location.origin}/share/${r.data.share_token}`;
        await navigator.clipboard.writeText(url).catch(() => {});
        toast.success(t("common.copied"));
      } else {
        toast.info(t("share.disabled"));
      }
    } catch (e) {
      toast.error("Failed to update sharing");
    } finally {
      setShareBusy(false);
    }
  };

  const copyShareLink = async () => {
    if (!syllabus?.share_token) return;
    const url = `${window.location.origin}/share/${syllabus.share_token}`;
    await navigator.clipboard.writeText(url).catch(() => {});
    toast.success(t("common.copied"));
  };

  const draftNewsletter = () => {
    if (!syllabus) return;
    const recipients = user?.family_emails || [];
    if (recipients.length === 0) {
      toast.error(t("news.no_recipients"));
      return;
    }
    // Next week's lesson (or current if last)
    const nextWeek = Math.min(32, currentWeek + (weekInfo.in_holiday ? 0 : 1));
    const lesson = syllabus.lessons.find((l) => l.week === nextWeek) || syllabus.lessons[0];
    const subject = t("news.subject", { n: lesson.week, title: lesson.title });
    const hwLine = lesson.homework
      ? t("news.body_homework_yes", { min: lesson.homework.estimated_minutes || 15 })
      : t("news.body_homework_no");
    const shareLine = syllabus.share_enabled && syllabus.share_token
      ? `${t("news.body_share")} ${window.location.origin}/share/${syllabus.share_token}`
      : "";
    const body = [
      t("news.body_hello"),
      "",
      t("news.body_intro"),
      "",
      `${t("news.body_theme")} ${lesson.title}`,
      `${t("news.body_grammar")} ${lesson.grammar}`,
      `${t("news.body_vocab")} ${lesson.vocabulary.slice(0, 8).join(", ")}`,
      `${t("news.body_homework")} ${hwLine}`,
      shareLine,
      "",
      t("news.body_close"),
      user?.full_name || "",
    ].filter(Boolean).join("\n");
    const mailto = `mailto:?bcc=${encodeURIComponent(recipients.join(","))}&subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
    window.location.href = mailto;
    toast.success(t("news.draft_opened"));
  };

  if (loading) return <Layout><div className="p-14 text-zinc-400 font-body">{t("common.loading")}</div></Layout>;

  if (!syllabus) {
    return (
      <Layout>
        <div className="p-14 max-w-3xl">
          <div className="text-xs uppercase tracking-widest text-lime mb-3">{t("dash.no_syllabus_kicker")}</div>
          <h1 className="font-display font-bold text-5xl tracking-tight">{t("dash.no_syllabus_title")}</h1>
          <p className="mt-4 text-zinc-400 max-w-lg">{t("dash.no_syllabus_desc")}</p>
          <Button data-testid="dash-generate-btn" onClick={regenerate} disabled={regenerating}
            className="mt-8 bg-lime text-black hover:bg-[#8BC926] rounded-full px-7 h-12 hover-lift font-semibold">
            {regenerating ? t("dash.regenerating") : t("dash.generate_btn")} <ArrowRight className="ml-2 h-4 w-4" />
          </Button>
        </div>
      </Layout>
    );
  }

  const greetKey = (() => {
    const h = new Date().getHours();
    if (h < 12) return "dash.greet_morning";
    if (h < 18) return "dash.greet_afternoon";
    return "dash.greet_evening";
  })();

  return (
    <Layout>
      <div className="p-8 lg:p-12">
        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-end md:justify-between gap-6 mb-10">
          <div>
            <div className="text-xs uppercase tracking-widest text-lime mb-2">{t("dash.kicker")}</div>
            <h1 className="font-display font-bold text-5xl tracking-tight">{t(greetKey)}, {user?.full_name?.split(" ")[0]}.</h1>
            <p className="mt-3 text-zinc-400 flex items-center gap-2">
              <Calendar className="h-4 w-4 text-lime" />
              {weekInfo.in_holiday ? (
                <span>{t("dash.on_holiday_a")} <span className="text-lime font-semibold">{weekInfo.holiday_name}</span>{t("dash.on_holiday_b")} <span className="text-white font-semibold">{t("dash.week")} {currentWeek}</span>.</span>
              ) : (
                <span>{t("dash.you_are_week")} <span className="text-white font-semibold">{t("dash.week")} {currentWeek}</span> {t("dash.of_school_year")}</span>
              )}
            </p>
          </div>
          <div className="flex flex-wrap gap-3">
            <Button data-testid="dash-current-week-btn" onClick={() => nav(`/week/${currentWeek}`)}
              className="bg-lime text-black hover:bg-[#8BC926] rounded-full px-5 h-11 hover-lift font-semibold">
              {t("dash.open_week")} <ArrowRight className="ml-2 h-4 w-4" />
            </Button>
            <Button data-testid="dash-export-syllabus-btn" onClick={exportAll} variant="ghost"
              className="border border-zinc-800 text-white hover:bg-zinc-900 rounded-full px-5 h-11">
              <FileDown className="mr-2 h-4 w-4" /> {t("dash.export_syllabus")}
            </Button>
            <Button data-testid="dash-regenerate-btn" onClick={regenerate} disabled={regenerating} variant="ghost"
              className="border border-zinc-800 text-white hover:bg-zinc-900 rounded-full px-5 h-11">
              <RefreshCw className={`mr-2 h-4 w-4 ${regenerating ? "animate-spin" : ""}`} />
              {regenerating ? t("dash.regenerating") : t("dash.regenerate")}
            </Button>
          </div>
        </div>

        {/* Progress analytics + Newsletter */}
        <div className="grid md:grid-cols-3 gap-5 mb-6">
          <div data-testid="stats-card" className="md:col-span-2 bg-white text-black border border-zinc-200 p-6">
            <div className="flex items-center gap-2 mb-4">
              <BarChart3 className="h-5 w-5" />
              <div className="text-xs uppercase tracking-widest text-zinc-500">{t("stats.kicker")}</div>
            </div>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
              <div>
                <div className="font-display font-bold text-4xl leading-none tracking-tight" data-testid="stats-taught">{taughtCount}</div>
                <div className="mt-2 text-xs uppercase tracking-widest text-zinc-500">{t("stats.taught")}</div>
              </div>
              <div>
                <div className="font-display font-bold text-4xl leading-none tracking-tight text-lime" data-testid="stats-packed">{packedCount}</div>
                <div className="mt-2 text-xs uppercase tracking-widest text-zinc-500">{t("stats.packed")}</div>
              </div>
              <div>
                <div className="font-display font-bold text-4xl leading-none tracking-tight" data-testid="stats-homework">{homeworkCount}</div>
                <div className="mt-2 text-xs uppercase tracking-widest text-zinc-500">{t("stats.homework")}</div>
              </div>
              <div>
                <div className="font-display font-bold text-4xl leading-none tracking-tight" data-testid="stats-remaining">{remainingCount}</div>
                <div className="mt-2 text-xs uppercase tracking-widest text-zinc-500">{t("stats.streak")}</div>
              </div>
            </div>
          </div>

          <div data-testid="newsletter-card" className="bg-black text-white border-2 border-lime p-6 flex flex-col">
            <div className="flex items-center gap-2 mb-2">
              <Mail className="h-5 w-5 text-lime" />
              <div className="text-xs uppercase tracking-widest text-lime">{t("news.card_kicker")}</div>
            </div>
            <h3 className="font-display font-bold text-xl tracking-tight mt-2">{t("news.card_title")}</h3>
            <p className="mt-2 text-sm text-zinc-400 flex-1">
              {t("news.card_desc", { n: Math.min(32, currentWeek + (weekInfo.in_holiday ? 0 : 1)) })}
            </p>
            <Button data-testid="newsletter-draft-btn" onClick={draftNewsletter}
              className="mt-4 bg-lime text-black hover:bg-[#8BC926] rounded-none h-11 font-semibold self-start px-5">
              <Send className="h-4 w-4 mr-2" /> {t("news.card_btn")}
            </Button>
          </div>
        </div>

        {/* Batch pack generation + Holidays + Sharing */}
        <div className="grid md:grid-cols-3 gap-5 mb-10">
          <div data-testid="batch-pack-card" className="bg-white text-black border-2 border-lime p-6">
            <div className="flex items-center gap-2 mb-2">
              <Package className="h-5 w-5" />
              <div className="text-xs uppercase tracking-widest text-black">{t("dash.batch_kicker")}</div>
            </div>
            <h3 className="font-display font-bold text-xl tracking-tight">
              {packedCount} / 32 · {t("dash.batch_progress")}
            </h3>
            <div className="mt-4 h-2 bg-zinc-100 relative">
              <div className="absolute inset-y-0 left-0 bg-lime" style={{ width: `${(packedCount / 32) * 100}%` }} />
            </div>
            {batch.status === "running" ? (
              <div data-testid="batch-progress" className="mt-4 text-sm text-zinc-700">
                <div className="flex items-center gap-2">
                  <Sparkles className="h-4 w-4 text-lime animate-pulse" />
                  {t("dash.batch_working")} {batch.current_week || "—"} · {batch.done}/{batch.total} {t("dash.batch_done")}
                </div>
                <div className="text-xs text-zinc-500 mt-1">{t("dash.batch_hint")}</div>
              </div>
            ) : (
              <Button data-testid="batch-start-btn" onClick={startBatch} disabled={packedCount === 32}
                className="mt-5 bg-black text-white hover:bg-zinc-900 rounded-full px-5 h-10">
                <Sparkles className="h-4 w-4 mr-2 text-lime" />
                {packedCount === 32 ? t("dash.batch_all_ready") : `${t("dash.batch_generate")} (${32 - packedCount})`}
              </Button>
            )}
          </div>

          <div data-testid="holidays-card" className="bg-white text-black border border-zinc-200 p-6">
            <div className="flex items-center gap-2 mb-2">
              <Calendar className="h-5 w-5" />
              <div className="text-xs uppercase tracking-widest text-zinc-500">{t("dash.holidays_kicker")}</div>
            </div>
            <h3 className="font-display font-bold text-xl tracking-tight">
              {t("dash.holidays_zone")} {user?.holiday_zone && user.holiday_zone !== "none" ? user.holiday_zone : t("dash.holidays_none")}
            </h3>
            {weekInfo.holidays && weekInfo.holidays.length ? (
              <ul className="mt-3 space-y-1 text-sm text-zinc-700">
                {weekInfo.holidays.map((h) => (
                  <li key={h.name} className="flex justify-between border-b border-zinc-100 py-1">
                    <span className="font-medium">{h.name}</span>
                    <span className="text-xs text-zinc-500">{h.start} → {h.end}</span>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="mt-3 text-sm text-zinc-600">{t("dash.holidays_hint")}</p>
            )}
          </div>

          <div data-testid="share-card" className="bg-white text-black border border-zinc-200 p-6">
            <div className="flex items-center gap-2 mb-2">
              <Share2 className="h-5 w-5" />
              <div className="text-xs uppercase tracking-widest text-zinc-500">{t("dash.share_btn")}</div>
            </div>
            <h3 className="font-display font-bold text-xl tracking-tight">
              {syllabus.share_enabled ? t("share.on_title") : t("share.off_title")}
            </h3>
            <p className="mt-2 text-sm text-zinc-600">{t("share.card_desc")}</p>
            <div className="mt-4 flex items-center justify-between">
              <span className="text-xs uppercase tracking-widest text-zinc-500">{t("share.enable_link")}</span>
              <Switch data-testid="share-toggle" checked={!!syllabus.share_enabled} disabled={shareBusy}
                onCheckedChange={toggleShare}
                className="data-[state=checked]:bg-black data-[state=unchecked]:bg-zinc-300 border border-zinc-400" />
            </div>
            {syllabus.share_enabled && syllabus.share_token && (
              <Button data-testid="share-copy-btn" onClick={copyShareLink} variant="ghost"
                className="mt-4 w-full border border-zinc-300 rounded-none justify-start text-xs uppercase tracking-widest text-black hover:bg-zinc-100">
                <LinkIcon className="h-4 w-4 mr-2" /> {t("share.copy_link")}
              </Button>
            )}
          </div>
        </div>

        {/* Grid of 32 weeks */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5">
          {syllabus.lessons.map((l) => {
            const isCurrent = l.week === currentWeek;
            const isPast = l.week < currentWeek;
            return (
              <button
                key={l.week}
                data-week={l.week}
                data-testid={`week-card-${l.week}`}
                onClick={() => nav(`/week/${l.week}`)}
                className={`text-left group relative bg-white text-black border p-6 hover-lift transition-colors ${isCurrent ? "border-lime border-2" : "border-zinc-200"}`}
              >
                {isCurrent && (
                  <div className="absolute -top-3 left-5 bg-lime text-black text-[10px] uppercase tracking-widest px-2 py-1 font-bold">
                    Current week
                  </div>
                )}
                <div className="flex items-baseline justify-between">
                  <div className="text-xs uppercase tracking-widest text-zinc-500">Week {l.week}</div>
                  <div className="flex items-center gap-2">
                    {l.pack && (
                      <span data-testid={`week-pack-badge-${l.week}`} className="text-[9px] uppercase tracking-widest bg-lime text-black px-1.5 py-0.5 font-bold">Pack</span>
                    )}
                    <div className={`text-[10px] uppercase tracking-widest ${isPast ? "text-zinc-400" : "text-lime"}`}>
                      {isPast ? "Past" : l.cefr_level}
                    </div>
                  </div>
                </div>
                <h3 className="font-display font-bold text-xl tracking-tight mt-3 min-h-[56px] leading-tight">{l.title}</h3>
                <div className="mt-5 space-y-2">
                  <div className="text-[11px] uppercase tracking-widest text-zinc-500">Grammar</div>
                  <div className="text-sm text-black line-clamp-2">{l.grammar}</div>
                </div>
                <div className="mt-4 flex flex-wrap gap-1.5">
                  {l.vocabulary.slice(0, 4).map((v) => (
                    <span key={v} className="text-[10px] uppercase tracking-widest px-2 py-1 bg-zinc-100 text-zinc-700">{v}</span>
                  ))}
                </div>
              </button>
            );
          })}
        </div>
      </div>
    </Layout>
  );
}
