import { useState, useRef, useEffect } from "react";
import { Sparkles, Send, X, MessageCircle } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useI18n } from "@/lib/i18n";
import api, { getErrorMessage } from "@/lib/api";
import { toast } from "sonner";

export default function LessonChat({ syllabusId, weekNum, lessonTitle }) {
  const { t, lang } = useI18n();
  const [open, setOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);
  const scrollRef = useRef(null);

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
  }, [messages, open]);

  const send = async () => {
    const message = input.trim();
    if (!message) return;
    const next = [...messages, { role: "user", content: message }];
    setMessages(next);
    setInput("");
    setBusy(true);
    try {
      const r = await api.post(`/syllabus/${syllabusId}/week/${weekNum}/chat`, {
        message,
        history: messages,
        lang,
      });
      setMessages([...next, { role: "assistant", content: r.data.response }]);
    } catch (e) {
      toast.error(getErrorMessage(e, t("chat.error")));
      // Restore input & rollback the user msg
      setInput(message);
      setMessages(next.slice(0, -1));
    } finally {
      setBusy(false);
    }
  };

  const quickPrompts = [
    t("chat.suggest_rephrase"),
    t("chat.suggest_level_down"),
    t("chat.suggest_warmer"),
    t("chat.suggest_example"),
  ];

  return (
    <>
      {!open && (
        <button
          data-testid="chat-fab-btn"
          onClick={() => setOpen(true)}
          className="fixed bottom-6 right-6 z-40 bg-lime text-black rounded-full h-14 pl-5 pr-6 shadow-2xl hover-lift flex items-center gap-2 font-semibold"
        >
          <MessageCircle className="h-5 w-5" />
          <span className="hidden sm:inline">{t("chat.fab")}</span>
        </button>
      )}
      {open && (
        <div
          data-testid="chat-panel"
          className="fixed bottom-6 right-6 z-40 w-[min(96vw,420px)] h-[min(78vh,620px)] bg-black text-white border-2 border-lime shadow-2xl flex flex-col"
        >
          <div className="flex items-center justify-between px-5 py-4 border-b border-zinc-800 bg-zinc-950">
            <div className="flex items-center gap-3">
              <div className="h-9 w-9 bg-lime text-black rounded-full flex items-center justify-center">
                <Sparkles className="h-4 w-4" />
              </div>
              <div className="leading-tight">
                <div className="font-display font-bold">{t("chat.title")}</div>
                <div className="text-[10px] uppercase tracking-widest text-zinc-500">Week {weekNum}</div>
              </div>
            </div>
            <button data-testid="chat-close-btn" onClick={() => setOpen(false)} className="text-zinc-400 hover:text-white">
              <X className="h-5 w-5" />
            </button>
          </div>

          <div ref={scrollRef} className="flex-1 overflow-y-auto p-4 space-y-3">
            {messages.length === 0 && (
              <div data-testid="chat-empty" className="text-sm text-zinc-400">
                <p className="mb-2">{t("chat.intro_a")} <span className="text-white">{lessonTitle}</span>.</p>
                <p className="text-xs text-zinc-500 mb-4">{t("chat.intro_b")}</p>
                <div className="space-y-2">
                  {quickPrompts.map((q, i) => (
                    <button key={i} data-testid={`chat-quick-${i}`} onClick={() => setInput(q)}
                      className="w-full text-left text-sm text-zinc-200 border border-zinc-800 hover:border-lime hover:text-white p-3 transition-colors">
                      {q}
                    </button>
                  ))}
                </div>
              </div>
            )}
            {messages.map((m, i) => (
              <div key={i} data-testid={`chat-msg-${i}`}
                className={`flex ${m.role === "user" ? "justify-end" : "justify-start"}`}>
                <div className={`max-w-[85%] px-4 py-3 text-sm leading-relaxed whitespace-pre-wrap ${
                  m.role === "user"
                    ? "bg-lime text-black"
                    : "bg-zinc-900 text-white border border-zinc-800"
                }`}>
                  {m.content}
                </div>
              </div>
            ))}
            {busy && (
              <div className="flex justify-start">
                <div className="bg-zinc-900 border border-zinc-800 px-4 py-3 text-sm text-zinc-400 flex items-center gap-2">
                  <span className="h-1.5 w-1.5 bg-lime rounded-full animate-pulse" />
                  <span className="h-1.5 w-1.5 bg-lime rounded-full animate-pulse" style={{ animationDelay: "0.15s" }} />
                  <span className="h-1.5 w-1.5 bg-lime rounded-full animate-pulse" style={{ animationDelay: "0.3s" }} />
                </div>
              </div>
            )}
          </div>

          <div className="border-t border-zinc-800 p-3 bg-zinc-950">
            <div className="flex gap-2">
              <textarea
                data-testid="chat-input"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); send(); } }}
                placeholder={t("chat.placeholder")}
                rows={2}
                className="flex-1 bg-black border border-zinc-800 text-white text-sm p-2 focus:outline-none focus:border-lime resize-none"
              />
              <Button data-testid="chat-send-btn" onClick={send} disabled={busy || !input.trim()}
                className="bg-lime text-black hover:bg-[#8BC926] rounded-none h-auto px-4">
                <Send className="h-4 w-4" />
              </Button>
            </div>
            <div className="text-[10px] text-zinc-600 mt-2 uppercase tracking-widest">{t("chat.model_footer")}</div>
          </div>
        </div>
      )}
    </>
  );
}
