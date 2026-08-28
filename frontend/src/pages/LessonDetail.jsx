import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import Layout from "@/components/Layout";
import api, { getErrorMessage, detailToMessage } from "@/lib/api";
import { useAuth } from "@/lib/auth";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from "@/components/ui/dialog";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { toast } from "sonner";
import { exportLessonPdf } from "@/lib/pdfExport";
// NOT YET PORTED (merge Phase 2): pdfPack.js's exportTeacherPlanPdf/
// exportStudentSheetsPdf/exportAnswerKeyPdf are built for the old pack
// shape (pack.timing/student_pages/answer_key) and would silently break
// against the new pack.teacher_script/sheets shape — see the "Print"
// button below for the interim print path, and the merge plan's docx
// export section for the real replacement.
import { exportHomeworkPdf, exportHomeworkAnswersPdf } from "@/lib/pdfHomework";
import { useI18n } from "@/lib/i18n";
import LessonChat from "@/components/LessonChat";
import { Checkbox } from "@/components/ui/checkbox";
import { EXERCISE_TYPES } from "@/constants/exerciseTypes";
import { SPECIAL_TOPICS } from "@/constants/specialTopics";
import { ArrowLeft, ArrowRight, FileDown, Save, Sparkles, Pencil, RefreshCw, FileText, GraduationCap, KeyRound, BookOpen, Send, AlertTriangle, X } from "lucide-react";

const PHASES = ["presentation", "practice", "production"];

