import re
import markdown2
from reportlab.platypus import SimpleDocTemplate, Paragraph, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

def convert_markdown_to_pdf(markdown_content):
    # Convert markdown to HTML
    html_content = markdown2.markdown(markdown_content)

    # Create a PDF buffer
    pdf_buffer = BytesIO()
    pdf = SimpleDocTemplate(pdf_buffer)
    
    # Define custom styles
    styles = getSampleStyleSheet()
    # Break content into structured elements
    story = []
    for line in html_content.split("\n"):
        if line.startswith("<h1>") and line.endswith("</h1>"):
            story.append(Paragraph(line[4:-5], styles["Heading1"]))
        elif line.startswith("<h2>") and line.endswith("</h2>"):
            story.append(Paragraph(line[4:-5], styles["Heading2"]))
        elif line.startswith("<ul>"):
            items = re.findall(r"<li>(.*?)</li>", line)
            list_items = [ListItem(Paragraph(item, styles["BodyText"])) for item in items]
            story.append(ListFlowable(list_items, bulletType="bullet"))
        else:
            story.append(Paragraph(line.strip(), styles["BodyText"]))

    # Build the PDF
    pdf.build(story)
    pdf_buffer.seek(0)
    return pdf_buffer

def is_valid_url(url):
    pattern = r"^https://[a-zA-Z0-9\-]+(\.[a-zA-Z0-9\-]+)+.*$"
    return re.match(pattern, url)

def load_markdown(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()
