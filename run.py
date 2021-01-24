import os
import jinja2
import pdfkit
import pandas as pd
import numpy as np
# from weasyprint import HTML
# from xhtml2pdf import pisa
from datetime import date

def render_html(row):
    """
    Render html page using jinja based on layout.html
    """
    template_loader = jinja2.FileSystemLoader(searchpath="./")
    template_env = jinja2.Environment(loader=template_loader)
    template_file = "layout.html"
    template = template_env.get_template(template_file)
    output_text = template.render(
        name=row.Name,
        address=row.Address,
        date=get_date(),
        invoice=row.Invoice,
        item=row.Item,
        amount=row.Cost
        )
    # HTML(string=outputText).write_pdf("weasyout.pdf")

    html_path = f'./res/{row.Name}.html'
    html_file = open(html_path, 'w')
    html_file.write(output_text)
    html_file.close()
    print(f"Now converting {row.Name} ... ")
    pdf_path = f'./res/{row.Name}.pdf'    
    html2pdf(html_path, pdf_path)   

def html2pdf(html_path, pdf_path):
    """
    Convert html to pdf using pdfkit which is a wrapper of wkhtmltopdf
    """
    options = {
        'page-size': 'Letter',
        'margin-top': '0.35in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'no-outline': None,
        'enable-local-file-access': None
    }
    with open(html_path) as f:
        pdfkit.from_file(f, pdf_path, options=options)

def get_date():
    "Get today's date in German format"
    today = date.today()
    return today.strftime("%d.%m.%Y")

if __name__ == "__main__":

    df = pd.read_csv('tables/sample.csv')
    for row in df.itertuples():
        render_html(row)