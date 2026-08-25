import os
from backend.parser.extractor import extract_tender_intelligence
from backend.generator.doc_generator import generate_compliance_sheet

def run_local_test():
    print("🚀 Initializing TenderPilot Local Pipeline Test...")
    
    # 1. Ensure output and data directories exist
    os.makedirs("./outputs", exist_ok=True)
    os.makedirs("./data", exist_ok=True)
    
    # Path for a sample PDF (place any test tender PDF in ./data/sample_tender.pdf)
    sample_pdf = "./data/sample_tender.pdf"
    
    if not os.path.exists(sample_pdf):
        print(f"⚠️ Warning: Sample PDF not found at {sample_pdf}.")
        print("Please drop a sample tender PDF into the './data/' folder named 'sample_tender.pdf' to test extraction.")
        print("Skipping AI extraction step, testing Document Generator directly...")
        
        # Test Document Generator directly
        doc_path = generate_compliance_sheet(bid_id="GEM/2026/B/TEST1234", company_name="Arif Solar Contractors")
        print(f"✅ Sample compliance document successfully generated at: {doc_path}")
        return

    print(f"📄 Processing tender PDF: {sample_pdf}...")
    try:
        # Run DeepSeek-R1 Extraction
        intelligence = extract_tender_intelligence(sample_pdf)
        print("📊 Extraction Successful! Risk Matrix Result:")
        print(intelligence)
        
        # Extract Bid ID or fallback
        bid_id = intelligence.get("tender_metadata", {}).get("bid_number", "GEM/2026/B/8924156")
        
        # Generate Compliance Doc
        doc_path = generate_compliance_sheet(bid_id=bid_id, company_name="Arif Solar Contractors")
        print(f"✅ Compliance document successfully generated at: {doc_path}")
        
    except Exception as e:
        print(f"❌ Pipeline execution error: {e}")

if __name__ == "__main__":
    run_local_test()
