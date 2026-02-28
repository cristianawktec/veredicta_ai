import { useEffect, useState } from "react";

import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
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
    return (
      <Card>
        <CardHeader>
          <CardTitle>Dashboard Overview</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground">Carregando métricas...</p>
        </CardContent>
      </Card>
    );
  }

  if (state.error) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Dashboard Overview</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-red-600">Erro no Overview: {state.error}</p>
        </CardContent>
      </Card>
    );
  }

  const metrics = state.metrics;
  const health = state.health;

  return (
    <section className="space-y-4">
      <div>
        <h2 className="text-xl font-semibold">Dashboard Overview</h2>
        <p className="text-sm text-muted-foreground">Resumo operacional do backend e métricas iniciais do sistema.</p>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <Card>
          <CardHeader>
            <CardTitle>Status do Serviço</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-2xl font-bold">{health?.status ?? "indisponível"}</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Serviço</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-lg font-semibold">{health?.service ?? "indisponível"}</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Requisições</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-2xl font-bold">{metrics?.requests_count ?? 0}</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Latência Média (ms)</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-2xl font-bold">{metrics?.latency_ms ?? "n/d"}</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Confiança Média</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-2xl font-bold">{metrics?.avg_confidence_score ?? "n/d"}</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Última Atualização</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground break-all">{metrics?.timestamp ?? "n/d"}</p>
          </CardContent>
        </Card>
      </div>
    </section>
  );
}
