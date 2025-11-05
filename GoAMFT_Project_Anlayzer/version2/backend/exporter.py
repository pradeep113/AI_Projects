from fpdf import FPDF
import tempfile
import os

def generate_pdf(summary_text):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=10)
    pdf.add_page()

    # Load Unicode font
    font_path = os.path.join(os.path.dirname(__file__), "DejaVuSans.ttf")
    pdf.add_font("DejaVu", "", font_path, uni=True)
    pdf.set_font("DejaVu", size=10)  # Reduce font size to fit wide characters

    # Set left/right margins to allow more horizontal space
    pdf.set_left_margin(10)
    pdf.set_right_margin(10)

    # Safely render each line
    for line in summary_text.split('\n'):
        try:
            pdf.multi_cell(0, 8, line)
        except RuntimeError as e:
            pdf.multi_cell(0, 8, "[Rendering error]")

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(temp_file.name)
    return temp_file.name

