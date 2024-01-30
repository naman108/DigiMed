from enum import Enum

class OllamaPermissions(Enum):
    """Ollama permissions"""
    # Permission to send prompt to an Ollama model
    PROMPT = "ollama-permission-prompt"
