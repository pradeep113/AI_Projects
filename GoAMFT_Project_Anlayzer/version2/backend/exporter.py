from fpdf import FPDF
import tempfile
import os
import textwrap

def generate_pdf(summary_text):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=10)
    pdf.add_page()

    # Load Unicode font
    font_path = os.path.join(os.path.dirname(__file__), "DejaVuSans.ttf")
    pdf.add_font("DejaVu", "", font_path, uni=True)
    pdf.set_font("DejaVu", size=10)

    pdf.set_left_margin(10)
    pdf.set_right_margin(10)

    max_chars_per_line = 100  # Adjust as needed for your font size and page width

    for line in summary_text.split('\n'):
        # Break long words manually if needed
        safe_line = ' '.join(textwrap.wrap(line, width=max_chars_per_line, break_long_words=True, break_on_hyphens=False))
        try:
            pdf.multi_cell(0, 8, safe_line)
        except RuntimeError:
            pdf.multi_cell(0, 8, "[Rendering error]")

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(temp_file.name)
    return temp_file.name

