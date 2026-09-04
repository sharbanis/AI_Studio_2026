"""
Groq Model Discovery - Find available models
"""

import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('GROQ_API_KEY')

if not api_key:
    print("Missing GROQ_API_KEY")
    exit(1)

try:
    from groq import Groq
    client = Groq(api_key=api_key)
    
    # Try to list models
    try:
        models = client.models.list()
        print("Available Groq Models:")
        for model in models.data:
            print(f"  - {model.id}")
    except Exception as e:
        print(f"Could not list models: {e}")
        print("\nTrying direct API call...")
        
        # Fallback: Try common model names
        test_models = [
            "gemma-7b-it",
            "llama2-70b-4096",
            "mixtral-8x7b-32768",
            "llama-3.1-70b-versatile",
            "llama-3.2-90b-vision-preview",
            "llama-3.2-1b-preview"
        ]
        
        print("Testing model availability:")
        for model_name in test_models:
            try:
                response = client.chat.completions.create(
                    messages=[{"role": "user", "content": "test"}],
                    model=model_name,
                    max_tokens=1
                )
                print(f"  ✅ {model_name} - AVAILABLE")
                break
            except Exception as model_error:
                error_msg = str(model_error)
                if "decommissioned" in error_msg:
                    print(f"  ❌ {model_name} - DECOMMISSIONED")
                elif "not found" in error_msg or "does not exist" in error_msg:
                    print(f"  ❌ {model_name} - NOT FOUND")
                else:
                    print(f"  ❌ {model_name} - ERROR: {error_msg[:60]}")
        
except ImportError:
    print("Groq library not installed")
