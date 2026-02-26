from docxtpl import DocxTemplate
from app.services.sheets_service import fetch_sheet_data
import os
from datetime import datetime

def generate_documents():
    data_rows = fetch_sheet_data()
    os.makedirs("generated_docs", exist_ok=True)

    for i, row in enumerate(data_rows, start=1):
        doc = DocxTemplate("app/templates/template.docx")
        context = {
            "title": row.get("title", ""),
            "content": row.get("content", ""),
            "points": row.get("points", "")
        }
        doc.render(context)
        filename = f"generated_docs/doc_{i}_{int(datetime.now().timestamp())}.docx"
        doc.save(filename)
        print(f"Saved {filename}")

generate_documents()