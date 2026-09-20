import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import Layout from "@/components/Layout";
import api, { getErrorMessage } from "@/lib/api";
import { useAuth } from "@/lib/auth";
import { Button } from "@/components/ui/button";
import { Check, X } from "lucide-react";
import { toast } from "sonner";

const FREE_FEATURES = [
  { label: "Full year syllabus & curriculum browsing", on: true },
  { label: "AI teacher script + worksheets", on: true, note: "Speaking & Listening only" },
  { label: "Exercise-type practice sheets", on: true, note: "up to 2 per lesson" },
  { label: "Reading & Writing sheets", on: false },
  { label: "Batch-generate a whole term at once", on: false },
  { label: ".docx export", on: false },
];

const PRO_FEATURES = [
  { label: "Full year syllabus & curriculum browsing", on: true },
  { label: "AI teacher script + worksheets", on: true, note: "all 4 skills" },
  { label: "Exercise-type practice sheets", on: true, note: "unlimited" },
  { label: "Reading & Writing sheets", on: true },
  { label: "Batch-generate a whole term at once", on: true },
  { label: ".docx export", on: true },
];

function FeatureRow({ label, on, note }) {
  return (
    <div className="flex items-start gap-3 py-2.5 border-b border-zinc-100 last:border-0">
      {on ? <Check className="h-4 w-4 text-lime shrink-0 mt-0.5" /> : <X className="h-4 w-4 text-zinc-300 shrink-0 mt-0.5" />}
      <div>
        <div className={on ? "text-black" : "text-zinc-400"}>{label}</div>
        {note && <div className="text-xs text-zinc-500">{note}</div>}
      </div>
    </div>
  );
}

export default function Plans() {
  const { user, refresh } = useAuth();
  const [searchParams, setSearchParams] = useSearchParams();
  const [plan, setPlan] = useState("annual");
  const [busy, setBusy] = useState(false);
  const isPro = user?.subscription_tier === "pro";

  useEffect(() => {
    const checkout = searchParams.get("checkout");
    if (checkout === "success") {
      toast.success("You're on Pro now — welcome aboard!");
      refresh();
    } else if (checkout === "cancelled") {
      toast.info("Checkout cancelled — no charge was made.");
    }
    if (checkout) {
      searchParams.delete("checkout");
      setSearchParams(searchParams, { replace: true });
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const upgrade = async () => {
    setBusy(true);
    try {
      const r = await api.post("/billing/create-checkout-session", { plan });
      window.location.href = r.data.checkout_url;
    } catch (e) {
      toast.error(getErrorMessage(e, "Could not start checkout"));
      setBusy(false);
    }
  };

  const manageSubscription = async () => {
    setBusy(true);
    try {
      const r = await api.post("/billing/portal");
      window.location.href = r.data.portal_url;
    } catch (e) {
      toast.error(getErrorMessage(e, "Could not open the billing portal"));
      setBusy(false);
    }
  };

  return (
    <Layout>
      <div className="p-8 lg:p-12 max-w-5xl">
        <div className="text-xs uppercase tracking-widest text-lime mb-2">Pricing</div>
        <h1 className="font-display font-bold text-5xl tracking-tight">Plans</h1>
        <p className="mt-3 text-zinc-400 max-w-xl">
          Free gives you a real feel for the output. Pro unlocks the full lesson pack — all four skills, unlimited practice sheets, batch generation, and exports.
        </p>

        <div className="mt-10 grid md:grid-cols-2 gap-6">
          {/* Free */}
          <div className="bg-white text-black border border-zinc-200 p-8 flex flex-col">
            <div className="text-xs uppercase tracking-widest text-zinc-500 mb-2">Free</div>
            <div className="font-display font-bold text-4xl mb-1">€0</div>
            <div className="text-sm text-zinc-500 mb-6">forever</div>
            <div className="flex-1">
              {FREE_FEATURES.map((f) => <FeatureRow key={f.label} {...f} />)}
            </div>
            {!isPro && (
              <div className="mt-6 text-center text-xs uppercase tracking-widest text-zinc-400 border border-zinc-200 py-3">
                Current plan
              </div>
            )}
          </div>

          {/* Pro */}
          <div className="bg-white text-black border-2 border-lime p-8 flex flex-col relative">
            <div className="absolute -top-3 left-8 bg-lime text-black text-xs uppercase tracking-widest font-semibold px-3 py-1">
              Full experience
            </div>
            <div className="text-xs uppercase tracking-widest text-zinc-500 mb-2 mt-2">Pro</div>

            {!isPro && (
              <div className="inline-flex border border-zinc-300 mb-4 w-fit" data-testid="plans-toggle">
                <button data-testid="plans-toggle-monthly" onClick={() => setPlan("monthly")}
                  className={`px-4 py-1.5 text-sm font-medium ${plan === "monthly" ? "bg-black text-white" : "text-zinc-600"}`}>
                  Monthly
                </button>
                <button data-testid="plans-toggle-annual" onClick={() => setPlan("annual")}
                  className={`px-4 py-1.5 text-sm font-medium ${plan === "annual" ? "bg-black text-white" : "text-zinc-600"}`}>
                  Annual
                </button>
              </div>
            )}

            <div className="font-display font-bold text-4xl mb-1">{plan === "annual" || isPro ? "€120" : "€14"}</div>
            <div className="text-sm text-zinc-500 mb-6">
              {isPro ? "your current plan" : plan === "annual" ? "per year (~30% off monthly)" : "per month"}
            </div>

            <div className="flex-1">
              {PRO_FEATURES.map((f) => <FeatureRow key={f.label} {...f} />)}
            </div>

            <div className="mt-6">
              {isPro ? (
                <Button data-testid="plans-manage-btn" onClick={manageSubscription} disabled={busy}
                  className="w-full bg-black text-white hover:bg-zinc-800 rounded-full h-11 font-semibold">
                  {busy ? "Opening…" : "Manage subscription"}
                </Button>
              ) : (
                <Button data-testid="plans-upgrade-btn" onClick={upgrade} disabled={busy}
                  className="w-full bg-lime text-black hover:bg-[#8BC926] rounded-full h-11 hover-lift font-semibold">
                  {busy ? "Redirecting…" : "Upgrade to Pro"}
                </Button>
              )}
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}
