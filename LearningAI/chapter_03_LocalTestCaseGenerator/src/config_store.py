"""
config_store.py — Manage environment and persisted configuration
Reads .env on startup, allows runtime updates via settings UI, persists to config.json
"""

import os
import json
from pathlib import Path
from dotenv import load_dotenv

CONFIG_FILE = "config.json"

class ConfigStore:
    def __init__(self):
        """Load configuration from .env, then overlay config.json if it exists."""
        self.config = {}
        self._load_env()
        self._load_persisted()
    
    def _load_env(self):
        """Load from .env file."""
        load_dotenv()
        self.config = {
            "jira_url": os.getenv("JIRA_URL", "").strip(),
            "jira_email": os.getenv("JIRA_EMAIL", "").strip(),
            "jira_api_token": os.getenv("JIRA_API_TOKEN", "").strip(),
            "ollama_url": os.getenv("OLLAMA_URL", "http://localhost:11434").strip(),
            "ollama_model": os.getenv("OLLAMA_MODEL", "gemma3:1b").strip(),
            "groq_api_key": os.getenv("GROQ_API_KEY", "").strip(),
            "llm_provider": os.getenv("LLM_PROVIDER", "ollama").strip(),
        }
    
    def _load_persisted(self):
        """Load from config.json, if it exists, to overlay .env values."""
        if Path(CONFIG_FILE).exists():
            try:
                with open(CONFIG_FILE, "r") as f:
                    persisted = json.load(f)
                    self.config.update(persisted)
            except Exception as e:
                print(f"Warning: Could not load {CONFIG_FILE}: {e}")
    
    def get(self, key, default=None):
        """Retrieve a config value."""
        return self.config.get(key, default)
    
    def update(self, updates: dict):
        """Update multiple config values and persist to config.json."""
        self.config.update(updates)
        self._persist()
    
    def _persist(self):
        """Write config to config.json."""
        try:
            with open(CONFIG_FILE, "w") as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Error persisting config: {e}")
    
    def to_dict(self):
        """Return entire config as a dictionary."""
        return self.config.copy()

# Global instance
_store = None

def get_store():
    """Get or create the global ConfigStore."""
    global _store
    if _store is None:
        _store = ConfigStore()
    return _store
