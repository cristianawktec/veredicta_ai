import DashboardOverview from "./components/DashboardOverview";
import UploadAnalysis from "./components/UploadAnalysis";

export default function App() {
  return (
    <main className="app-shell">
      <header>
        <h1>Veredicta AI</h1>
        <p>MVP Dashboard - Módulo 1 (Overview)</p>
      </header>

      <DashboardOverview />
      <UploadAnalysis />
    </main>
  );
}
