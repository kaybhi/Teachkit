import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import axios from "axios";
import { useI18n } from "@/lib/i18n";
import LangToggle from "@/components/LangToggle";
import { ArrowLeft, Sparkles, Users, School } from "lucide-react";

export default function Gallery() {
  const { t } = useI18n();
  const [items, setItems] = useState(null);

  useEffect(() => {
    const url = `${process.env.REACT_APP_BACKEND_URL}/api/public/gallery`;
    axios.get(url).then((r) => setItems(r.data)).catch(() => setItems([]));
  }, []);

  return (
    <div className="min-h-screen bg-black text-white font-body">
      <header className="border-b border-zinc-900 sticky top-0 bg-black/80 backdrop-blur-xl z-10">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <Link to="/" className="flex items-center gap-3" data-testid="gallery-home-link">
            <img src="/teachkit-logo.webp" alt="" className="h-10 w-10" />
            <div className="leading-tight">
              <div className="font-display font-bold"><span className="text-lime">[THE]</span> TEACHKIT</div>
              <div className="text-[10px] uppercase tracking-widest text-zinc-500">{t("gallery.subtitle")}</div>
            </div>
          </Link>
          <div className="flex items-center gap-3">
            <LangToggle variant="dark" />
            <Link to="/" data-testid="gallery-back-link" className="text-sm text-zinc-400 hover:text-white uppercase tracking-widest inline-flex items-center gap-2">
              <ArrowLeft className="h-4 w-4" /> {t("nav.back_home")}
            </Link>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-6 py-16">
        <div className="text-xs uppercase tracking-widest text-lime mb-3 flex items-center gap-2">
          <Sparkles className="h-3.5 w-3.5" /> {t("gallery.kicker")}
        </div>
        <h1 className="font-display font-bold text-4xl sm:text-6xl tracking-tight max-w-3xl">{t("gallery.title")}</h1>
        <p className="mt-4 text-zinc-400 max-w-xl">{t("gallery.desc")}</p>

        <div className="mt-14">
          {items === null && <div className="text-zinc-400">{t("common.loading")}</div>}
          {items && items.length === 0 && (
            <div data-testid="gallery-empty" className="bg-white text-black p-10 border border-zinc-200 max-w-xl">
              <h2 className="font-display font-bold text-2xl tracking-tight">{t("gallery.empty_title")}</h2>
              <p className="mt-3 text-sm text-zinc-600">{t("gallery.empty_desc")}</p>
            </div>
          )}
          {items && items.length > 0 && (
            <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
              {items.map((it) => (
                <Link key={it.share_token} data-testid={`gallery-item-${it.share_token}`}
                  to={`/share/${it.share_token}`}
                  className="group relative bg-white text-black border border-zinc-200 p-7 hover-lift block">
                  <div className="flex items-center justify-between">
                    <span className="text-[10px] uppercase tracking-widest bg-lime text-black px-2 py-1 font-bold">{it.class_level}</span>
                    <span className="text-[10px] uppercase tracking-widest text-zinc-500">{it.lesson_count} weeks</span>
                  </div>
                  <h3 className="font-display font-bold text-xl mt-6 tracking-tight leading-tight min-h-[52px]">
                    {it.teacher?.school_name || t("gallery.card_default_title")}
                  </h3>
                  <div className="mt-5 space-y-1.5 text-sm text-zinc-700">
                    <div className="flex items-center gap-2">
                      <Users className="h-3.5 w-3.5 text-zinc-500" />
                      <span>{it.teacher?.full_name || t("gallery.card_default_title")}</span>
                    </div>
                    {it.teacher?.school_city ? (
                      <div className="flex items-center gap-2">
                        <School className="h-3.5 w-3.5 text-zinc-500" />
                        <span>{it.teacher.school_city}</span>
                      </div>
                    ) : (
                      <div className="text-xs text-zinc-400">{t("gallery.subtitle")}</div>
                    )}
                  </div>
                  <div className="mt-6 text-xs uppercase tracking-widest text-lime opacity-0 group-hover:opacity-100 transition-opacity">
                    {t("gallery.view")} →
                  </div>
                </Link>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
