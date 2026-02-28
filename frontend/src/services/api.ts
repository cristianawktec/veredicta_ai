import type { HealthResponse, MetricsResponse } from "../types/dashboard";

const BASE_URL = "http://127.0.0.1:8011";

async function request<T>(path: string): Promise<T> {
  const response = await fetch(`${BASE_URL}${path}`);
  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }
  return (await response.json()) as T;
}

export function fetchHealth(): Promise<HealthResponse> {
  return request<HealthResponse>("/health");
}

export function fetchMetrics(): Promise<MetricsResponse> {
  return request<MetricsResponse>("/metrics");
}
