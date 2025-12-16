import { useEffect, useMemo, useRef, useState } from "react";

const API_BASE = import.meta.env.VITE_API_BASE;

const SUGGESTED = [
  "Galaxy S24 battery issues?",
  "Best phone under $500 for battery life",
  "Common camera complaints for iPhone 15",
  "Is the Pixel 8 overheating? What do reviews say?",
  "Best value phone with good performance",
];

function nowTime() {
  const d = new Date();
  return d.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}

function clampSources(sources) {
  return Array.isArray(sources) ? sources : [];
}

function safeText(v) {
  return typeof v === "string" ? v : "";
}

function persistTheme(theme) {
  try {
    localStorage.setItem("theme", theme);
  } catch {}
}

function readTheme() {
  try {
    return localStorage.getItem("theme");
  } catch {
    return null;
  }
}

export default function App() {
  const [theme, setTheme] = useState(() => readTheme() || "dark");
  const [draft, setDraft] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [expandedSources, setExpandedSources] = useState(() => new Set());

  const [messages, setMessages] = useState(() => [
    {
      id: crypto.randomUUID(),
      role: "assistant",
      time: nowTime(),
      text:
        "Ask me anything about phone reviews.\n\nExamples:\n• Galaxy S24 battery issues?\n• Best phone under $500 for battery?\n• iPhone 15 camera complaints?",
      sources: [],
    },
  ]);

  const bottomRef = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
    persistTheme(theme);
  }, [theme]);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, busy]);

  const canSend = useMemo(() => draft.trim().length > 0 && !busy, [draft, busy]);

  function toggleTheme() {
    setTheme((t) => (t === "dark" ? "light" : "dark"));
  }

  function resetChat() {
    setMessages([
      {
        id: crypto.randomUUID(),
        role: "assistant",
        time: nowTime(),
        text:
          "Ask me anything about phone reviews.\n\nExamples:\n• Galaxy S24 battery issues?\n• Best phone under $500 for battery?\n• iPhone 15 camera complaints?",
        sources: [],
      },
    ]);
    setDraft("");
    setError("");
    setBusy(false);
    setExpandedSources(new Set());
    setTimeout(() => inputRef.current?.focus(), 0);
  }

  function insertPrompt(p) {
    setDraft(p);
    setTimeout(() => inputRef.current?.focus(), 0);
  }

  function toggleSources(messageId) {
    setExpandedSources((prev) => {
      const next = new Set(prev);
      if (next.has(messageId)) next.delete(messageId);
      else next.add(messageId);
      return next;
    });
  }

  async function copyToClipboard(text) {
    try {
      await navigator.clipboard.writeText(text);
      return true;
    } catch {
      return false;
    }
  }

  async function sendMessage(userText) {
    setError("");
    const clean = userText.trim();
    if (!clean) return;

    const userMsg = {
      id: crypto.randomUUID(),
      role: "user",
      time: nowTime(),
      text: clean,
      sources: [],
    };

    setMessages((m) => [...m, userMsg]);
    setBusy(true);

    try {
      const res = await fetch(`${API_BASE}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: clean }),
      });

      if (!res.ok) {
        const t = await res.text();
        throw new Error(`API error ${res.status}: ${t}`);
      }

      const data = await res.json();
      const answer = safeText(data?.answer);
      const sources = clampSources(data?.sources);

      const assistantMsg = {
        id: crypto.randomUUID(),
        role: "assistant",
        time: nowTime(),
        text: answer || "No answer returned.",
        sources,
      };

      setMessages((m) => [...m, assistantMsg]);
    } catch (err) {
      setError(err?.message || "Request failed");
    } finally {
      setBusy(false);
    }
  }

  function onSubmit(e) {
    e.preventDefault();
    if (!canSend) return;
    const toSend = draft;
    setDraft("");
    sendMessage(toSend);
  }

  function onKeyDown(e) {
    // Enter sends, Shift+Enter adds newline
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      if (canSend) {
        const toSend = draft;
        setDraft("");
        sendMessage(toSend);
      }
    }
  }

  return (
    <div className="appShell">
      <header className="topBar">
        <div className="brand">
          <div className="logo">PR</div>
          <div className="brandText">
            <div className="title">Phone Reviews Assistant</div>
            <div className="subtitle">Chatbot grounded in real review snippets (RAG)</div>
          </div>
        </div>

        <div className="actions">
          <button className="ghostBtn" onClick={toggleTheme} type="button">
            {theme === "dark" ? "Light" : "Dark"}
          </button>
          <button className="ghostBtn" onClick={resetChat} type="button">
            New chat
          </button>
        </div>
      </header>

      <main className="mainGrid single">
        <section className="chatCard">
          <div className="chatHeader">
            <div className="pill">
              <span className={busy ? "dot dotOn" : "dot"} />
              {busy ? "Thinking…" : "Ready"}
            </div>

            <div className="hint">
              Enter to send • Shift+Enter new line • Use constraints like “under $500”
            </div>
          </div>

          <div className="chatBody">
            {messages.map((m) => {
              const isUser = m.role === "user";
              const hasSources = !isUser && Array.isArray(m.sources) && m.sources.length > 0;
              const expanded = expandedSources.has(m.id);

              return (
                <div key={m.id} className={`row ${isUser ? "rowUser" : "rowBot"}`}>
                  <div className={`bubble ${isUser ? "bubbleUser" : "bubbleBot"}`}>
                    <div className="meta">
                      <span className="who">{isUser ? "You" : "Assistant"}</span>
                      <span className="time">{m.time}</span>
                    </div>

                    <div className="text">{m.text}</div>

                    {!isUser && (
                      <div className="msgActions">
                        <button
                          className="miniBtn"
                          type="button"
                          onClick={async () => {
                            const ok = await copyToClipboard(m.text);
                            if (!ok) setError("Copy failed (clipboard blocked by browser).");
                          }}
                        >
                          Copy
                        </button>

                        {hasSources && (
                          <button className="miniBtn" type="button" onClick={() => toggleSources(m.id)}>
                            {expanded ? "Hide sources" : `View sources (${m.sources.length})`}
                          </button>
                        )}
                      </div>
                    )}

                    {hasSources && expanded && (
                      <div className="sourcesInline">
                        {m.sources.map((s, idx) => (
                          <div key={idx} className="sourceItem">
                            <div className="sourceTop">
                              <div className="sourceTitle">
                                {(s?.metadata?.brand || "Unknown") + " " + (s?.metadata?.model || "")}
                              </div>
                              <div className="sourceBadges">
                                {typeof s?.metadata?.rating !== "undefined" && (
                                  <span className="badge">rating {s.metadata.rating}</span>
                                )}
                                {typeof s?.metadata?.battery_life_rating !== "undefined" && (
                                  <span className="badge">battery {s.metadata.battery_life_rating}</span>
                                )}
                                {s?.metadata?.sentiment && <span className="badge">{s.metadata.sentiment}</span>}
                              </div>
                            </div>
                            <div className="sourceSnippet">{s?.snippet}</div>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              );
            })}

            {busy && (
              <div className="row rowBot">
                <div className="bubble bubbleBot">
                  <div className="meta">
                    <span className="who">Assistant</span>
                    <span className="time">{nowTime()}</span>
                  </div>
                  <div className="typing">
                    <span className="b" />
                    <span className="b" />
                    <span className="b" />
                  </div>
                </div>
              </div>
            )}

            <div ref={bottomRef} />
          </div>

          {error && (
            <div className="errorBox">
              <b>Error:</b> {error}
            </div>
          )}

          <div className="chipsRow">
            {SUGGESTED.map((p) => (
              <button key={p} className="chip" type="button" onClick={() => insertPrompt(p)} disabled={busy}>
                {p}
              </button>
            ))}
          </div>

          <form className="chatInput" onSubmit={onSubmit}>
            <textarea
              ref={inputRef}
              className="input textarea"
              value={draft}
              onChange={(e) => setDraft(e.target.value)}
              onKeyDown={onKeyDown}
              placeholder="Type your question…"
              disabled={busy}
              rows={1}
            />
            <button className="sendBtn" type="submit" disabled={!canSend}>
              Send
            </button>
          </form>
        </section>
      </main>
    </div>
  );
}
