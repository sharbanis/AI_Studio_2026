"""
llm_client.py — Generate test cases via Ollama (local) with Groq fallback
"""

import requests
from typing import Optional
from config_store import get_store

class LLMClient:
    def __init__(self):
        """Initialize LLM client."""
        self.store = get_store()
    
    def generate(self, prompt: str) -> Optional[str]:
        """
        Generate test cases using the configured LLM provider.
        Tries the selected provider first, then falls back to the other one.
        Works as long as at least one provider (Ollama or Groq) is available.
        """
        provider = self.store.get("llm_provider", "ollama").lower()

        if provider == "groq":
            result = self._generate_groq(prompt)
            if result is not None:
                return result
            print("Groq unavailable, falling back to Ollama...")
            return self._generate_ollama(prompt)

        # Default to Ollama first
        result = self._generate_ollama(prompt)
        if result is not None:
            return result

        # Fall back to Groq
        print("Ollama unavailable, falling back to Groq...")
        return self._generate_groq(prompt)

    def get_available_provider(self) -> Optional[str]:
        """
        Return the best available provider to use for generation.

        Checks the selected provider first, then falls back to the other.
        Returns 'ollama', 'groq', or None if neither is available.
        """
        provider = self.store.get("llm_provider", "ollama").lower()

        if provider == "groq":
            if self.test_groq():
                return "groq"
            if self.test_ollama():
                return "ollama"
            return None

        if self.test_ollama():
            return "ollama"
        if self.test_groq():
            return "groq"
        return None
    
    def _generate_ollama(self, prompt: str) -> Optional[str]:
        """
        Generate test cases using local Ollama instance.
        """
        ollama_url = self.store.get("ollama_url", "http://localhost:11434").strip()
        ollama_model = self.store.get("ollama_model", "gemma3:1b").strip()
        
        if not ollama_url:
            print("ERROR: Ollama URL not configured")
            return None
        
        api_url = f"{ollama_url.rstrip('/')}/api/generate"
        
        payload = {
            "model": ollama_model,
            "prompt": prompt,
            "stream": False,
            "temperature": 0.7,
        }
        
        try:
            print(f"DEBUG: Attempting Ollama connection to {api_url} with model {ollama_model}")
            response = requests.post(api_url, json=payload, timeout=60)
            print(f"DEBUG: Ollama response status code: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                result = data.get("response", "").strip()
                print(f"DEBUG: Ollama generation successful, got {len(result)} chars")
                return result
            else:
                print(f"ERROR: Ollama returned status {response.status_code}: {response.text[:200]}")
                return None
        except requests.exceptions.ConnectionError as e:
            print(f"ERROR: Ollama connection failed at {ollama_url}: {e}")
            return None
        except requests.exceptions.Timeout:
            print(f"ERROR: Ollama request timed out after 60 seconds")
            return None
        except requests.exceptions.RequestException as e:
            print(f"ERROR: Ollama request error: {e}")
            return None
        except Exception as e:
            print(f"ERROR: Unexpected error calling Ollama: {type(e).__name__}: {e}")
            return None
    
    def _generate_groq(self, prompt: str) -> Optional[str]:
        """
        Generate test cases using Groq API (fallback).
        """
        groq_api_key = self.store.get("groq_api_key", "").strip()
        
        if not groq_api_key:
            print("Groq API key not configured")
            return None
        
        try:
            from groq import Groq
        except ImportError:
            print("Groq library not installed. Install with: pip install groq")
            return None
        
        try:
            client = Groq(api_key=groq_api_key)
            message = client.messages.create(
                model="llama-3.1-8b-instant",
                max_tokens=2048,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
            )
            return message.content[0].text if message.content else None
        except Exception as e:
            print(f"Groq error: {e}")
            return None
    
    def test_ollama(self) -> bool:
        """Test if Ollama is available."""
        ollama_url = self.store.get("ollama_url", "http://localhost:11434").strip()
        
        if not ollama_url:
            return False
        
        try:
            response = requests.get(
                f"{ollama_url.rstrip('/')}/api/tags",
                timeout=5
            )
            return response.status_code == 200
        except:
            return False
    
    def test_groq(self) -> bool:
        """Test if Groq API is available."""
        groq_api_key = self.store.get("groq_api_key", "").strip()
        
        if not groq_api_key:
            return False
        
        try:
            from groq import Groq
            client = Groq(api_key=groq_api_key)
            # Simple test call
            message = client.messages.create(
                model="llama-3.1-8b-instant",
                max_tokens=10,
                messages=[
                    {
                        "role": "user",
                        "content": "Say 'OK'",
                    }
                ],
            )
            return bool(message.content)
        except:
            return False

# Global instance
_llm_client = None

def get_llm_client():
    """Get or create the global LLMClient."""
    global _llm_client
    if _llm_client is None:
        _llm_client = LLMClient()
    return _llm_client
