# 441Midterm
## Purpose
- Semantic search engine with AI summary capabilities
- Built as a mini personal search engine where you control the data that goes in

## Project Overview
- Kade developed the backend qdrant searching and webscraping
- Nick developed the PySide front end
- All planning was done together over discord
- Some co-programming to integrate backend into frontend

## How to run
- git clone https://github.com/KadeSchrock/441Midterm.git
- Install UV
- WINDOWS: powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
- LINUX: curl -LsSf https://astral.sh/uv/install.sh | sh
- uv sync
- activate .venv if it didn't for you
- uv run main.py ()

# Sources
## All Qdrant Related Links: 
- https://github.com/qdrant/qdrant-client
- https://qdrant.tech/course/beginners/module-2/chunking-strategies/
- https://qdrant.tech/documentation/
## WebScrape Code: 
- Chunking: https://docs.langchain.com/oss/python/integrations/splitters
- Text Extraction: https://trafilatura.readthedocs.io/en/latest/quickstart.html
## Google AI:
- [](https://ai.google.dev/gemini-api/docs/generate-content/get-started)

# AI Usage:
- Used Deepseek harness with local model (Qwen3.8-27B-UD-Q4_K_M.gguf) for some PySide6 UI work
- Chat GPT standard web chat for some of the PySide6 work as well
