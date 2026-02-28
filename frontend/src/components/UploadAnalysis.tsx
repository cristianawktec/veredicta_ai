import { FormEvent, useState } from "react";

import { Button } from "./ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Input } from "./ui/input";
import { Label } from "./ui/label";
import { Select } from "./ui/select";
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
    <section className="space-y-4">
      <div>
        <h2 className="text-xl font-semibold">Upload & Analysis</h2>
        <p className="text-sm text-muted-foreground">Envie um PDF para processar e visualizar um resumo da análise.</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Novo Documento</CardTitle>
        </CardHeader>
        <CardContent>
          <form className="grid gap-4" onSubmit={handleSubmit}>
            <div className="grid gap-2">
              <Label htmlFor="pdf-file">Arquivo PDF</Label>
              <Input
                id="pdf-file"
                type="file"
                accept="application/pdf"
                onChange={(event) => {
                  const selected = event.target.files?.[0] ?? null;
                  setState((current) => ({ ...current, file: selected, error: null }));
                }}
              />
            </div>

            <div className="grid gap-2">
              <Label htmlFor="analysis-type">Tipo de análise</Label>
              <Select
                id="analysis-type"
                value={state.documentType}
                onChange={(event) => setState((current) => ({ ...current, documentType: event.target.value as UploadState["documentType"] }))}
              >
                <option value="Contrato">Contrato</option>
                <option value="Sentença">Sentença</option>
                <option value="Laudo">Laudo</option>
              </Select>
            </div>

            <Button type="submit" disabled={state.loading}>
              {state.loading ? "Analisando..." : "Enviar PDF"}
            </Button>
          </form>
        </CardContent>
      </Card>

      {state.error && (
        <Card>
          <CardContent className="pt-6">
            <p className="text-sm text-red-600">{state.error}</p>
          </CardContent>
        </Card>
      )}

      {state.result && (
        <Card>
          <CardHeader>
            <CardTitle>Resultado da análise</CardTitle>
          </CardHeader>
          <CardContent className="space-y-2">
            <p className="text-sm">
              <span className="font-semibold">ID:</span> {state.result.document_id}
            </p>
            <p className="text-sm">
              <span className="font-semibold">Tipo:</span> {state.result.case_id}
            </p>
            <p className="text-sm">
              <span className="font-semibold">Arquivo:</span> {state.result.filename}
            </p>
            <p className="text-sm">
              <span className="font-semibold">Status:</span> {state.result.status}
            </p>
            <p className="text-sm">
              <span className="font-semibold">Chunks criados:</span> {state.result.chunks_created}
            </p>
            <p className="text-sm">
              <span className="font-semibold">Embeddings criados:</span> {String(state.result.embeddings_created)}
            </p>
          </CardContent>
        </Card>
      )}
    </section>
  );
}