// Lightweight prose-script renderer: the teacher's script is plain text with
// "## Heading" markdown-style section headers (see backend/prompt_builders.py
// build_script_prompt) — not full markdown, just line-based structure.
function ScriptViewer({ text }) {
  if (!text) return null;
  const lines = text.split(/\r?\n/);
  return (
    <div className="space-y-1 text-sm text-zinc-800 leading-relaxed">
      {lines.map((line, i) => {
        const heading = line.match(/^#{1,6}\s*(.+)/);
        if (heading) {
          return <h3 key={i} className="font-display font-bold text-base tracking-tight mt-5 mb-1 first:mt-0">{heading[1]}</h3>;
        }
        if (!line.trim()) return <div key={i} className="h-2" />;
        return <p key={i} className="whitespace-pre-wrap">{line}</p>;
      })}
    </div>
  );
}

export default function LessonDetail() {
  const { week } = useParams();
  const weekNum = parseInt(week, 10);
  const { user } = useAuth();
  const { t } = useI18n();
  const nav = useNavigate();
  const [syllabus, setSyllabus] = useState(null);
  const [lesson, setLesson] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [editMode, setEditMode] = useState(false);
  const [swapDialog, setSwapDialog] = useState(null); // { phase, index }
  const [swapForm, setSwapForm] = useState({ title: "", description: "", type: "", skill: "" });
  const [aiBusy, setAiBusy] = useState(false);
  const [packBusy, setPackBusy] = useState(false);
  const [homeworkBusy, setHomeworkBusy] = useState(false);
  const [exerciseTypes, setExerciseTypes] = useState([]);
  const [topicBusy, setTopicBusy] = useState(false);
  const [docxBusy, setDocxBusy] = useState(null); // which doc type is downloading, or null

  const hasPack = !!lesson?.pack;
  const hasHomework = !!lesson?.homework;

  const toggleExerciseType = (key) => {
    setExerciseTypes((prev) => (prev.includes(key) ? prev.filter((k) => k !== key) : [...prev, key]));
  };

  const applySpecialTopic = async (key) => {
    setTopicBusy(true);
    try {
      const r = await api.post(`/syllabus/${syllabus.id}/week/${weekNum}/special-topic`, { special_topic_key: key || null });
      setLesson({ ...lesson, ...r.data });
      toast.success(key ? "Special topic applied" : "Special topic cleared — back to this week's curriculum");
    } catch (e) {
      toast.error(getErrorMessage(e, "Failed to update special topic"));
    } finally {
      setTopicBusy(false);
    }
  };

  const generateHomework = async () => {
    setHomeworkBusy(true);
    try {
      const r = await api.post(`/syllabus/${syllabus.id}/week/${weekNum}/homework`);
      setLesson({ ...lesson, homework: r.data });
      toast.success(t("hw.generated"));
    } catch (e) {
      toast.error(getErrorMessage(e, t("hw.failed")));
    } finally {
      setHomeworkBusy(false);
    }
  };

  const sendHomeworkEmail = () => {
    if (!lesson?.homework) return;
    const recipients = user?.family_emails || [];
    if (recipients.length === 0) {
      toast.error(t("hw.send_no_recipients"));
      return;
    }
    // First download the PDF so teacher can attach it
    exportHomeworkPdf(lesson, user);
    const subject = t("hw.send_email_subject", { n: lesson.week, title: lesson.homework.title });
    const body = [
      t("hw.send_email_body_1"),
      "",
      t("hw.send_email_body_2", { title: lesson.homework.title, min: lesson.homework.estimated_minutes || 15 }),
      "",
      t("hw.send_email_body_3"),
      "",
      t("hw.send_email_body_4"),
      user?.full_name || "",
    ].join("\n");
    const mailto = `mailto:?bcc=${encodeURIComponent(recipients.join(","))}&subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
    window.location.href = mailto;
    toast.success(t("hw.draft_opened", { n: recipients.length }));
  };

  const downloadDocx = async (docType, label) => {
    setDocxBusy(docType);
    try {
      const r = await api.get(`/syllabus/${syllabus.id}/week/${weekNum}/export/docx`, {
        params: { doc: docType },
        responseType: "blob",
      });
      const blobUrl = URL.createObjectURL(r.data);
      const a = document.createElement("a");
      a.href = blobUrl;
      a.download = `TheTeachkit-Week${String(weekNum).padStart(2, "0")}-${docType}.docx`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(blobUrl);
      toast.success(`${label} downloaded`);
    } catch (e) {
      // responseType "blob" means error bodies also arrive as a Blob, not
      // parsed JSON — read it as text to recover the real detail message.
      const fallback = `Failed to download ${label.toLowerCase()}`;
      let detail = fallback;
      if (e.response?.data instanceof Blob) {
        try {
          const text = await e.response.data.text();
          detail = detailToMessage(JSON.parse(text)?.detail, fallback);
        } catch { /* keep default detail */ }
      } else {
        detail = getErrorMessage(e, fallback);
      }
      toast.error(detail);
    } finally {
      setDocxBusy(null);
    }
  };

  const generatePack = async () => {
    setPackBusy(true);
    try {
      const r = await api.post(`/syllabus/${syllabus.id}/week/${weekNum}/enrich`, { exercise_types: exerciseTypes });
      setLesson({ ...lesson, pack: r.data });
      toast.success(t("pack.generated"));
    } catch (e) {
      toast.error(getErrorMessage(e, "Pack generation failed"));
    } finally {
      setPackBusy(false);
    }
  };

  const load = async () => {
    setLoading(true);
    try {
      const r = await api.get("/syllabus/active");
      setSyllabus(r.data);
      const l = r.data.lessons.find((x) => x.week === weekNum);
      setLesson(l);
    } catch (e) {
      toast.error("Failed to load lesson");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, [weekNum]);

  const save = async () => {
    setSaving(true);
    try {
      const r = await api.put(`/syllabus/${syllabus.id}/week/${weekNum}`, lesson);
      setLesson(r.data);
      toast.success(t("lesson.saved"));
      setEditMode(false);
    } catch (e) {
      toast.error(t("lesson.save_failed"));
    } finally {
      setSaving(false);
    }
  };

  const openSwap = (phase, index) => {
    const activity = lesson.ppp[phase].activities[index];
    setSwapForm({ ...activity });
    setSwapDialog({ phase, index });
  };

  const doSwap = async () => {
    try {
      const r = await api.post(`/syllabus/${syllabus.id}/week/${weekNum}/swap-activity`, {
        phase: swapDialog.phase,
        index: swapDialog.index,
        new_activity: swapForm,
      });
      setLesson(r.data);
      setSwapDialog(null);
      toast.success(t("lesson.swap_ok"));
    } catch (e) {
      toast.error(t("lesson.swap_failed"));
    }
  };

  const aiSuggest = async () => {
    if (!swapDialog) return;
    setAiBusy(true);
    try {
      const r = await api.post("/ai/suggest-activity", {
        week_theme: lesson.theme,
        grammar: lesson.grammar,
        vocabulary: lesson.vocabulary,
        phase: swapDialog.phase,
        skill_focus: swapForm.skill || user?.priorities?.[0] || "Speaking",
        current_activity_title: swapForm.title,
      });
      setSwapForm(r.data);
      toast.success(t("lesson.ai_ok"));
    } catch (e) {
      toast.error(getErrorMessage(e, t("lesson.ai_failed")));
    } finally {
      setAiBusy(false);
    }
  };

  if (loading || !lesson) return <Layout><div className="p-14 text-zinc-400 font-body">Loading lesson…</div></Layout>;

  const updateLessonField = (field, value) => setLesson({ ...lesson, [field]: value });

  return (
    <Layout>
      <div className="p-8 lg:p-12">
        {/* Top nav */}
        <div className="flex items-center justify-between mb-8">
          <Button data-testid="lesson-back-btn" variant="ghost" onClick={() => nav("/dashboard")} className="text-zinc-400 hover:text-white hover:bg-zinc-900 rounded-none">
            <ArrowLeft className="h-4 w-4 mr-2" /> Back to syllabus
          </Button>
          <div className="flex gap-2">
            <Button data-testid="lesson-prev-btn" variant="ghost" onClick={() => weekNum > 1 && nav(`/week/${weekNum - 1}`)} disabled={weekNum <= 1}
              className="border border-zinc-800 text-white hover:bg-zinc-900 rounded-none">
              <ArrowLeft className="h-4 w-4" />
            </Button>
            <Button data-testid="lesson-next-btn" variant="ghost" onClick={() => weekNum < 32 && nav(`/week/${weekNum + 1}`)} disabled={weekNum >= 32}
              className="border border-zinc-800 text-white hover:bg-zinc-900 rounded-none">
              <ArrowRight className="h-4 w-4" />
            </Button>
          </div>
        </div>

        {/* Special-topic override: one-off grammar focus for revision/off-
            curriculum weeks, overriding this week's normal curriculum topic. */}
        {lesson.special_topic_key && (
          <div data-testid="special-topic-warning" className="mb-4 border border-amber-400 bg-amber-50 text-amber-900 px-5 py-3 flex items-center justify-between gap-4 text-sm">
            <span className="flex items-center gap-2">
              <AlertTriangle className="h-4 w-4 shrink-0" />
              Special topic active — this week's real curriculum topic is being skipped until you clear it.
            </span>
            <Button data-testid="clear-special-topic-btn" onClick={() => applySpecialTopic(null)} disabled={topicBusy}
              variant="ghost" size="sm" className="text-amber-900 hover:bg-amber-100 rounded-none shrink-0">
              <X className="h-3 w-3 mr-1" /> Clear
            </Button>
          </div>
        )}
        <div className="mb-8 flex items-center gap-3">
          <Label className="text-xs uppercase tracking-widest text-zinc-500 whitespace-nowrap">Special topic override</Label>
          <Select value={lesson.special_topic_key || "__none__"} onValueChange={(v) => applySpecialTopic(v === "__none__" ? null : v)} disabled={topicBusy}>
            <SelectTrigger data-testid="special-topic-select" className="bg-zinc-950 border-zinc-800 text-white rounded-none h-9 max-w-xs"><SelectValue /></SelectTrigger>
            <SelectContent className="bg-zinc-950 border-zinc-800 text-white">
              <SelectItem value="__none__">— None (this week's curriculum)</SelectItem>
              {SPECIAL_TOPICS.map((topic) => (
                <SelectItem key={topic.key} value={topic.key}>{topic.label}</SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        {/* Header card */}
        <div className="bg-white text-black p-8 border border-zinc-200 mb-8">
          <div className="flex flex-wrap items-start justify-between gap-4">
            <div className="flex-1 min-w-0">
              <div className="text-xs uppercase tracking-widest text-zinc-500">Week {lesson.week} · CEFR {lesson.cefr_level}</div>
              {editMode ? (
                <Input data-testid="lesson-title-input" value={lesson.title} onChange={(e) => updateLessonField("title", e.target.value)}
                  className="mt-3 font-display font-bold text-3xl bg-transparent border-zinc-300 rounded-none h-14 tracking-tight" />
              ) : (
                <h1 className="font-display font-bold text-4xl tracking-tight mt-3" data-testid="lesson-title">{lesson.title}</h1>
              )}
            </div>
            <div className="flex flex-wrap gap-2">
              <Button data-testid="lesson-export-btn" onClick={() => { exportLessonPdf(lesson, user); toast.success(t("pdf.downloaded")); }}
                className="bg-lime text-black hover:bg-[#8BC926] rounded-full px-5 hover-lift font-semibold">
                <FileDown className="h-4 w-4 mr-2" /> Quick PDF
              </Button>
              {!editMode ? (
                <Button data-testid="lesson-edit-btn" onClick={() => setEditMode(true)} variant="ghost" className="border border-zinc-300 text-black hover:bg-zinc-100 rounded-full px-5">
                  <Pencil className="h-4 w-4 mr-2" /> Edit
                </Button>
              ) : (
                <Button data-testid="lesson-save-btn" onClick={save} disabled={saving} className="bg-black text-white hover:bg-zinc-900 rounded-full px-5">
                  <Save className="h-4 w-4 mr-2" /> {saving ? "Saving…" : "Save"}
                </Button>
              )}
            </div>
          </div>

          <div className="mt-10 grid md:grid-cols-2 gap-8">
            <div>
              <div className="text-xs uppercase tracking-widest text-zinc-500 mb-2">Grammar focus</div>
              {editMode ? (
                <Input data-testid="lesson-grammar-input" value={lesson.grammar} onChange={(e) => updateLessonField("grammar", e.target.value)}
                  className="bg-transparent border-zinc-300 rounded-none" />
              ) : (
                <div className="text-black font-medium">{lesson.grammar}</div>
              )}
            </div>
            <div>
              <div className="text-xs uppercase tracking-widest text-zinc-500 mb-2">Vocabulary</div>
              {editMode ? (
                <Input data-testid="lesson-vocab-input" value={lesson.vocabulary.join(", ")}
                  onChange={(e) => updateLessonField("vocabulary", e.target.value.split(",").map((v) => v.trim()).filter(Boolean))}
                  className="bg-transparent border-zinc-300 rounded-none" />
              ) : (
                <div className="flex flex-wrap gap-1.5">
                  {lesson.vocabulary.map((v) => (
                    <Badge key={v} variant="secondary" className="bg-zinc-100 text-black rounded-none border-none uppercase text-[10px] tracking-widest">{v}</Badge>
                  ))}
                </div>
              )}
            </div>
            <div>
              <div className="text-xs uppercase tracking-widest text-zinc-500 mb-2">Objectives</div>
              {editMode ? (
                <Textarea data-testid="lesson-objectives-input"
                  value={lesson.objectives.join("\n")}
                  onChange={(e) => updateLessonField("objectives", e.target.value.split("\n").map((o) => o.trim()).filter(Boolean))}
                  className="bg-transparent border-zinc-300 rounded-none min-h-24" />
              ) : (
                <ol className="list-decimal list-inside space-y-1 text-sm text-zinc-800">
                  {lesson.objectives.map((o, i) => <li key={i}>{o}</li>)}
                </ol>
              )}
            </div>
            <div>
              <div className="text-xs uppercase tracking-widest text-zinc-500 mb-2">Materials</div>
              {editMode ? (
                <Textarea data-testid="lesson-materials-input"
                  value={lesson.materials.join("\n")}
                  onChange={(e) => updateLessonField("materials", e.target.value.split("\n").map((m) => m.trim()).filter(Boolean))}
                  className="bg-transparent border-zinc-300 rounded-none min-h-24" />
              ) : (
                <ul className="space-y-1 text-sm text-zinc-800">
                  {lesson.materials.map((m, i) => <li key={i} className="flex gap-2"><span className="text-lime">▪</span>{m}</li>)}
                </ul>
              )}
            </div>
          </div>
        </div>

        {/* Teacher Pack: prose teacher's script + skill sheets + optional
            exercise-type sheets — validated engine format (Form+Function
            grammar, 6-word vocab cap, zero repetition between script/sheet/
            answer-key). Docx export lands in a later pass. */}
        <div className="bg-white text-black border-2 border-lime p-8 mb-8" data-testid="teacher-pack-section">
          <div className="flex flex-wrap items-start justify-between gap-4">
            <div>
              <div className="text-xs uppercase tracking-widest text-lime mb-2">Full teacher pack</div>
              <h2 className="font-display font-bold text-2xl tracking-tight">
                {hasPack ? "Teacher's script & activity sheets" : "Generate the full teacher pack"}
              </h2>
              <p className="mt-2 text-sm text-zinc-600 max-w-xl">
                A real teacher's-own-notes lesson script (Form + Function grammar breakdown, max 6 vocabulary
                words with pronunciation) plus 4 printable skill sheets — Speaking, Listening, Reading, Writing —
                and any grammar/vocab practice formats you pick below. Powered by Claude Sonnet 5.
              </p>
            </div>
            {!hasPack ? (
              <Button data-testid="pack-generate-btn" onClick={generatePack} disabled={packBusy}
                className="bg-black text-white hover:bg-zinc-900 rounded-full px-6 h-11 font-semibold">
                <Sparkles className={`h-4 w-4 mr-2 ${packBusy ? "animate-pulse" : ""}`} />
                {packBusy ? "Generating (20-40s)…" : "Generate teacher pack"}
              </Button>
            ) : (
              <div className="flex gap-2">
                <Button data-testid="pack-print-btn" onClick={() => window.print()} variant="ghost"
                  className="border border-zinc-300 rounded-full px-5 h-11">
                  <FileDown className="h-4 w-4 mr-2" /> Print
                </Button>
                <Button data-testid="pack-regenerate-btn" onClick={generatePack} disabled={packBusy} variant="ghost"
                  className="border border-zinc-300 rounded-full px-5 h-11">
                  <RefreshCw className={`h-4 w-4 mr-2 ${packBusy ? "animate-spin" : ""}`} />
                  {packBusy ? "Regenerating…" : "Regenerate"}
                </Button>
              </div>
            )}
          </div>

          {hasPack && (
            <div className="mt-6 grid sm:grid-cols-3 gap-3">
              <Button data-testid="download-script-btn" onClick={() => downloadDocx("script", "Teacher's Script")} disabled={docxBusy === "script"}
                className="bg-black text-white hover:bg-zinc-900 rounded-none h-14 justify-start px-5">
                <FileText className="h-5 w-5 mr-3 text-lime" />
                <div className="text-left leading-tight">
                  <div className="text-[10px] uppercase tracking-widest text-zinc-400">Document 1</div>
                  <div className="font-semibold">{docxBusy === "script" ? "Downloading…" : "Teacher's script (.docx)"}</div>
                </div>
              </Button>
              <Button data-testid="download-sheets-btn" onClick={() => downloadDocx("sheets", "Activity Sheets")} disabled={docxBusy === "sheets"}
                className="bg-black text-white hover:bg-zinc-900 rounded-none h-14 justify-start px-5">
                <GraduationCap className="h-5 w-5 mr-3 text-lime" />
                <div className="text-left leading-tight">
                  <div className="text-[10px] uppercase tracking-widest text-zinc-400">Document 2</div>
                  <div className="font-semibold">{docxBusy === "sheets" ? "Downloading…" : "Activity sheets (.docx)"}</div>
                </div>
              </Button>
              <Button data-testid="download-answerkey-btn" onClick={() => downloadDocx("answerkey", "Answer Key")} disabled={docxBusy === "answerkey"}
                className="bg-black text-white hover:bg-zinc-900 rounded-none h-14 justify-start px-5">
                <KeyRound className="h-5 w-5 mr-3 text-lime" />
                <div className="text-left leading-tight">
                  <div className="text-[10px] uppercase tracking-widest text-zinc-400">Document 3</div>
                  <div className="font-semibold">{docxBusy === "answerkey" ? "Downloading…" : "Answer key (.docx)"}</div>
                </div>
              </Button>
            </div>
          )}

          <div className="mt-6 border-t border-zinc-200 pt-4">
            <div className="text-xs uppercase tracking-widest text-zinc-500 mb-3">
              Extra grammar/vocab practice sheets (optional — pick before generating or regenerating)
            </div>
            <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-2">
              {EXERCISE_TYPES.map((ex) => {
                const on = exerciseTypes.includes(ex.key);
                return (
                  <div key={ex.key} data-testid={`exercise-type-${ex.key}`} role="button" tabIndex={0}
                    onClick={() => toggleExerciseType(ex.key)}
                    onKeyDown={(e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); toggleExerciseType(ex.key); } }}
                    className={`p-3 border text-left flex items-center gap-2 text-sm cursor-pointer transition-colors ${on ? "border-lime bg-zinc-50" : "border-zinc-200 hover:border-zinc-400"}`}>
                    <Checkbox checked={on} className="pointer-events-none data-[state=checked]:bg-lime data-[state=checked]:border-lime" />
                    <span>{ex.label}</span>
                  </div>
                );
              })}
            </div>
          </div>

          {hasPack && lesson.pack.teacher_script && (
            <div className="mt-8 border-t border-zinc-200 pt-6">
              <div className="text-xs uppercase tracking-widest text-zinc-500 mb-4 flex items-center gap-2">
                <FileText className="h-4 w-4 text-lime" /> Teacher's script
              </div>
              <ScriptViewer text={lesson.pack.teacher_script} />
            </div>
          )}

          {hasPack && Array.isArray(lesson.pack.sheets) && lesson.pack.sheets.length > 0 && (
            <div className="mt-8 border-t border-zinc-200 pt-6">
              <div className="text-xs uppercase tracking-widest text-zinc-500 mb-4 flex items-center gap-2">
                <GraduationCap className="h-4 w-4 text-lime" /> Activity sheets
              </div>
              <div className="grid lg:grid-cols-2 gap-4">
                {lesson.pack.sheets.map((s) => (
                  <div key={s.letter} data-testid={`sheet-card-${s.letter}`} className="border border-zinc-200 p-5">
                    <div className="flex items-center gap-2 mb-3">
                      <Badge className="bg-black text-white rounded-none uppercase text-[10px] tracking-widest">Sheet {s.letter}</Badge>
                      <span className="font-display font-bold text-sm tracking-tight">{s.title}</span>
                    </div>
                    <div className="text-xs text-zinc-800 whitespace-pre-wrap max-h-64 overflow-y-auto">{s.student_content || s.content}</div>
                    {s.teacher_notes && (
                      <details className="mt-3">
                        <summary className="text-[10px] uppercase tracking-widest text-zinc-500 cursor-pointer flex items-center gap-1">
                          <KeyRound className="h-3 w-3" /> Answer key / teacher notes
                        </summary>
                        <div className="mt-2 text-xs text-zinc-600 whitespace-pre-wrap bg-zinc-50 p-3 border border-zinc-200">{s.teacher_notes}</div>
                      </details>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {hasPack && Array.isArray(lesson.pack.exercise_sheets) && lesson.pack.exercise_sheets.length > 0 && (
            <div className="mt-8 border-t border-zinc-200 pt-6">
              <div className="text-xs uppercase tracking-widest text-zinc-500 mb-4 flex items-center gap-2">
                <GraduationCap className="h-4 w-4 text-lime" /> Grammar & vocab practice sheets
              </div>
              <div className="grid lg:grid-cols-2 gap-4">
                {lesson.pack.exercise_sheets.map((s) => (
                  <div key={s.key} data-testid={`exercise-sheet-card-${s.key}`} className="border border-zinc-200 p-5">
                    <div className="flex items-center gap-2 mb-3">
                      <Badge className="bg-lime text-black rounded-none uppercase text-[10px] tracking-widest border-none">{s.title}</Badge>
                    </div>
                    <div className="text-xs text-zinc-800 whitespace-pre-wrap max-h-64 overflow-y-auto">{s.student_content || s.content}</div>
                    {s.teacher_notes && (
                      <details className="mt-3">
                        <summary className="text-[10px] uppercase tracking-widest text-zinc-500 cursor-pointer flex items-center gap-1">
                          <KeyRound className="h-3 w-3" /> Answer key
                        </summary>
                        <div className="mt-2 text-xs text-zinc-600 whitespace-pre-wrap bg-zinc-50 p-3 border border-zinc-200">{s.teacher_notes}</div>
                      </details>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {hasPack && lesson.pack.extension && (
            <div className="mt-8 border-t border-zinc-200 pt-6">
              <div className="text-xs uppercase tracking-widest text-zinc-500 mb-3">Fast-finisher extension</div>
              <div className="text-sm text-zinc-800 whitespace-pre-wrap border border-zinc-200 p-4 bg-zinc-50">{lesson.pack.extension}</div>
            </div>
          )}

          {hasPack && !lesson.pack.teacher_script && (
            <div className="mt-6 border-t border-zinc-200 pt-4 text-sm text-zinc-500">
              This pack was generated under an older format — hit Regenerate to get the current teacher's-script + sheets format.
            </div>
          )}
        </div>

        {/* Homework */}
        <div className="bg-white text-black border border-zinc-200 p-8 mb-8" data-testid="homework-section">
          <div className="flex flex-wrap items-start justify-between gap-4">
            <div>
              <div className="flex items-center gap-2 mb-2">
                <BookOpen className="h-5 w-5" />
                <div className="text-xs uppercase tracking-widest text-zinc-500">{t("lesson.homework_kicker")}</div>
              </div>
              <h2 className="font-display font-bold text-2xl tracking-tight">
                {hasHomework ? t("lesson.homework_title_generated") : t("lesson.homework_title_missing")}
              </h2>
              <p className="mt-2 text-sm text-zinc-600 max-w-xl">{t("lesson.homework_desc")}</p>
            </div>
            {!hasHomework ? (
              <Button data-testid="homework-generate-btn" onClick={generateHomework} disabled={homeworkBusy}
                className="bg-black text-white hover:bg-zinc-900 rounded-full px-6 h-11 font-semibold">
                <Sparkles className={`h-4 w-4 mr-2 ${homeworkBusy ? "animate-pulse" : ""}`} />
                {homeworkBusy ? t("lesson.homework_generating") : t("lesson.homework_generate")}
              </Button>
            ) : (
              <Button data-testid="homework-regenerate-btn" onClick={generateHomework} disabled={homeworkBusy} variant="ghost"
                className="border border-zinc-300 rounded-full px-5 h-11">
                <RefreshCw className={`h-4 w-4 mr-2 ${homeworkBusy ? "animate-spin" : ""}`} />
                {homeworkBusy ? t("lesson.homework_generating") : t("lesson.pack_regenerate")}
              </Button>
            )}
          </div>
          {hasHomework && (
            <div className="mt-6 grid sm:grid-cols-2 gap-3">
              <Button data-testid="homework-download-btn" onClick={() => { exportHomeworkPdf(lesson, user); toast.success(t("hw.download_ok")); }}
                className="bg-lime text-black hover:bg-[#8BC926] rounded-none h-12 justify-start px-5 font-semibold">
                <FileDown className="h-4 w-4 mr-2" /> {t("lesson.homework_download")}
              </Button>
              <Button data-testid="homework-answers-btn" onClick={() => { exportHomeworkAnswersPdf(lesson, user); toast.success(t("hw.answers_ok")); }}
                variant="ghost" className="border border-zinc-300 rounded-none h-12 justify-start px-5">
                <KeyRound className="h-4 w-4 mr-2" /> {t("lesson.homework_download_answers")}
              </Button>
              <Button data-testid="homework-send-btn" onClick={sendHomeworkEmail}
                className="bg-black text-white hover:bg-zinc-900 rounded-none h-12 justify-start px-5 sm:col-span-2">
                <Send className="h-4 w-4 mr-2 text-lime" /> {t("hw.send_families")}
              </Button>
            </div>
          )}
        </div>

        {/* PPP */}
        <div className="space-y-6">
          {PHASES.map((p) => {
            const phase = lesson.ppp[p];
            return (
              <div key={p} className="bg-white text-black border border-zinc-200 p-8" data-testid={`ppp-phase-${p}`}>
                <div className="flex items-center justify-between mb-6">
                  <div>
                    <div className="text-xs uppercase tracking-widest text-lime">{phase.phase}</div>
                    <h2 className="font-display font-bold text-2xl tracking-tight mt-1">{phase.duration_min} minutes</h2>
                  </div>
                </div>
                <div className="space-y-4">
                  {phase.activities.map((a, i) => (
                    <div key={i} data-testid={`activity-${p}-${i}`} className="border border-zinc-200 p-5 flex flex-col md:flex-row md:items-start gap-4 hover:border-zinc-400 transition-colors">
                      <div className="flex-1">
                        <div className="flex flex-wrap items-center gap-2 mb-2">
                          <Badge className="bg-black text-white rounded-none uppercase text-[10px] tracking-widest">{a.type}</Badge>
                          <Badge variant="secondary" className="bg-lime text-black rounded-none uppercase text-[10px] tracking-widest border-none">{a.skill}</Badge>
                        </div>
                        <h3 className="font-display font-bold text-lg tracking-tight">{a.title}</h3>
                        <p className="text-sm text-zinc-700 mt-2 leading-relaxed">{a.description}</p>
                      </div>
                      <Button data-testid={`swap-btn-${p}-${i}`} onClick={() => openSwap(p, i)} variant="ghost"
                        className="border border-zinc-300 hover:border-lime hover:bg-zinc-50 rounded-full text-xs uppercase tracking-widest px-4">
                        <RefreshCw className="h-3 w-3 mr-2" /> Swap
                      </Button>
                    </div>
                  ))}
                </div>
              </div>
            );
          })}
        </div>

        {/* Notes */}
        <div className="mt-6 bg-white text-black border border-zinc-200 p-8">
          <div className="text-xs uppercase tracking-widest text-zinc-500 mb-3">Teacher notes</div>
          <Textarea data-testid="lesson-notes-input" value={lesson.notes || ""} onChange={(e) => updateLessonField("notes", e.target.value)}
            onBlur={save} placeholder="Add your notes for this week…" className="bg-transparent border-zinc-300 rounded-none min-h-24" />
        </div>
      </div>

      {/* Swap dialog */}
      <Dialog open={!!swapDialog} onOpenChange={(o) => !o && setSwapDialog(null)}>
        <DialogContent className="bg-zinc-950 text-white border-zinc-800 rounded-none max-w-lg">
          <DialogHeader>
            <DialogTitle className="font-display tracking-tight text-2xl">Swap activity</DialogTitle>
          </DialogHeader>
          <div className="space-y-4">
            <div>
              <Label className="text-xs uppercase tracking-widest text-zinc-400">Title</Label>
              <Input data-testid="swap-title-input" value={swapForm.title} onChange={(e) => setSwapForm({ ...swapForm, title: e.target.value })}
                className="mt-2 bg-black border-zinc-800 rounded-none" />
            </div>
            <div>
              <Label className="text-xs uppercase tracking-widest text-zinc-400">Description</Label>
              <Textarea data-testid="swap-desc-input" value={swapForm.description} onChange={(e) => setSwapForm({ ...swapForm, description: e.target.value })}
                className="mt-2 bg-black border-zinc-800 rounded-none min-h-24" />
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label className="text-xs uppercase tracking-widest text-zinc-400">Type</Label>
                <Input data-testid="swap-type-input" value={swapForm.type} onChange={(e) => setSwapForm({ ...swapForm, type: e.target.value })}
                  className="mt-2 bg-black border-zinc-800 rounded-none" />
              </div>
              <div>
                <Label className="text-xs uppercase tracking-widest text-zinc-400">Skill</Label>
                <Input data-testid="swap-skill-input" value={swapForm.skill} onChange={(e) => setSwapForm({ ...swapForm, skill: e.target.value })}
                  className="mt-2 bg-black border-zinc-800 rounded-none" />
              </div>
            </div>
            <Button data-testid="swap-ai-btn" onClick={aiSuggest} disabled={aiBusy} variant="ghost"
              className="w-full border border-lime text-lime hover:bg-lime hover:text-black rounded-none">
              <Sparkles className={`h-4 w-4 mr-2 ${aiBusy ? "animate-pulse" : ""}`} />
              {aiBusy ? "Asking Claude…" : "Suggest with AI"}
            </Button>
          </div>
          <DialogFooter>
            <Button variant="ghost" onClick={() => setSwapDialog(null)} className="rounded-none">Cancel</Button>
            <Button data-testid="swap-save-btn" onClick={doSwap} className="bg-lime text-black hover:bg-[#8BC926] rounded-none">Save swap</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {syllabus && (
        <LessonChat syllabusId={syllabus.id} weekNum={weekNum} lessonTitle={lesson.title} />
      )}
    </Layout>
  );
}
