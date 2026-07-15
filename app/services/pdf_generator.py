import re
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak

PAGE_W, PAGE_H = A4
MARGIN = 18 * mm
CONTENT_W = PAGE_W - 2 * MARGIN

def p(text, style):
    return Paragraph(text, style)

# Custom Styles
body = ParagraphStyle("pdf_body", fontName="Helvetica", fontSize=10.4, leading=14.5, spaceAfter=8)
body_bold = ParagraphStyle("pdf_body_bold", parent=body, fontName="Helvetica-Bold")
title = ParagraphStyle("pdf_title", fontName="Helvetica-Bold", fontSize=16, leading=20, alignment=TA_CENTER, textColor=colors.HexColor("#1158e9"))
subtitle = ParagraphStyle("pdf_subtitle", fontName="Helvetica", fontSize=11, leading=14, alignment=TA_CENTER, textColor=colors.HexColor("#555555"))
section_title = ParagraphStyle("pdf_section", fontName="Helvetica-Bold", fontSize=12, leading=15, textColor=colors.HexColor("#0f172a"), spaceBefore=10, spaceAfter=6)
analogy_style = ParagraphStyle("pdf_analogy", fontName="Helvetica-Oblique", fontSize=10, leading=13.5, textColor=colors.HexColor("#1e3a8a"))
highlight_style = ParagraphStyle("pdf_highlight", parent=body, fontSize=9.8, leading=13)
quiz_q = ParagraphStyle("pdf_quiz_q", fontName="Helvetica-Bold", fontSize=10.5, leading=14, spaceBefore=8, spaceAfter=4)
quiz_opt = ParagraphStyle("pdf_quiz_opt", fontName="Helvetica", fontSize=10, leading=13, leftIndent=15, spaceAfter=3)

def draw_header(canvas, doc):
    """
    Draws the official SmartBridge / Skill Wallet template header on every page.
    """
    canvas.saveState()
    # Left Brand Mark
    canvas.setFont("Helvetica", 15)
    canvas.setFillColor(colors.HexColor("#444444"))
    canvas.drawString(MARGIN + 8 * mm, PAGE_H - 17 * mm, "SMARTBRIDGE")
    canvas.setFont("Helvetica", 5.6)
    canvas.setFillColor(colors.HexColor("#0089d1"))
    canvas.drawRightString(MARGIN + 42 * mm, PAGE_H - 21 * mm, "Let's Bridge the Gap")
    
    # Decorative Arc lines
    canvas.setLineWidth(1.4)
    canvas.setStrokeColor(colors.HexColor("#ef3030"))
    canvas.arc(MARGIN - 2 * mm, PAGE_H - 24 * mm, MARGIN + 11 * mm, PAGE_H - 14 * mm, 200, 125)
    canvas.setStrokeColor(colors.HexColor("#9acb38"))
    canvas.arc(MARGIN + 3 * mm, PAGE_H - 19 * mm, MARGIN + 14 * mm, PAGE_H - 9 * mm, 15, 130)
    canvas.setStrokeColor(colors.HexColor("#0089d1"))
    canvas.arc(MARGIN + 8 * mm, PAGE_H - 29 * mm, MARGIN + 15 * mm, PAGE_H - 15 * mm, 295, 130)
    
    # Right Brand Mark
    right = PAGE_W - MARGIN
    canvas.setFont("Helvetica-Bold", 18)
    canvas.setFillColor(colors.black)
    canvas.drawRightString(right - 2 * mm, PAGE_H - 13 * mm, "SKILL")
    canvas.setFillColor(colors.HexColor("#1158e9"))
    canvas.drawRightString(right - 2 * mm, PAGE_H - 19 * mm, "WALLET")
    canvas.setFont("Helvetica", 6.8)
    canvas.setFillColor(colors.HexColor("#555555"))
    canvas.drawRightString(right - 2 * mm, PAGE_H - 23 * mm, "A SmartBridge Product")
    
    # Footer Page Numbering (optional helper line)
    canvas.setStrokeColor(colors.HexColor("#cccccc"))
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN, 15 * mm, PAGE_W - MARGIN, 15 * mm)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#777777"))
    canvas.drawCentredString(PAGE_W / 2.0, 10 * mm, f"Page {doc.page}")
    canvas.restoreState()

