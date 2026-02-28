export type HealthResponse = {
  status: string;
  service: string;
};

export type MetricsResponse = {
  service: string;
  timestamp: string;
  latency_ms: number | null;
  requests_count: number;
  avg_confidence_score: number | null;
};

export type UploadResponse = {
  document_id: string;
  case_id: string;
  filename: string;
  status: string;
  chunks_created: number;
  embeddings_created: boolean;
};
