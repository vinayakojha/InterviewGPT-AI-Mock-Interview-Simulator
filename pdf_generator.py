from fpdf import FPDF

def generate_pdf(content):

    pdf = FPDF()

    pdf.add_page()

    pdf.set_font(
        "Arial",
        size=12
    )

    content = content.encode(
        "latin-1",
        "replace"
    ).decode(
        "latin-1"
    )

    pdf.multi_cell(
        0,
        10,
        content
    )

    file_name = "Interview_Report.pdf"

    pdf.output(
        file_name
    )

    return file_name