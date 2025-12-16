import { useMemo, useState } from "react";

const API_BASE = import.meta.env.VITE_API_BASE;

export default function App() {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState([]);
  const [error, setError] = useState("");

  const canSend = useMemo(() => query.trim().length > 0 && !loading, [query, loading]);

  async function onAsk(e) {
    e.preventDefault();
    setError("");
    setAnswer("");
    setSources([]);
    setLoading(true);

    try {
      const res = await fetch(`${API_BASE}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });

      if (!res.ok) {
        const text = await res.text();
        throw new Error(`API error ${res.status}: ${text}`);
      }

      const data = await res.json();
      setAnswer(data.answer || "");
      setSources(Array.isArray(data.sources) ? data.sources : []);
    } catch (err) {
      setError(err?.message || "Request failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ maxWidth: 900, margin: "40px auto", padding: 16, fontFamily: "system-ui, Arial" }}>
      <h1 style={{ marginBottom: 8 }}>Phone Reviews Assistant</h1>
      <p style={{ marginTop: 0, opacity: 0.75 }}>Ask questions and get answers grounded in real review snippets.</p>

      <form onSubmit={onAsk} style={{ display: "flex", gap: 8, marginTop: 16 }}>
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="e.g., Galaxy S24 battery issues?"
          style={{ flex: 1, padding: 12, borderRadius: 10, border: "1px solid #ccc" }}
        />
        <button
          type="submit"
          disabled={!canSend}
          style={{
            padding: "12px 16px",
            borderRadius: 10,
            border: "1px solid #333",
            background: canSend ? "#111" : "#777",
            color: "white",
          }}
        >
          {loading ? "Asking..." : "Ask"}
        </button>
      </form>

      {error && (
        <div style={{ marginTop: 16, padding: 12, borderRadius: 10, background: "#ffe8e8", border: "1px solid #ffb3b3" }}>
          <b>Error:</b> {error}
        </div>
      )}

      {answer && (
        <div style={{ marginTop: 16, padding: 16, borderRadius: 14, border: "1px solid #ddd" }}>
          <h3 style={{ marginTop: 0 }}>Answer</h3>
          <div style={{ whiteSpace: "pre-wrap", lineHeight: 1.5 }}>{answer}</div>
        </div>
      )}

      {sources.length > 0 && (
        <div style={{ marginTop: 16 }}>
          <h3>Sources</h3>
          <div style={{ display: "grid", gap: 10 }}>
            {sources.map((s, idx) => (
              <div key={idx} style={{ padding: 12, borderRadius: 12, border: "1px solid #eee", background: "#fafafa" }}>
                <div style={{ fontSize: 13, opacity: 0.75, marginBottom: 6 }}>
                  {s?.metadata?.brand} {s?.metadata?.model} • rating {s?.metadata?.rating}
                </div>
                <div style={{ whiteSpace: "pre-wrap" }}>{s?.snippet}</div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
