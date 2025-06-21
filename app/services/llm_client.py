# app/services/llm_client.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://router.huggingface.co/featherless-ai/v1/chat/completions"
MODEL_ID = "mistralai/Mistral-7B-Instruct-v0.2"
HF_TOKEN = os.getenv("HF_TOKEN")

def call_mistral_chat(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}"
    }

    payload = {
        "model": MODEL_ID,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]
