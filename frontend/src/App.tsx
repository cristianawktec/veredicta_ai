import DashboardOverview from "./components/DashboardOverview";
import UploadAnalysis from "./components/UploadAnalysis";
import { Scale } from "lucide-react";

export default function App() {
  return (
    <main className="min-h-screen bg-muted/30">
      <div className="mx-auto max-w-7xl space-y-6 p-6">
        <header className="rounded-lg border bg-card p-6 shadow-sm">
          <div className="flex items-center gap-3">
            <div className="rounded-md bg-primary/10 p-2 text-primary">
              <Scale className="h-5 w-5" />
            </div>
            <div>
              <h1 className="text-3xl font-bold tracking-tight">Veredicta AI</h1>
              <p className="text-sm text-muted-foreground">Dashboard Jurídico - MVP (Overview + Upload & Analysis)</p>
            </div>
          </div>
        </header>

        <section className="space-y-6">
          <DashboardOverview />
          <UploadAnalysis />
        </section>
      </div>
    </main>
  );
}
