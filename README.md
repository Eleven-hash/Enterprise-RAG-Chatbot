# 💬 Enterprise RAG Chatbot: Document-Intelligent Conversational System

A production-grade **Retrieval-Augmented Generation (RAG)** conversational system designed to answer user inquiries based strictly and securely on corporate platform documentation. 

Leveraging local state-of-the-art vector embedding technology combined with advanced LLM reasoning, this system acts as a secure, private, and highly explainable knowledge expert for project files, billing plans, integrations, and support guidelines.

---

## 🌟 Core Technical Highlights

1. **🔒 Absolute Data Privacy (Local Embeddings)**: Traditional pipelines stream proprietary business files to public cloud APIs for embedding, posing data privacy risks and incurring subscription costs. This architecture utilizes a **local `BAAI/bge-m3` embedding model** executing entirely on the local device, ensuring zero data leakage and zero API costs for database indexing.
2. **🛡️ Absolute Zero-Hallucination Guardrails**: Standard chatbots are notoriously prone to fabricating realistic-sounding lies. By implementing strict semantic instruction masks inside the prompt templates, the system forces the LLM to rely *exclusively* on the retrieved chunks. If a query falls outside the documented data, the bot safely admits ignorance instead of guessing.
3. **🔍 Explainability & View-Source Auditing**: To build stakeholder trust, the chatbot is equipped with an automated citation compiler. Every factual response generated contains an expander detailing the exact folders, files, and snippets used by the AI brain.
4. **💬 Fully Conversational Memory**: The system features history-aware retrieval. When users ask multi-turn questions, a pre-retriever reformulates casual references into clear, standalone contextual queries before database query extraction.

---

## 🏗️ Architecture Design

```
   [📂 Markdown Docs] ──> [⚙️ DirectoryLoader] ──> [Recursive Splitter]
                                                      │
   [🔍 Cosine Similarity] <── [🗄️ ChromaDB] <── [🧠 Local bge-m3 Embed]
           │
           ├──> [📝 strict Prompt Builder] ──> [🤖 OpenAI gpt-4o-mini]
                                                       │
   [👤 User Chat] <── [💬 Streamlit Web App] <─── [🛠️ Citation Compiler]
```

---

## 📂 Portable Repository Directory Structure

The project features a highly clean, production-grade structure separating knowledge directories, diagnostic code, and validation reports:

```
embedding/
│
├── app.py                      # Main Streamlit Chatbot UI Application
├── rag_pipeline.py             # Document loading, chunking, and database builder
├── test_rag.py                 # Core diagnostic and validation script
├── requirements.txt            # Python dependencies list
├── .gitignore                  # Git exclusion rules (venv, .env, caches)
├── .env.example                # Template for required API keys
├── colab_rag_chatbot.ipynb     # Jupyter notebook for Google Colab environments
│
├── data/                       # Ingested mock knowledge base documents
│   ├── features/               # Task Manager, Time Tracker, AI Copilot
│   ├── integrations/           # Slack Integration, GitHub Sync
│   ├── billing/                # Pricing, Wallet Credits, Cancellation
│   └── support/                # My Profile & email change policy
│
├── reports/                    # Quality assurance & project evaluations
│   ├── project_executive_report.md  # Comprehensive executive evaluation briefing
│   └── rag_test_results.md     # 13-Question accuracy benchmark logs
│
└── chroma_db/                  # The persisted local Vector database (BAAI/bge-m3)
```

---

## 🚀 Quick Start Guide

### 1. Setup Virtual Environment & Install Dependencies
Ensure you have Python 3.9+ installed. Run the following to configure the virtual environment and install standard library dependencies:

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate      # On macOS/Linux
venv\Scripts\activate         # On Windows

# Install required packages
pip install -r requirements.txt
```

### 2. Configure API Keys
1. Copy the template configuration file:
   ```bash
   cp .env.example .env
   ```
2. Open `.env` and fill in your OpenAI API Key (required for LLM reasoning):
   ```env
   OPENAI_API_KEY=sk-proj-yourRealOpenAiKeyHere
   ```

---

## 📊 Ingestion & Running the System

### A. Rebuild the Vector Database
Run the ingestion pipeline to recursively parse, chunk, and embed the mock documentation locally using the `BAAI/bge-m3` embedding model:

```bash
python rag_pipeline.py
```
*Note: This parses the mock documents into semantic chunks, creating a persisted local vector index inside the `chroma_db/` directory.*

### B. Run Diagnostic Verification
To run an instant verification test to make sure the retrieval database and LangChain components are fully aligned and functioning correctly:

```bash
python test_rag.py
```

### C. Launch the Chatbot Application
Launch the highly responsive Streamlit web interface to chat with the system:

```bash
streamlit run app.py
```
*The Streamlit server will start and open your browser automatically. You can query the assistant and see exact source documentation references on every response.*

---

## 📈 Quality Assurance Scorecard

The chatbot's strict guardrails and negative controls were rigorously validated against a **13-Question Evaluation Suite** (covering factual calculations, complex multi-hop answers, and out-of-scope hallucination attempts), achieving a **100% Pass Rate**. 

All logs are stored in `reports/rag_test_results.md` and detailed business benefits are located in `reports/project_executive_report.md`.
