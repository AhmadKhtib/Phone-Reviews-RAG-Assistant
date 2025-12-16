# Phone Reviews RAG Assistant – Project Report

## 1. Overview

This project implements a **Retrieval-Augmented Generation (RAG)** system that answers mobile-phone questions using **real user reviews** and structured metadata.

The application uses **LangChain**, **OpenAI models**, **ChromaDB** for semantic retrieval, and **Streamlit** for the user interface.

---

## 2. Problem Statement

Consumers face information overload when choosing smartphones. Reviews are scattered, lengthy, and often contradictory.

The challenge was to extract value from unstructured reviews while ensuring factual consistency and preventing hallucinations.

---

## 3. Dataset

A cleaned CSV dataset containing textual reviews and numeric metadata such as:

- brand
- model
- price (USD)
- overall rating
- camera rating
- battery life rating
- performance rating
- display rating
- sentiment

The dataset is stored locally and **not committed to GitHub** for licensing and size reasons.

---

## 4. System Architecture

The system follows a modular RAG pipeline:

1. **Data Ingestion** – Load and clean CSV reviews  
2. **Embedding Generation** – Convert reviews into vector embeddings  
3. **Vector Storage** – Persist embeddings in ChromaDB  
4. **Semantic Retrieval** – Retrieve top-K relevant reviews  
5. **Prompt Grounding** – Inject retrieved context into prompts  
6. **LLM Generation** – Generate grounded answers  
7. **UI Rendering** – Display chat, sources, and controls via Streamlit  

---

## 5. RAG Strategy

Key design decisions:

- Fixed Top-K retrieval for deterministic behavior  
- Strict grounding to retrieved reviews only  
- Metadata-aware reasoning (price, ratings, sentiment)  
- Deduplication by `(brand + model)`  
- Explicit refusal when information is insufficient  

---

## 6. User Interface

The Streamlit-based UI provides:

- Chat-style interaction
- Expandable sources per response
- Sidebar controls (Show sources, Clear chat)
- Clean, distraction-free layout

---

## 7. Installation & Setup

### 7.1 Requirements

- Python **3.10+**
- OpenAI API key

### 7.2 Environment Setup

Create and activate a virtual environment:

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 7.3 Environment Variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_openai_key_here
```

> `.env` is ignored by Git and must not be committed.

---

## 8. Running the Project

### 8.1 Build Vector Store (First Run)

```bash
python src/vectorizer.py
```

This generates embeddings and initializes the local Chroma database.

### 8.2 Launch the Application

```bash
streamlit run UI.py
```

---

## 9. Limitations

- Not a global product catalog
- No external APIs or live pricing
- Answers limited to dataset coverage

---

## 10. Conclusion

This project demonstrates how **structured review data + RAG** can produce reliable, explainable AI systems.

It serves as both:
- a practical consumer-assistance tool
- a technical demonstration of production-style RAG pipelines
