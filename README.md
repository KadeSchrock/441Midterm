# 441Midterm

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

# AI Usage:
- Used Deepseek harness with local model (Qwen3.8-27B-UD-Q4_K_M.gguf) for some PySide6 UI work
- Chat GPT standard web chat for some of the PySide6 work as well

# NOTES:
### Anything denoted with <NOTE:> before it in a comment indicates that it is a temporary hardcoded(ish) solution to make it simnpler to get a demo up and running