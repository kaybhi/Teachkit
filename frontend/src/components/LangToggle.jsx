import { useI18n } from "@/lib/i18n";
import { Button } from "@/components/ui/button";

export default function LangToggle({ variant = "dark" }) {
  const { lang, setLang } = useI18n();
  const other = lang === "en" ? "fr" : "en";
  const isDark = variant === "dark";
  return (
    <Button
      data-testid="lang-toggle"
      onClick={() => setLang(other)}
      variant="ghost"
      className={`rounded-full px-3 h-9 text-xs uppercase tracking-widest border ${
        isDark
          ? "border-zinc-800 text-white hover:bg-zinc-900"
          : "border-zinc-300 text-black hover:bg-zinc-100"
      }`}
    >
      {lang === "en" ? "🇬🇧 EN" : "🇫🇷 FR"} · {other.toUpperCase()}
    </Button>
  );
}
