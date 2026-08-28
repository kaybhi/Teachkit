import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api, { getErrorMessage } from "@/lib/api";
import { useAuth } from "@/lib/auth";
import { useI18n } from "@/lib/i18n";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Checkbox } from "@/components/ui/checkbox";
import { toast } from "sonner";
import LangToggle from "@/components/LangToggle";
import { GripVertical, ArrowRight } from "lucide-react";
import { CLASS_TYPES, levelsForClassType, defaultLevelId } from "@/constants/classTypes";

const SKILLS = ["Speaking", "Listening", "Reading", "Writing"];
const ACTIVITIES = ["Games", "Pair work", "Group work", "Songs", "Role-play", "Video", "Digital", "Storytelling", "Whole class", "Individual"];

export default function Onboarding() {
  const { user, refresh } = useAuth();
  const { t } = useI18n();
  const nav = useNavigate();
  const [step, setStep] = useState(1);
  const [busy, setBusy] = useState(false);
  const [form, setForm] = useState({
    school_name: user?.school_name || "",
    school_city: user?.school_city || "",
    class_type: user?.class_type || "school",
    level_id: user?.level_id || "cm2",
    school_year_start: user?.school_year_start || `${new Date().getFullYear() - (new Date().getMonth() < 7 ? 1 : 0)}-09-01`,
    priorities: user?.priorities?.length ? user.priorities : SKILLS,
    activity_types: user?.activity_types?.length ? user.activity_types : ["Games", "Pair work", "Group work", "Songs", "Role-play"],
  });

  const setClassType = (classType) => {
    setForm({ ...form, class_type: classType, level_id: defaultLevelId(classType) });
  };

  const movePriority = (idx, dir) => {
    const next = [...form.priorities];
    const swap = idx + dir;
    if (swap < 0 || swap >= next.length) return;
    [next[idx], next[swap]] = [next[swap], next[idx]];
    setForm({ ...form, priorities: next });
  };

  const toggleActivity = (a) => {
    const has = form.activity_types.includes(a);
    setForm({ ...form, activity_types: has ? form.activity_types.filter((x) => x !== a) : [...form.activity_types, a] });
  };

  const finish = async () => {
    setBusy(true);
    try {
      await api.put("/profile", form);
      await api.post("/syllabus/generate", {
        class_type: form.class_type,
        level_id: form.level_id,
        priorities: form.priorities,
        activity_types: form.activity_types,
      });
      await refresh();
      toast.success("Your syllabus is ready!");
      nav("/dashboard");
    } catch (e) {
      toast.error(getErrorMessage(e));
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="min-h-screen bg-black text-white font-body">
      <div className="max-w-3xl mx-auto px-6 py-14">
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center gap-3">
            <img src="/teachkit-logo.webp" alt="" className="h-10 w-10" />
            <span className="font-display font-bold text-lg"><span className="text-lime">[THE]</span> TEACHKIT</span>
          </div>
          <LangToggle variant="dark" />
        </div>

        <div className="flex items-center gap-2 mb-10">
          {[1, 2, 3].map((s) => (
            <div key={s} className={`h-1 flex-1 ${s <= step ? "bg-lime" : "bg-zinc-800"}`} />
          ))}
        </div>

        {step === 1 && (
          <div className="animate-slide-up">
            <div className="text-xs uppercase tracking-widest text-lime mb-3">{t("onb.step_of", { n: 1 })}</div>
            <h1 className="font-display font-bold text-4xl tracking-tight">{t("onb.step1_title")}</h1>
            <p className="mt-3 text-zinc-400">{t("onb.step1_desc")}</p>
            <div className="mt-10 grid sm:grid-cols-2 gap-5">
              <div>
                <Label className="text-xs uppercase tracking-widest text-zinc-400">{t("profile.school_name")}</Label>
                <Input data-testid="onb-school-name" value={form.school_name} onChange={(e) => setForm({ ...form, school_name: e.target.value })}
                  className="mt-2 bg-zinc-950 border-zinc-800 rounded-none h-12" placeholder="Collège Jean Moulin" />
              </div>
              <div>
                <Label className="text-xs uppercase tracking-widest text-zinc-400">{t("profile.city")}</Label>
                <Input data-testid="onb-school-city" value={form.school_city} onChange={(e) => setForm({ ...form, school_city: e.target.value })}
                  className="mt-2 bg-zinc-950 border-zinc-800 rounded-none h-12" placeholder="Lyon" />
              </div>
              <div>
                <Label className="text-xs uppercase tracking-widest text-zinc-400">{t("profile.class_type")}</Label>
                <Select value={form.class_type} onValueChange={setClassType}>
                  <SelectTrigger data-testid="onb-class-type" className="mt-2 bg-zinc-950 border-zinc-800 rounded-none h-12"><SelectValue /></SelectTrigger>
                  <SelectContent className="bg-zinc-950 border-zinc-800 text-white">
                    {CLASS_TYPES.map((c) => (
                      <SelectItem key={c.key} value={c.key}>{c.label}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              <div>
                <Label className="text-xs uppercase tracking-widest text-zinc-400">{t("profile.class_level")}</Label>
                <Select value={form.level_id} onValueChange={(v) => setForm({ ...form, level_id: v })}>
                  <SelectTrigger data-testid="onb-class-level" className="mt-2 bg-zinc-950 border-zinc-800 rounded-none h-12"><SelectValue /></SelectTrigger>
                  <SelectContent className="bg-zinc-950 border-zinc-800 text-white">
                    {levelsForClassType(form.class_type).map((lv) => (
                      <SelectItem key={lv.id} value={lv.id}>{lv.label} · {lv.cefr}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              <div>
                <Label className="text-xs uppercase tracking-widest text-zinc-400">{t("profile.year_start")}</Label>
                <Input type="date" data-testid="onb-year-start" value={form.school_year_start} onChange={(e) => setForm({ ...form, school_year_start: e.target.value })}
                  className="mt-2 bg-zinc-950 border-zinc-800 rounded-none h-12" />
              </div>
            </div>
            <div className="mt-10 flex justify-end">
              <Button data-testid="onb-next-1" onClick={() => setStep(2)} className="bg-lime text-black hover:bg-[#8BC926] rounded-full px-6 h-11 hover-lift">
                {t("common.continue")} <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
            </div>
          </div>
        )}

        {step === 2 && (
          <div className="animate-slide-up">
            <div className="text-xs uppercase tracking-widest text-lime mb-3">{t("onb.step_of", { n: 2 })}</div>
            <h1 className="font-display font-bold text-4xl tracking-tight">{t("onb.step2_title")}</h1>
            <p className="mt-3 text-zinc-400">{t("onb.step2_desc")}</p>
            <div className="mt-10 space-y-2">
              {form.priorities.map((p, i) => (
                <div key={p} data-testid={`onb-priority-${p}`} className="bg-white text-black px-5 py-4 flex items-center justify-between border border-zinc-200">
                  <div className="flex items-center gap-4">
                    <GripVertical className="h-4 w-4 text-zinc-400" />
                    <span className="text-lime font-display font-bold w-8">#{i + 1}</span>
                    <span className="font-medium">{p}</span>
                  </div>
                  <div className="flex gap-2">
                    <Button data-testid={`onb-priority-up-${p}`} variant="ghost" size="sm" onClick={() => movePriority(i, -1)} disabled={i === 0} className="rounded-none">↑</Button>
                    <Button data-testid={`onb-priority-down-${p}`} variant="ghost" size="sm" onClick={() => movePriority(i, 1)} disabled={i === form.priorities.length - 1} className="rounded-none">↓</Button>
                  </div>
                </div>
              ))}
            </div>
            <div className="mt-10 flex justify-between">
              <Button variant="ghost" onClick={() => setStep(1)} className="rounded-full text-zinc-400 hover:text-white hover:bg-zinc-900">{t("common.back")}</Button>
              <Button data-testid="onb-next-2" onClick={() => setStep(3)} className="bg-lime text-black hover:bg-[#8BC926] rounded-full px-6 h-11 hover-lift">
                {t("common.continue")} <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
            </div>
          </div>
        )}

        {step === 3 && (
          <div className="animate-slide-up">
            <div className="text-xs uppercase tracking-widest text-lime mb-3">{t("onb.step_of", { n: 3 })}</div>
            <h1 className="font-display font-bold text-4xl tracking-tight">{t("onb.step3_title")}</h1>
            <p className="mt-3 text-zinc-400">{t("onb.step3_desc")}</p>
            <div className="mt-10 grid sm:grid-cols-2 gap-3">
              {ACTIVITIES.map((a) => {
                const on = form.activity_types.includes(a);
                return (
                  <div key={a} data-testid={`onb-activity-${a}`} role="button" tabIndex={0}
                    onClick={() => toggleActivity(a)}
                    onKeyDown={(e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); toggleActivity(a); } }}
                    className={`p-4 border text-left flex items-center gap-3 transition-colors cursor-pointer ${on ? "border-lime bg-zinc-950" : "border-zinc-800 hover:border-zinc-600"}`}>
                    <Checkbox checked={on} className="pointer-events-none data-[state=checked]:bg-lime data-[state=checked]:border-lime" />
                    <span className={on ? "text-white" : "text-zinc-300"}>{a}</span>
                  </div>
                );
              })}
            </div>
            <div className="mt-10 flex justify-between">
              <Button variant="ghost" onClick={() => setStep(2)} className="rounded-full text-zinc-400 hover:text-white hover:bg-zinc-900">{t("common.back")}</Button>
              <Button data-testid="onb-finish-btn" onClick={finish} disabled={busy}
                className="bg-lime text-black hover:bg-[#8BC926] rounded-full px-6 h-11 hover-lift font-semibold">
                {busy ? t("onb.finish_busy") : t("onb.finish")} <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
