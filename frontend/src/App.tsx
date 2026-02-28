import DashboardOverview from "./components/DashboardOverview";

export default function App() {
  return (
    <main className="app-shell">
      <header>
        <h1>Veredicta AI</h1>
        <p>MVP Dashboard - Módulo 1 (Overview)</p>
      </header>

      <DashboardOverview />
    </main>
  );
}
