import { useState } from "react";
import Layout from "@/components/Layout";
import api from "@/lib/api";
import { useAuth } from "@/lib/auth";
import { useI18n } from "@/lib/i18n";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Checkbox } from "@/components/ui/checkbox";
import { toast } from "sonner";
import { CLASS_TYPES, levelsForClassType, defaultLevelId } from "@/constants/classTypes";

const ACTIVITIES = ["Games", "Pair work", "Group work", "Songs", "Role-play", "Video", "Digital", "Storytelling", "Whole class", "Individual"];
const SKILLS = ["Speaking", "Listening", "Reading", "Writing"];

export default function Profile() {
  const { user, refresh } = useAuth();
  const { t } = useI18n();
  const [form, setForm] = useState({
    full_name: user?.full_name || "",
    school_name: user?.school_name || "",
    school_city: user?.school_city || "",
    class_type: user?.class_type || "school",
    level_id: user?.level_id || "cm2",
    student_count: user?.student_count || 4,
    duration: user?.duration || 60,
    school_year_start: user?.school_year_start || "",
    priorities: user?.priorities?.length ? user.priorities : SKILLS,
    activity_types: user?.activity_types?.length ? user.activity_types : [],
    holiday_zone: user?.holiday_zone || "none",
    family_emails: (user?.family_emails || []).join("\n"),
  });
  const [saving, setSaving] = useState(false);

  const setClassType = (classType) => {
    setForm({ ...form, class_type: classType, level_id: defaultLevelId(classType) });
  };

  const move = (idx, dir) => {
    const next = [...form.priorities];
    const swap = idx + dir;
    if (swap < 0 || swap >= next.length) return;
    [next[idx], next[swap]] = [next[swap], next[idx]];
    setForm({ ...form, priorities: next });
  };

  const toggle = (a) => {
    const has = form.activity_types.includes(a);
    setForm({ ...form, activity_types: has ? form.activity_types.filter((x) => x !== a) : [...form.activity_types, a] });
  };

  const save = async () => {
    setSaving(true);
    try {
      const payload = {
        ...form,
        family_emails: form.family_emails.split("\n").map((s) => s.trim()).filter((s) => s.includes("@")),
      };
      await api.put("/profile", payload);
      await refresh();
      toast.success("Profile updated");
    } catch (e) {
      toast.error("Failed to save");
    } finally {
      setSaving(false);
    }
  };

  return (
    <Layout>
      <div className="p-8 lg:p-12 max-w-4xl">
        <div className="text-xs uppercase tracking-widest text-lime mb-2">Your account</div>
        <h1 className="font-display font-bold text-5xl tracking-tight">Profile & preferences</h1>

        {/* Teacher */}
        <div className="mt-10 bg-white text-black border border-zinc-200 p-8">
          <div className="text-xs uppercase tracking-widest text-zinc-500 mb-6">Teacher & school</div>
          <div className="grid sm:grid-cols-2 gap-5">
            <div>
              <Label className="text-xs uppercase tracking-widest text-zinc-500">Full name</Label>
              <Input data-testid="profile-name-input" value={form.full_name} onChange={(e) => setForm({ ...form, full_name: e.target.value })}
                className="mt-2 bg-transparent border-zinc-300 rounded-none" />
            </div>
            <div>
              <Label className="text-xs uppercase tracking-widest text-zinc-500">Email</Label>
              <Input value={user?.email} disabled className="mt-2 bg-zinc-100 border-zinc-300 rounded-none" />
            </div>
            <div>
              <Label className="text-xs uppercase tracking-widest text-zinc-500">School name</Label>
              <Input data-testid="profile-school-input" value={form.school_name} onChange={(e) => setForm({ ...form, school_name: e.target.value })}
                className="mt-2 bg-transparent border-zinc-300 rounded-none" />
            </div>
            <div>
              <Label className="text-xs uppercase tracking-widest text-zinc-500">City</Label>
              <Input data-testid="profile-city-input" value={form.school_city} onChange={(e) => setForm({ ...form, school_city: e.target.value })}
                className="mt-2 bg-transparent border-zinc-300 rounded-none" />
            </div>
            <div>
              <Label className="text-xs uppercase tracking-widest text-zinc-500">{t("profile.class_type")}</Label>
              <Select value={form.class_type} onValueChange={setClassType}>
                <SelectTrigger data-testid="profile-class-type-select" className="mt-2 bg-transparent border-zinc-300 rounded-none"><SelectValue /></SelectTrigger>
                <SelectContent>
                  {CLASS_TYPES.map((c) => (
                    <SelectItem key={c.key} value={c.key}>{c.label}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div>
              <Label className="text-xs uppercase tracking-widest text-zinc-500">{t("profile.class_level")}</Label>
              <Select value={form.level_id} onValueChange={(v) => setForm({ ...form, level_id: v })}>
                <SelectTrigger data-testid="profile-class-select" className="mt-2 bg-transparent border-zinc-300 rounded-none"><SelectValue /></SelectTrigger>
                <SelectContent>
                  {levelsForClassType(form.class_type).map((lv) => (
                    <SelectItem key={lv.id} value={lv.id}>{lv.label} · {lv.cefr}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div>
              <Label className="text-xs uppercase tracking-widest text-zinc-500">School year start</Label>
              <Input type="date" data-testid="profile-year-input" value={form.school_year_start} onChange={(e) => setForm({ ...form, school_year_start: e.target.value })}
                className="mt-2 bg-transparent border-zinc-300 rounded-none" />
            </div>
            <div>
              <Label className="text-xs uppercase tracking-widest text-zinc-500">Class size</Label>
              <Input type="number" min="1" max="40" data-testid="profile-student-count-input" value={form.student_count}
                onChange={(e) => setForm({ ...form, student_count: parseInt(e.target.value, 10) || 1 })}
                className="mt-2 bg-transparent border-zinc-300 rounded-none" />
            </div>
            <div>
              <Label className="text-xs uppercase tracking-widest text-zinc-500">Lesson duration (minutes)</Label>
              <Input type="number" min="15" max="180" step="5" data-testid="profile-duration-input" value={form.duration}
                onChange={(e) => setForm({ ...form, duration: parseInt(e.target.value, 10) || 60 })}
                className="mt-2 bg-transparent border-zinc-300 rounded-none" />
            </div>
            <div>
              <Label className="text-xs uppercase tracking-widest text-zinc-500">French holiday zone</Label>
              <Select value={form.holiday_zone} onValueChange={(v) => setForm({ ...form, holiday_zone: v })}>
                <SelectTrigger data-testid="profile-zone-select" className="mt-2 bg-transparent border-zinc-300 rounded-none"><SelectValue /></SelectTrigger>
                <SelectContent>
                  <SelectItem value="none">— None (skip holidays)</SelectItem>
                  <SelectItem value="A">Zone A (Lyon, Bordeaux, Grenoble…)</SelectItem>
                  <SelectItem value="B">Zone B (Lille, Nantes, Strasbourg…)</SelectItem>
                  <SelectItem value="C">Zone C (Paris, Toulouse, Montpellier…)</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
        </div>

        {/* Priorities */}
        <div className="mt-6 bg-white text-black border border-zinc-200 p-8">
          <div className="text-xs uppercase tracking-widest text-zinc-500 mb-6">Priority skills (drag to reorder)</div>
          <div className="space-y-2">
            {form.priorities.map((p, i) => (
              <div key={p} className="border border-zinc-200 px-5 py-4 flex items-center justify-between">
                <div className="flex items-center gap-4">
                  <span className="text-lime font-display font-bold w-8">#{i + 1}</span>
                  <span className="font-medium">{p}</span>
                </div>
                <div className="flex gap-2">
                  <Button data-testid={`profile-up-${p}`} variant="ghost" size="sm" onClick={() => move(i, -1)} disabled={i === 0} className="rounded-none">↑</Button>
                  <Button data-testid={`profile-down-${p}`} variant="ghost" size="sm" onClick={() => move(i, 1)} disabled={i === form.priorities.length - 1} className="rounded-none">↓</Button>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Activity types */}
        <div className="mt-6 bg-white text-black border border-zinc-200 p-8">
          <div className="text-xs uppercase tracking-widest text-zinc-500 mb-6">Preferred activity types</div>
          <div className="grid sm:grid-cols-2 gap-3">
            {ACTIVITIES.map((a) => {
              const on = form.activity_types.includes(a);
              return (
                <div key={a} data-testid={`profile-activity-${a}`} role="button" tabIndex={0}
                  onClick={() => toggle(a)}
                  onKeyDown={(e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); toggle(a); } }}
                  className={`p-4 border text-left flex items-center gap-3 transition-colors cursor-pointer ${on ? "border-lime bg-zinc-50" : "border-zinc-200 hover:border-zinc-400"}`}>
                  <Checkbox checked={on} className="pointer-events-none data-[state=checked]:bg-lime data-[state=checked]:border-lime" />
                  <span>{a}</span>
                </div>
              );
            })}
          </div>
        </div>

        {/* Family emails */}
        <div className="mt-6 bg-white text-black border border-zinc-200 p-8">
          <div className="text-xs uppercase tracking-widest text-zinc-500 mb-2">{t("profile.family_emails")}</div>
          <p className="text-sm text-zinc-600 mb-4">{t("profile.family_emails_hint")}</p>
          <Textarea data-testid="profile-family-emails" value={form.family_emails}
            onChange={(e) => setForm({ ...form, family_emails: e.target.value })}
            placeholder="parent1@example.com&#10;parent2@example.com&#10;parent3@example.com"
            className="bg-transparent border-zinc-300 rounded-none min-h-32" />
        </div>

        <div className="mt-8 flex justify-end">
          <Button data-testid="profile-save-btn" onClick={save} disabled={saving}
            className="bg-lime text-black hover:bg-[#8BC926] rounded-full px-7 h-11 hover-lift font-semibold">
            {saving ? "Saving…" : "Save changes"}
          </Button>
        </div>
      </div>
    </Layout>
  );
}
