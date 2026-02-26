from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from app.services.sheets_service import fetch_sheet_data
from datetime import datetime
import os


def generate_documents():
    style_rows, content_rows = fetch_sheet_data()

    os.makedirs("generated_docs", exist_ok=True)

    # --------------------------------
    # Convert Sheet1 into style config
    # --------------------------------
    style_config = {}

    for row in style_rows:
        if len(row) >= 3:
            key = row[0]
            style_config[key] = row[1:]

    # Extract margins separately
    margins = style_config.get("Margin", [0.5, 0.5, 0.5, 0.5])

    # --------------------------------
    # Create Document
    # --------------------------------
    doc = Document("app/templates/template.docx")

    # Set margins
    section = doc.sections[0]
    section.top_margin = Inches(float(margins[0]))
    section.bottom_margin = Inches(float(margins[1]))
    section.left_margin = Inches(float(margins[2]))
    section.right_margin = Inches(float(margins[3]))

    for row in content_rows:

        text = row.get("Text", "")

        # Auto replace date placeholder
        if "[Date the file is generated]" in text:
            text = datetime.now().strftime("%B %d, %Y")

        style_name = row.get("Style")
        align_value = row.get("Align", "Left")

        paragraph = doc.add_paragraph(text)

        # Alignment
        if align_value.lower() == "right":
            paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        elif align_value.lower() == "center":
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        else:
            paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT

        # Apply style from Sheet1
        if style_name in style_config:
            font_name = style_config[style_name][0]
            font_size = style_config[style_name][1]

            run = paragraph.runs[0]
            run.font.name = font_name
            run.font.size = Pt(float(font_size))

            # Fix for Times New Roman rendering
            run._element.rPr.rFonts.set(qn('w:eastAsia'), font_name)

        # Line spacing
        if "LineSpacing" in style_config:
            paragraph.paragraph_format.line_spacing = float(style_config["LineSpacing"][0])

    filename = f"generated_docs/document_{int(datetime.now().timestamp())}.docx"
    doc.save(filename)

    return [filename]