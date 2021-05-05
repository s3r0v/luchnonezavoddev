import os

from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.pagesizes import letter
import fitz


class MetricsToPDF:
    def __init__(self, existing_pdf_name="new.pdf", new_pdf_name="dest.pdf", png_name="out.png"):
        self.path = os.path.dirname(os.path.abspath(__file__)) + "/"
        pdfmetrics.registerFont(TTFont('Anton', self.path + 'Anton.ttf'))
        self.existing_pdf_name = self.path + existing_pdf_name
        self.new_pdf_name = self.path + new_pdf_name
        self.png_name = self.path + png_name
        self.can = None 
        self.packet = None

    def make_new_pdf(self, metrics):
        self. packet = io.BytesIO()
        # create a new PDF with Reportlab
        self.can = canvas.Canvas(self.packet, pagesize=letter)
        self.can.setFont('Anton', 120)
        self.add_metrics(metrics=metrics)
        self.can.save()

    def add_metrics(self, metrics):
        metrics = list(map(str, metrics))
        self.can.drawString(800, 410, metrics[0])
        self.can.drawString(800, 230, metrics[1])
        self.can.drawString(800, 50, metrics[2])

    def add_to_existing_pdf(self, new_pdf_name=None):
        #move to the beginning of the StringIO buffer
        self.packet.seek(0)
        new_pdf = PdfFileReader(self.packet)
        # read your existing PDF
        existing_pdf = PdfFileReader(open(self.existing_pdf_name, "rb"))
        output = PdfFileWriter()
        # add the "watermark" (which is the new pdf) on the existing page
        page = existing_pdf.getPage(0)
        page.mergePage(new_pdf.getPage(0))
        output.addPage(page)
        # finally, write "output" to a real file
        new_pdf_name = (self.path + new_pdf_name) if new_pdf_name else self.new_pdf_name
        outputStream = open(new_pdf_name, "wb")
        output.write(outputStream)
        outputStream.close()

    def save_new_pdf_as_png(self, png_name, new_pdf_name):
        # pages = convert_from_path(self.new_pdf_name, 500)
        png_name = self.path + (png_name if png_name else self.png_name)
        new_pdf_name = (self.path + new_pdf_name) if new_pdf_name else self.new_pdf_name
        doc = fitz.open(new_pdf_name)
        page = doc.loadPage(0)  # number of page
        pix = page.getPixmap()
        pix.writePNG(png_name)
        # pages[0].save(self.png_name, 'JPEG')

    def add(self, metrics, new_pdf_name=None):
        self.make_new_pdf(metrics)
        self.add_to_existing_pdf(new_pdf_name)

    def add_as_png(self, metrics, png_name="out.png", new_pdf_name=None):
        self.add(metrics, new_pdf_name)
        self.save_new_pdf_as_png(png_name, new_pdf_name)


if __name__ == "__main__":
    MtoPDF = MetricsToPDF("new.pdf")
    MtoPDF.add_as_png([10, 20, 30])
