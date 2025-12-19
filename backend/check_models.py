import os
import google.generativeai as genai
from app.config import get_settings

try:
    settings = get_settings()
    api_key = settings.GEMINI_API_KEY
    print(f"Using API Key: {api_key[:5]}...{api_key[-5:]}")
    
    genai.configure(api_key=api_key)
    
    print("Listing available models...")
    with open("models_out.txt", "w", encoding="utf-8") as f:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"- {m.name}")
                f.write(f"{m.name}\n")
            
except Exception as e:
    print(f"Error: {e}")
