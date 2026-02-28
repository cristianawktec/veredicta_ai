import { FormEvent, useState } from "react";

import { uploadDocument } from "../services/api";
import type { UploadResponse } from "../types/dashboard";

type UploadState = {
  file: File | null;
  documentType: "Contrato" | "Sentença" | "Laudo";
  loading: boolean;
  error: string | null;
  result: UploadResponse | null;
};

export default function UploadAnalysis() {
  const [state, setState] = useState<UploadState>({
    file: null,
    documentType: "Contrato",
    loading: false,
    error: null,
    result: null,
  });

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!state.file) {
      setState((current) => ({ ...current, error: "Selecione um PDF para upload." }));
      return;
    }

    setState((current) => ({ ...current, loading: true, error: null, result: null }));

    try {
      const result = await uploadDocument(state.file, state.documentType);
      setState((current) => ({ ...current, loading: false, result }));
    } catch (error) {
      const message = error instanceof Error ? error.message : "Falha no upload";
      setState((current) => ({ ...current, loading: false, error: message }));
    }
  }

  return (
    <section>
      <h2>Upload & Analysis</h2>
      <form className="upload-form" onSubmit={handleSubmit}>
        <label>
          Arquivo PDF
          <input
            type="file"
            accept="application/pdf"
            onChange={(event) => {
              const selected = event.target.files?.[0] ?? null;
              setState((current) => ({ ...current, file: selected, error: null }));
            }}
          />
        </label>

        <label>
          Tipo de documento
          <select
            value={state.documentType}
            onChange={(event) => {
              const selected = event.target.value as UploadState["documentType"];
              setState((current) => ({ ...current, documentType: selected }));
            }}
          >
            <option value="Contrato">Contrato</option>
            <option value="Sentença">Sentença</option>
            <option value="Laudo">Laudo</option>
          </select>
        </label>

        <button type="submit" disabled={state.loading}>
          {state.loading ? "Enviando..." : "Enviar para análise"}
        </button>
      </form>

      {state.error ? <p>Erro: {state.error}</p> : null}

      {state.result ? (
        <div className="result-panel">
          <h3>Resultado da Análise</h3>
          <p>Document ID: {state.result.document_id}</p>
          <p>Case ID: {state.result.case_id}</p>
          <p>Arquivo: {state.result.filename}</p>
          <p>Status: {state.result.status}</p>
          <p>Chunks criados: {state.result.chunks_created}</p>
          <p>Embeddings criados: {String(state.result.embeddings_created)}</p>
        </div>
      ) : null}
    </section>
  );
}
