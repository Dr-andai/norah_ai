import nbformat
from app.services.hf_llm_featherless import call_mistral_featherless
import os
from dotenv import load_dotenv

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

NOTEBOOK_WITH_SOP_PROMPT = """
You are Norah AI, a smart assistant reviewing a data analysis notebook.

First, here is the SOP context describing how the data was collected and structured:
"""
{context_from_sop}
"""

Now, here is the analysis script:
"""
{notebook_text}
"""

Please summarize the following:
1. What type of analysis is performed? (e.g., EDA, modeling)
2. Which variables or outcomes are being studied?
3. Are any models or statistical methods used?
4. What key insights or outputs were generated?
5. Does the analysis appear to align with how the data was collected per the SOP?

Return your answer in structured bullet points.
"""

def extract_notebook_text(file_path):
    nb = nbformat.read(file_path, as_version=4)
    content = []

    for cell in nb.cells:
        if cell.cell_type in ["markdown", "code"]:
            content.append(cell.source.strip())

    return "\n\n".join(content)

def summarize_notebook_with_llm(notebook_text, sop_context):
    prompt = NOTEBOOK_WITH_SOP_PROMPT.format(
        notebook_text=notebook_text[:3000],
        context_from_sop=sop_context[:1000]
    )
    return call_mistral_featherless(prompt, HF_TOKEN)