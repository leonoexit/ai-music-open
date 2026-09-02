"use client";

import { FormEvent, useEffect, useState } from "react";

type Generation = {
  id: string;
  status: string;
  output_url?: string | null;
  error?: string | null;
};

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export default function Home() {
  const [lyrics, setLyrics] = useState("[Verse]\nWrite your lyrics here...\n\n[Chorus]\nA memorable chorus...");
  const [tags, setTags] = useState("pop, uplifting, piano, female vocal");
  const [generation, setGeneration] = useState<Generation | null>(null);
  const [message, setMessage] = useState("");
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    if (!generation || ["finished", "failed", "canceled", "stopped"].includes(generation.status)) {
      return;
    }

    const timer = window.setInterval(async () => {
      const response = await fetch(`${API_URL}/v1/generations/${generation.id}`);
      if (response.ok) {
        setGeneration(await response.json());
      }
    }, 3000);
    return () => window.clearInterval(timer);
  }, [generation]);

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSubmitting(true);
    setMessage("");
    setGeneration(null);

    try {
      const response = await fetch(`${API_URL}/v1/generations`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          lyrics,
          tags: tags.split(",").map((tag) => tag.trim()).filter(Boolean),
        }),
      });
      if (!response.ok) {
        const body = await response.json();
        throw new Error(body.detail ?? "Could not start generation");
      }
      setGeneration(await response.json());
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "Unexpected error");
    } finally {
      setSubmitting(false);
    }
  }

  const audioUrl = generation?.output_url ? `${API_URL}${generation.output_url}` : null;

  return (
    <main>
      <section className="intro">
        <p className="eyebrow">AI MUSIC OPEN</p>
        <h1>Make music on your own terms.</h1>
        <p className="lede">Run and evaluate open music models without depending on a single provider.</p>
      </section>

      <form onSubmit={submit}>
        <label htmlFor="lyrics">Lyrics</label>
        <textarea id="lyrics" value={lyrics} onChange={(event) => setLyrics(event.target.value)} rows={14} />

        <label htmlFor="tags">Style tags</label>
        <input id="tags" value={tags} onChange={(event) => setTags(event.target.value)} />
        <p className="hint">Separate tags with commas, for example: indie pop, dreamy, synth, female vocal.</p>

        <button disabled={submitting}>{submitting ? "Queuing..." : "Generate song"}</button>
      </form>

      {(generation || message) && (
        <section className="result" aria-live="polite">
          {message && <p className="error">{message}</p>}
          {generation && (
            <>
              <p>Job <code>{generation.id}</code></p>
              <strong>Status: {generation.status}</strong>
              {generation.error && <p className="error">Generation failed. Check the worker logs.</p>}
              {audioUrl && <audio controls src={audioUrl} />}
            </>
          )}
        </section>
      )}
    </main>
  );
}
