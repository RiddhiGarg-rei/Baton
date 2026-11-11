import { accessLabel } from "../citation";

// Colour is never the only signal: every chip also shows its name in words.
const STYLES = {
  public: "bg-emerald-100 text-emerald-900",
  team: "bg-sky-100 text-sky-900",
  lead_only: "bg-amber-100 text-amber-900",
  restricted: "bg-rose-100 text-rose-900",
};

export default function AccessChip({ level }) {
  return (
    <span
      className={`inline-block rounded-full px-2.5 py-0.5 text-xs font-bold ${
        STYLES[level] ?? "bg-slate-200 text-slate-800"
      }`}
    >
      {accessLabel(level)}
    </span>
  );
}
