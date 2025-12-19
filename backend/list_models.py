import google.generativeai as genai
import os

# Manually load key from backend/.env for strict isolation
key = None
with open("backend/.env", "r") as f:
    for line in f:
        if line.startswith("GEMINI_API_KEY="):
            key = line.strip().split("=")[1]
            break

if not key:
    print("No key found in backend/.env")
    exit(1)

genai.configure(api_key=key)

print(f"Checking models for key ending in ...{key[-4:]}")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)
except Exception as e:
    print(f"Error listing models: {e}")
