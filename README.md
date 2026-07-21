# 🎬 AI Video Assistant

An AI-powered meeting/video intelligence tool that takes a **YouTube URL or a local audio/video file**, transcribes it, summarises it, extracts action items and key decisions, and lets you **chat with the transcript** using a Retrieval-Augmented Generation (RAG) pipeline — all wrapped in a Streamlit UI (with a CLI alternative).

---

## Features

- **Flexible input** — paste a YouTube URL or point to a local audio/video file path.
- **Chunked audio processing** — long recordings are split into fixed-length chunks before transcription.
- **Dual transcription engines**
  - `english` → local **OpenAI Whisper** model.
  - `hinglish` → **Sarvam AI** speech-to-text-translate API (handles Hindi/Hinglish audio and returns English text directly).
- **LLM-powered analysis via LangChain LCEL + Mistral**
  - Auto-generated meeting **title**
  - Map-reduce **summary** (chunked → per-chunk summary → combined final summary)
  - **Action items** (task, owner, deadline)
  - **Key decisions**
  - **Open questions / follow-ups**
- **RAG chat** — the transcript is embedded with HuggingFace sentence-transformers and stored in a local **ChromaDB** vector store, so you can ask free-form questions and get answers grounded in the transcript.
- **Streamlit UI** — dark, custom-styled interface with a live pipeline-status sidebar and an in-app chat panel.
- **CLI mode** (`main.py`) — run the full pipeline and chat with the transcript from the terminal.

---

## Architecture

```
YouTube URL / Local File
        │
        ▼
 utils/audio_processor.py   → download (yt-dlp) / convert to WAV → chunk into fixed-length segments
        │
        ▼
 core/transcriber.py        → Whisper (english) or Sarvam AI (hinglish) → full transcript
        │
        ├──► core/summarizer.py   → LangChain LCEL map-reduce chain (Mistral) → title + summary
        │
        ├──► core/extractor.py    → LangChain LCEL chains (Mistral) → action items / decisions / questions
        │
        └──► core/vector_store.py → chunk + HuggingFace embeddings → ChromaDB
                    │
                    ▼
             core/rag_engine.py   → LCEL RAG chain (retriever → Mistral) → chat answers
                    │
                    ▼
              app.py (Streamlit UI)  /  main.py (CLI)
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Audio acquisition | `yt-dlp`, `pydub`, `ffmpeg-python` |
| Transcription | `openai-whisper` (local), Sarvam AI STT-translate API (hinglish) |
| LLM orchestration | `langchain`, `langchain-core`, `langchain-community`, LCEL |
| LLM | `langchain-mistralai` / `mistralai` (`mistral-small-latest`) |
| Embeddings | `langchain-huggingface` (`sentence-transformers`, `all-MiniLM-L6-v2`) |
| Vector store | `langchain-chroma` / `chromadb` |
| UI | `streamlit`, `streamlit-extras` |
| Export libs (included) | `reportlab`, `fpdf2` |
| Config | `python-dotenv` |

---

## Project Structure

```
Video-Ai-Agent/
├── app.py                    # Streamlit UI entry point
├── main.py                   # CLI entry point
├── Requirements.txt          # Python dependencies (note: capital R)
├── core/
│   ├── extractor.py          # Action items / decisions / questions (LCEL + Mistral)
│   ├── rag_engine.py         # RAG chain build + query (LCEL)
│   ├── summarizer.py         # Title + map-reduce summary (LCEL + Mistral)
│   └── vector_store.py       # ChromaDB + HuggingFace embeddings
└── utils/
    └── audio_processor.py    # YouTube download / file conversion / chunking
```

---

## Setup

### 1. Prerequisites

- Python **3.10+**
- `ffmpeg` installed and available on your `PATH` (required by `pydub` / `yt-dlp`)
- A free [Mistral API key](https://console.mistral.ai/)
- A [Sarvam AI API key](https://www.sarvam.ai/) — only required if you plan to use the `hinglish` transcription mode

### 2. Clone & install

```bash
git clone https://github.com/Tanudhillod/Video-Ai-Agent.git
cd Video-Ai-Agent

python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

pip install -r Requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```env
MISTRAL_API_KEY=your_mistral_api_key_here
WHISPER_MODEL=small          # tiny / base / small / medium / large
SARVAM_API_KEY=your_sarvam_api_key_here   # only needed for hinglish mode
SARVAM_STT_MODEL=saaras:v2.5              # optional, defaults shown
```

> ⚠️ **Security note:** never commit a real `.env` file. If a key has already been pushed to the repository, rotate it immediately and remove it from git history — being listed in `.gitignore` does not remove a file that was already committed.

---

## Usage

### Streamlit UI

```bash
streamlit run app.py
```

1. Open the app at `http://localhost:8501`.
2. In the sidebar, paste a **YouTube URL** or a **local file path**.
3. Choose the language mode: `english` (Whisper) or `hinglish` (Sarvam AI).
4. Click **Analyse** and watch the pipeline status (audio → transcript → title → summary → extraction → RAG) update live.
5. Review the generated **summary**, **action items**, **key decisions**, and **open questions**.
6. Use the **chat panel** to ask questions about the meeting — answers are grounded in the transcript via RAG.

### CLI

```bash
python main.py
```

You'll be prompted for a source (YouTube URL or file path) and a language, after which the pipeline runs and prints the title, summary, action items, decisions, and open questions, followed by an interactive chat loop (`exit`/`quit`/`q` to leave).

---

## How It Works (Pipeline Detail)

1. **Input handling** (`utils/audio_processor.py`) — detects whether the input is a URL or local path, downloads/converts it to 16kHz mono WAV, and splits it into 10-minute chunks.
2. **Transcription** (`core/transcriber.py`) — routes each chunk to Whisper (local) or Sarvam AI (splitting into ≤25s pieces to respect the API's 30s limit) based on the selected language.
3. **Title & Summary** (`core/summarizer.py`) — splits the full transcript into ~3000-character chunks, summarises each chunk individually (map step), then combines the partial summaries into one final bullet-point summary (reduce step) using an LCEL chain.
4. **Extraction** (`core/extractor.py`) — three separate LCEL chains prompt Mistral to pull out action items (with owner/deadline), key decisions, and open questions from the full transcript.
5. **RAG indexing** (`core/vector_store.py`) — the transcript is split into 500-character chunks with 50-character overlap, embedded with `all-MiniLM-L6-v2`, and stored in a local ChromaDB collection (`meeting_transcript`).
6. **RAG chat** (`core/rag_engine.py`) — user questions are embedded, the top-4 most similar chunks are retrieved, and an LCEL chain feeds the retrieved context + question to Mistral, which is instructed to only answer from the provided context.

---

## Known Limitations

- No speaker diarisation — the transcript does not distinguish between speakers.
- The `hinglish` mode depends on the third-party Sarvam AI API being available and requires its own API key.
- No persistence of past sessions between runs — each analysis rebuilds a fresh ChromaDB collection in memory for that transcript.
- PDF/TXT export libraries (`reportlab`, `fpdf2`) are included in requirements but not yet wired into `app.py`/`main.py`.

---

