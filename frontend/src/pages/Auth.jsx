import { useState } from "react";
import { useNavigate, useSearchParams, Link } from "react-router-dom";
import { useAuth } from "@/lib/auth";
import { getErrorMessage } from "@/lib/api";
import { useI18n } from "@/lib/i18n";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { toast } from "sonner";
import LangToggle from "@/components/LangToggle";
import { ArrowRight, ArrowLeft } from "lucide-react";

export default function Auth() {
  const [params] = useSearchParams();
  const [mode, setMode] = useState(params.get("mode") === "login" ? "login" : "signup");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");
  const [busy, setBusy] = useState(false);
  const { login, signup } = useAuth();
  const { t } = useI18n();
  const nav = useNavigate();

  const submit = async (e) => {
    e.preventDefault();
    setBusy(true);
    try {
      let user;
      if (mode === "signup") user = await signup(email, password, name);
      else user = await login(email, password);
      toast.success(mode === "signup" ? t("auth.welcome") : t("auth.welcome_back"));
      nav(user.onboarded ? "/dashboard" : "/onboarding");
    } catch (err) {
      toast.error(getErrorMessage(err));
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="min-h-screen bg-black text-white font-body grid lg:grid-cols-2">
      <div className="hidden lg:flex relative grain overflow-hidden border-r border-zinc-900">
        <div className="relative z-10 p-14 flex flex-col justify-between w-full">
          <Link to="/" className="flex items-center gap-3 group" data-testid="auth-back-home">
            <ArrowLeft className="h-4 w-4 text-zinc-500 group-hover:text-lime transition-colors" />
            <span className="text-sm text-zinc-500 group-hover:text-white transition-colors uppercase tracking-widest">{t("nav.back_home")}</span>
          </Link>
          <div>
            <img src="/teachkit-logo.webp" alt="" className="h-24 w-24 mb-8" />
            <h2 className="font-display font-bold text-5xl leading-tight tracking-tight">
              {t("auth.side_a")}<br /> {t("auth.side_b")}<br /><span className="text-lime">{t("auth.side_c")}</span>
            </h2>
            <p className="mt-6 text-zinc-400 max-w-md">{t("auth.side_sub")}</p>
          </div>
          <div className="text-xs uppercase tracking-widest text-zinc-600">{t("auth.side_footer")}</div>
        </div>
      </div>

      <div className="flex items-center justify-center p-8 bg-black">
        <div className="w-full max-w-md">
          <div className="flex items-center justify-between mb-6">
            <div className="lg:hidden flex items-center gap-3">
              <img src="/teachkit-logo.webp" alt="" className="h-10 w-10" />
              <span className="font-display font-bold text-lg"><span className="text-lime">[THE]</span> TEACHKIT</span>
            </div>
            <div className="ml-auto"><LangToggle variant="dark" /></div>
          </div>
          <div className="text-xs uppercase tracking-widest text-lime mb-3">{mode === "signup" ? t("auth.signup_kicker") : t("auth.login_kicker")}</div>
          <h1 className="font-display font-bold text-4xl tracking-tight">
            {mode === "signup" ? t("auth.signup_title") : t("auth.login_title")}
          </h1>

          <form onSubmit={submit} className="mt-10 space-y-5">
            {mode === "signup" && (
              <div>
                <Label htmlFor="name" className="text-xs uppercase tracking-widest text-zinc-400">{t("auth.name")}</Label>
                <Input id="name" data-testid="auth-name-input" value={name} onChange={(e) => setName(e.target.value)} required
                  className="mt-2 bg-zinc-950 border-zinc-800 text-white rounded-none h-12 focus:ring-2 focus:ring-[#A6E22E]" />
              </div>
            )}
            <div>
              <Label htmlFor="email" className="text-xs uppercase tracking-widest text-zinc-400">{t("auth.email")}</Label>
              <Input id="email" type="email" data-testid="auth-email-input" value={email} onChange={(e) => setEmail(e.target.value)} required
                className="mt-2 bg-zinc-950 border-zinc-800 text-white rounded-none h-12 focus:ring-2 focus:ring-[#A6E22E]" />
            </div>
            <div>
              <Label htmlFor="password" className="text-xs uppercase tracking-widest text-zinc-400">{t("auth.password")}</Label>
              <Input id="password" type="password" data-testid="auth-password-input" value={password} onChange={(e) => setPassword(e.target.value)} required minLength={6}
                className="mt-2 bg-zinc-950 border-zinc-800 text-white rounded-none h-12 focus:ring-2 focus:ring-[#A6E22E]" />
            </div>
            <Button type="submit" data-testid="auth-submit-btn" disabled={busy}
              className="w-full bg-lime text-black hover:bg-[#8BC926] rounded-none h-12 font-semibold text-base hover-lift">
              {busy ? t("common.loading") : mode === "signup" ? t("auth.create_account") : t("auth.login")}
              <ArrowRight className="ml-2 h-4 w-4" />
            </Button>
          </form>

          <div className="mt-6 text-sm text-zinc-400">
            {mode === "signup" ? (
              <>{t("auth.have_account")} <button data-testid="auth-switch-login" onClick={() => setMode("login")} className="text-lime hover:underline">{t("auth.login")}</button></>
            ) : (
              <>{t("auth.new_here")} <button data-testid="auth-switch-signup" onClick={() => setMode("signup")} className="text-lime hover:underline">{t("auth.create_account")}</button></>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
