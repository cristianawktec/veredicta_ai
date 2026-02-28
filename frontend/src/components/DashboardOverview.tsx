import { useEffect, useState } from "react";

import { fetchHealth, fetchMetrics } from "../services/api";
import type { HealthResponse, MetricsResponse } from "../types/dashboard";

type OverviewState = {
  health: HealthResponse | null;
  metrics: MetricsResponse | null;
  loading: boolean;
  error: string | null;
};

export default function DashboardOverview() {
  const [state, setState] = useState<OverviewState>({
    health: null,
    metrics: null,
    loading: true,
    error: null,
  });

  useEffect(() => {
    async function loadOverview() {
      try {
        const [health, metrics] = await Promise.all([fetchHealth(), fetchMetrics()]);
        setState({ health, metrics, loading: false, error: null });
      } catch (error) {
        const message = error instanceof Error ? error.message : "Falha ao carregar overview";
        setState({ health: null, metrics: null, loading: false, error: message });
      }
    }

    loadOverview();
  }, []);

  if (state.loading) {
    return <p>Carregando módulo Overview...</p>;
  }

  if (state.error) {
    return <p>Erro no Overview: {state.error}</p>;
  }

  const metrics = state.metrics;
  const health = state.health;

  return (
    <section>
      <h2>Dashboard Overview</h2>
      <div className="cards-grid">
        <article className="card">
          <h3>Status do Serviço</h3>
          <p>{health?.status ?? "indisponível"}</p>
        </article>

        <article className="card">
          <h3>Serviço</h3>
          <p>{health?.service ?? "indisponível"}</p>
        </article>

        <article className="card">
          <h3>Requisições</h3>
          <p>{metrics?.requests_count ?? 0}</p>
        </article>

        <article className="card">
          <h3>Latência Média (ms)</h3>
          <p>{metrics?.latency_ms ?? "n/d"}</p>
        </article>

        <article className="card">
          <h3>Confiança Média</h3>
          <p>{metrics?.avg_confidence_score ?? "n/d"}</p>
        </article>

        <article className="card">
          <h3>Última Atualização</h3>
          <p>{metrics?.timestamp ?? "n/d"}</p>
        </article>
      </div>
    </section>
  );
}