def clean_markdown_to_html(text: str) -> str:
    """
    Translates simple markdown constructs into ReportLab-compatible HTML tags.
    """
    # Replace headers
    text = re.sub(r'### (.*?)\n', r'<b>\1</b><br/>', text)
    text = re.sub(r'#### (.*?)\n', r'<b>\1</b><br/>', text)
    
    # Replace bold
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    
    # Replace bullets
    text = re.sub(r'^\s*[\*\-]\s*(.*?)$', r'• \1', text, flags=re.MULTILINE)
    
    # Replace newlines with breaks
    text = text.replace("\n", "<br/>")
    return text

def generate_explanation_pdf(data: dict) -> BytesIO:
    """
    Creates an explanation report PDF.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=26 * mm,
        bottomMargin=18 * mm
    )
    
    story = []
    
    # Header titles
    story.append(p("EduGenie Personalized Study Guide", title))
    story.append(p(f"Topic: {data['topic']} | Level: {data['level']} | Style: {data['style']}", subtitle))
    story.append(Spacer(1, 8 * mm))
    
    # Overview Table
    meta_info = [
        [p("<b>Concept Topic</b>", body_bold), p(data["topic"], body)],
        [p("<b>Learning Level</b>", body_bold), p(data["level"], body)],
        [p("<b>Learning Style</b>", body_bold), p(data["style"], body)]
    ]
    t = Table(meta_info, colWidths=[40 * mm, CONTENT_W - 40 * mm])
    t.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#f8fafc")),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 6 * mm))
    
    # Explanation
    story.append(p("Concept Explanation", section_title))
    html_explanation = clean_markdown_to_html(data["explanation"])
    story.append(p(html_explanation, body))
    story.append(Spacer(1, 4 * mm))
    
    # Analogy (inside a neat boxed callout)
    story.append(p("Creative Analogy & Metaphor", section_title))
    analogy_content = [[p(data["analogies"], analogy_style)]]
    analogy_table = Table(analogy_content, colWidths=[CONTENT_W])
    analogy_table.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#2563eb")),
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#eff6ff")),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
    ]))
    story.append(analogy_table)
    story.append(Spacer(1, 6 * mm))
    
    # Key Highlights
    story.append(p("Key Highlights & Takeaways", section_title))
    for highlight in data.get("key_highlights", []):
        story.append(p(f"• {highlight}", highlight_style))
    story.append(Spacer(1, 4 * mm))
    
    # Study Plan
    story.append(p("Personalized Study Plan", section_title))
    for idx, step in enumerate(data.get("study_plan", []), 1):
        story.append(p(f"<b>{idx}.</b> {step}", highlight_style))
        
    doc.build(story, onFirstPage=draw_header, onLaterPages=draw_header)
    buffer.seek(0)
    return buffer

def generate_quiz_pdf(data: dict) -> BytesIO:
    """
    Creates a practice quiz report PDF containing questions, followed by an answer key.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=26 * mm,
        bottomMargin=18 * mm
    )
    
    story = []
    
    story.append(p("EduGenie Practice Assessment", title))
    story.append(p(f"Assessment Topic: {data['topic']}", subtitle))
    story.append(Spacer(1, 8 * mm))
    
    # Questions
    story.append(p("Multiple Choice Questions", section_title))
    story.append(Spacer(1, 2 * mm))
    
    for idx, q in enumerate(data["questions"], 1):
        story.append(p(f"<b>Q{idx}.</b> {q['question']}", quiz_q))
        for o_idx, opt in enumerate(q["options"]):
            letter = chr(65 + o_idx) # A, B, C, D
            story.append(p(f"({letter}) &nbsp; {opt}", quiz_opt))
        story.append(Spacer(1, 4 * mm))
        
    story.append(PageBreak())
    
    # Answer Key and Explanations
    story.append(p("Answer Key & Explanations", title))
    story.append(Spacer(1, 6 * mm))
    
    for idx, q in enumerate(data["questions"], 1):
        correct_letter = chr(65 + q['correct_index'])
        story.append(p(f"<b>Question {idx} Answer:</b> ({correct_letter})", quiz_q))
        story.append(p(f"<b>Explanation:</b> {q['explanation']}", body))
        story.append(Spacer(1, 4 * mm))
        
    doc.build(story, onFirstPage=draw_header, onLaterPages=draw_header)
    buffer.seek(0)
    return buffer
