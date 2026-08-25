import os
import json
import fitz  # PyMuPDF
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

def extract_text_with_pages(pdf_path: str) -> str:
    """Extracts text page-by-page from tender PDF with explicit markers."""
    doc = fitz.open(pdf_path)
    full_text = ""
    for page_num, page in enumerate(doc, start=1):
        full_text += f"\n--- PAGE {page_num} ---\n" + page.get_text()
    return full_text

def extract_tender_intelligence(pdf_path: str) -> dict:
    """
    Ingests tender PDF, runs DeepSeek-R1 chain-of-thought extraction,
    and returns a structured disqualification risk matrix.
    """
    tender_text = extract_text_with_pages(pdf_path)
    
    system_prompt = (
        "You are TenderPilot-Engine, an expert Indian Public Procurement Auditor and Legal-Technical Analyst. "
        "Analyze the provided tender document text, extract eligibility criteria, financial thresholds, past experience rules, "
        "and hidden disqualification traps, and return a valid JSON object matching the standard schema."
    )
    
    response = client.chat.completions.create(
        model="deepseek-reasoner",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Analyze this tender document:\n\n{tender_text[:15000]}..."}
        ],
        response_format={"type": "json_object"}
    )
    
    return json.loads(response.choices[0].message.content)
