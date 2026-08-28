import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";
import { getErrorMessage } from "@/lib/api";
import { useI18n } from "@/lib/i18n";
import LangToggle from "@/components/LangToggle";
import { Badge } from "@/components/ui/badge";

export default function SharedSyllabus() {
  const { token } = useParams();
  const { t } = useI18n();
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [selected, setSelected] = useState(null);

  useEffect(() => {
    const url = `${process.env.REACT_APP_BACKEND_URL}/api/public/syllabus/${token}`;
    axios.get(url).then((r) => setData(r.data)).catch((e) => setError(getErrorMessage(e, "Not found")));
  }, [token]);

  if (error) return <div className="min-h-screen bg-black text-white font-body flex items-center justify-center p-8"><div className="text-center"><div className="text-lime uppercase tracking-widest text-xs mb-3">404</div><div className="font-display text-3xl">{error}</div></div></div>;
  if (!data) return <div className="min-h-screen bg-black text-white font-body flex items-center justify-center">{t("common.loading")}</div>;

  const teacher = data.shared_by || {};

  return (
    <div className="min-h-screen bg-black text-white font-body">
      <header className="border-b border-zinc-900 sticky top-0 bg-black/80 backdrop-blur-xl z-10">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <img src="/teachkit-logo.webp" alt="" className="h-10 w-10" />
            <div className="leading-tight">
              <div className="font-display font-bold"><span className="text-lime">[THE]</span> TEACHKIT</div>
              <div className="text-[10px] uppercase tracking-widest text-zinc-500">{t("share.readonly")}</div>
            </div>
          </div>
          <LangToggle />
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-6 py-12">
        <div className="text-xs uppercase tracking-widest text-lime mb-3">{t("share.title")}</div>
        <h1 className="font-display font-bold text-4xl sm:text-5xl tracking-tight" data-testid="share-title">
          {teacher.school_name || teacher.full_name || "English syllabus"}
        </h1>
        <p className="mt-3 text-zinc-400">
          {t("share.by")} <span className="text-white">{teacher.full_name}</span>
          {teacher.school_city ? ` · ${teacher.school_city}` : ""}
          {data.class_level ? ` · ${data.class_level}` : ""}
        </p>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5 mt-10">
          {data.lessons.map((l) => (
            <button key={l.week} data-testid={`share-week-${l.week}`} onClick={() => setSelected(l)}
              className="text-left bg-white text-black border border-zinc-200 p-6 hover-lift">
              <div className="flex items-baseline justify-between">
                <div className="text-xs uppercase tracking-widest text-zinc-500">Week {l.week}</div>
                <div className="text-[10px] uppercase tracking-widest text-lime">{l.cefr_level}</div>
              </div>
              <h3 className="font-display font-bold text-xl tracking-tight mt-3 min-h-[56px] leading-tight">{l.title}</h3>
              <div className="mt-5 space-y-2">
                <div className="text-[11px] uppercase tracking-widest text-zinc-500">Grammar</div>
                <div className="text-sm text-black line-clamp-2">{l.grammar}</div>
              </div>
            </button>
          ))}
        </div>

        {selected && (
          <div data-testid="share-modal" className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-6" onClick={() => setSelected(null)}>
            <div className="bg-white text-black max-w-3xl w-full max-h-[90vh] overflow-y-auto p-8" onClick={(e) => e.stopPropagation()}>
              <div className="text-xs uppercase tracking-widest text-zinc-500">Week {selected.week} · CEFR {selected.cefr_level}</div>
              <h2 className="font-display font-bold text-3xl tracking-tight mt-2">{selected.title}</h2>
              <div className="mt-6 space-y-4">
                <div><div className="text-xs uppercase tracking-widest text-zinc-500 mb-1">Grammar</div><div>{selected.grammar}</div></div>
                <div><div className="text-xs uppercase tracking-widest text-zinc-500 mb-1">Vocabulary</div><div className="flex flex-wrap gap-1.5">{selected.vocabulary.map((v) => <Badge key={v} variant="secondary" className="rounded-none bg-zinc-100">{v}</Badge>)}</div></div>
                <div><div className="text-xs uppercase tracking-widest text-zinc-500 mb-1">Objectives</div><ol className="list-decimal list-inside text-sm space-y-1">{selected.objectives.map((o, i) => <li key={i}>{o}</li>)}</ol></div>
                <div><div className="text-xs uppercase tracking-widest text-zinc-500 mb-1">Materials</div><ul className="text-sm space-y-1">{selected.materials.map((m, i) => <li key={i} className="flex gap-2"><span className="text-lime">▪</span>{m}</li>)}</ul></div>
              </div>
              <button className="mt-6 text-xs uppercase tracking-widest text-zinc-500 hover:text-black" onClick={() => setSelected(null)}>× Close</button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
