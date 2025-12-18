# Mobile Review Intelligence  
**Phone Reviews RAG Assistant**  
· LangChain · ChromaDB · OpenAI

A **Retrieval-Augmented Generation (RAG)** application that answers smartphone-related questions **strictly using real user reviews and structured metadata**.

The system embeds a cleaned CSV dataset of mobile reviews into a vector database and generates **grounded, explainable answers** through a modern chat interface — without relying on external product APIs or speculative knowledge.

---

## Overview

Choosing a smartphone often requires:
- watching long review videos,
- manually comparing specifications,
- resolving conflicting opinions across sources.

This project simplifies that process by enabling users to ask **natural-language questions** and receive answers based **only on real user reviews**, not marketing material or hallucinated specifications.

The system is designed for **decision support**, not as a replacement for professional reviewers.

---

## Technical Highlights

This project demonstrates how a **single structured CSV dataset** can be transformed into an interactive AI system using:

- semantic embeddings,
- vector search,
- metadata-aware retrieval,
- strict prompt constraints to reduce hallucinations.

It showcases a practical, production-style RAG pipeline without fine-tuning or recommendation engines.

---

## Key Features

- 🔍 Semantic search over phone reviews (ChromaDB)
- 📊 Metadata-aware responses (price, rating, camera, battery, performance, display)
- 🧠 Hallucination-resistant answers (context-only generation)
- ❌ Explicit refusal when information is insufficient
- 💬 Streamlit-based chat interface
- 🧭 Sidebar controls:
  - Toggle source visibility
  - Clear conversation
- ♻️ Persistent local vector database

---
