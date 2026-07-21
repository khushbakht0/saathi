"use client";

import { useHealth } from "@/hooks/useHealth";

function getStatusLabel(status: "loading" | "connected" | "offline"): string {
  switch (status) {
    case "connected":
      return "🟢 Backend Connected";
    case "offline":
      return "🔴 Backend Offline";
    default:
      return "🟡 Checking backend connection";
  }
}

export function BackendStatus() {
  const { status, responseTimeMs, version, errorMessage, retry } = useHealth();

  return (
    <section className="rounded-2xl border border-white/10 bg-slate-900/70 p-6 shadow-lg backdrop-blur">
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.3em] text-cyan-300">
            Backend status
          </p>
          <h2 className="mt-2 text-2xl font-semibold text-white">{getStatusLabel(status)}</h2>
        </div>

        {status === "offline" ? (
          <button
            type="button"
            onClick={retry}
            className="rounded-full border border-cyan-400/40 bg-cyan-400/10 px-4 py-2 text-sm font-medium text-cyan-100 transition hover:bg-cyan-400/20"
          >
            Retry
          </button>
        ) : null}
      </div>

      <dl className="mt-6 grid gap-4 sm:grid-cols-3">
        <div className="rounded-xl border border-white/10 bg-white/5 p-4">
          <dt className="text-xs uppercase tracking-[0.24em] text-slate-400">Response time</dt>
          <dd className="mt-2 text-lg font-semibold text-white">
            {responseTimeMs === null ? "—" : `${responseTimeMs} ms`}
          </dd>
        </div>

        <div className="rounded-xl border border-white/10 bg-white/5 p-4">
          <dt className="text-xs uppercase tracking-[0.24em] text-slate-400">Backend version</dt>
          <dd className="mt-2 text-lg font-semibold text-white">{version ?? "n/a"}</dd>
        </div>

        <div className="rounded-xl border border-white/10 bg-white/5 p-4">
          <dt className="text-xs uppercase tracking-[0.24em] text-slate-400">State</dt>
          <dd className="mt-2 text-lg font-semibold text-white">{status}</dd>
        </div>
      </dl>

      {errorMessage ? (
        <p className="mt-4 rounded-xl border border-rose-400/30 bg-rose-500/10 px-4 py-3 text-sm text-rose-100">
          {errorMessage}
        </p>
      ) : null}
    </section>
  );
}
