import pdfplumber
from docx import Document
from app.services.hf_llm_featherless import call_mistral_featherless
import os
from dotenv import load_dotenv

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

PROMPT_TEMPLATE = """
You are an assistant helping summarize research protocols or SOPs for mental health projects.

Start with a brief 20-word summary of the protocol’s purpose.

Then extract and structure the following:

1. Title
2. Objective
3. Study Design (arms, duration, measurements)
4. Primary and Secondary Outcomes
5. Sample Size
6. Version Number (if available)
7. Checklist Items mentioned (if it's an SOP)

Here is the document content:
{document_text}

Return your output in clear bullet format.
"""

def extract_text_from_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        return "\n".join([p.extract_text() for p in pdf.pages if p.extract_text()])

def extract_text_from_docx(file_path):
    doc = Document(file_path)
    return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])

def query_llm(document_text: str):
    prompt = PROMPT_TEMPLATE.format(document_text=document_text[:4000])
    return call_mistral_featherless(prompt, HF_TOKEN)