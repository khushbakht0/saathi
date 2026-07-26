import { BackendStatus } from "@/components/BackendStatus";

export default function Home() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-slate-950 px-6 py-12 text-white">
      <section className="w-full max-w-4xl rounded-3xl border border-white/10 bg-white/5 p-10 shadow-2xl backdrop-blur">
        <p className="mb-4 text-sm font-semibold uppercase tracking-[0.3em] text-cyan-300">
          Production milestone 1
        </p>
        <h1 className="text-4xl font-bold tracking-tight sm:text-5xl">
          AI Student Assistant
        </h1>
        <p className="mt-4 max-w-2xl text-lg text-slate-300">
          Frontend-to-backend connectivity is now validated through a reusable API client and a typed health-check integration.
        </p>

        <div className="mt-8 flex flex-wrap gap-3">
          <span className="rounded-full bg-cyan-400/15 px-4 py-2 text-sm text-cyan-200">
            Next.js App Router
          </span>
          <span className="rounded-full bg-fuchsia-400/15 px-4 py-2 text-sm text-fuchsia-200">
            TailwindCSS
          </span>
          <span className="rounded-full bg-emerald-400/15 px-4 py-2 text-sm text-emerald-200">
            TypeScript
          </span>
        </div>

        <div className="mt-8">
          <BackendStatus />
        </div>
      </section>
    </main>
  );
}
