from app.services.hf_llm_featherless import call_mistral_featherless
import os
from dotenv import load_dotenv

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

R_SCRIPT_PROMPT = """
You are Norah AI, a smart assistant reviewing an R script uploaded by a healthcare data scientist.

Please summarize the script by answering:

1. What type of analysis is performed? (e.g., EDA, visualization, modeling)
2. Which variables or outcomes are being analyzed?
3. Are any machine learning or statistical models used?
4. Are any results or insights evident from the script?
5. How well does it align with the expected protocol or SOP?

Here is the R script content:
"""
{r_script_text}
"""

Please return your answer in clear bullet format.
"""

def read_r_script(file_path):
    with open(file_path, "r") as f:
        return f.read()

def summarize_r_script_with_llm(r_script_text):
    prompt = R_SCRIPT_PROMPT.format(r_script_text=r_script_text[:4000])
    return call_mistral_featherless(prompt, HF_TOKEN)