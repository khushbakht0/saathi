type EmailCardProps = {
  subject: string;
  sender: string;
};

export function EmailCard({ subject, sender }: EmailCardProps) {
  return (
    <div className="rounded-xl border border-white/10 bg-slate-900 p-4 text-white">
      <p className="font-semibold">{subject}</p>
      <p className="text-sm text-slate-400">{sender}</p>
    </div>
  );
}
