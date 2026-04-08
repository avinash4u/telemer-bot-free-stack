Use Ollama as the free local LLM serving layer.

Example:
```bash
ollama pull llama3.2:3b
curl http://localhost:11434/api/generate -d '{"model":"llama3.2:3b","prompt":"hello","stream":false}'
```
