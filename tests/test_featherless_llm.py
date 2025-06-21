import os
import sys
from dotenv import load_dotenv

# Ensure the app directory is on the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "app")))

from services.hf_llm_featherless import call_mistral_featherless

# Load .env file
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

# Define a test prompt
prompt = "Summarize the following data process:\nPHQ-9 scores were collected weekly to assess depression symptoms."

def run_test():
    print("📤 Sending prompt to Mistral...")
    response = call_mistral_featherless(prompt, HF_TOKEN)
    print("\n📥 LLM Response:\n", response)

if __name__ == "__main__":
    run_test()