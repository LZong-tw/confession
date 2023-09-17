import time
from fpdf import FPDF  # for pdf creation
import win32print
import win32api
from pydub import AudioSegment


class newPDF(FPDF):
    def __init__(self, orientation="P", unit="mm", format="A4"):
        # Some checks
        self._dochecks()
        # Initialization of properties
        self.offsets = {}  # array of object offsets
        self.page = 0  # current page number
        self.n = 2  # current object number
        self.buffer = ""  # buffer holding in-memory PDF
        self.pages = {}  # array containing pages
        self.orientation_changes = {}  # array indicating orientation changes
        self.state = 0  # current document state
        self.fonts = {}  # array of used fonts
        self.font_files = {}  # array of font files
        self.diffs = {}  # array of encoding differences
        self.images = {}  # array of used images
        self.page_links = {}  # array of links in pages
        self.links = {}  # array of internal links
        self.in_footer = 0  # flag set when processing footer
        self.lastw = 0
        self.lasth = 0  # height of last cell printed
        self.font_family = ""  # current font family
        self.font_style = ""  # current font style
        self.font_size_pt = 12  # current font size in points
        self.underline = 0  # underlining flag
        self.draw_color = "0 G"
        self.fill_color = "0 g"
        self.text_color = "0 g"
        self.color_flag = 0  # indicates whether fill and text colors are different
        self.ws = 0  # word spacing
        self.angle = 0
        # Standard fonts
        self.core_fonts = {
            "courier": "Courier",
            "courierB": "Courier-Bold",
            "courierI": "Courier-Oblique",
            "courierBI": "Courier-BoldOblique",
            "helvetica": "Helvetica",
            "helveticaB": "Helvetica-Bold",
            "helveticaI": "Helvetica-Oblique",
            "helveticaBI": "Helvetica-BoldOblique",
            "times": "Times-Roman",
            "timesB": "Times-Bold",
            "timesI": "Times-Italic",
            "timesBI": "Times-BoldItalic",
            "symbol": "Symbol",
            "zapfdingbats": "ZapfDingbats",
        }
        # Scale factor
        if unit == "pt":
            self.k = 1
        elif unit == "mm":
            self.k = 72 / 25.4
        elif unit == "cm":
            self.k = 72 / 2.54
        elif unit == "in":
            self.k = 72.0
        else:
            self.error("Incorrect unit: " + unit)
        # Page format
        self.fw_pt = 68 * self.k
        self.fh_pt = 150 * self.k
        self.fw = self.fw_pt / self.k
        self.fh = self.fh_pt / self.k
        # Page orientation
        orientation = orientation.lower()
        if orientation == "p" or orientation == "portrait":
            self.def_orientation = "P"
            self.w_pt = self.fw_pt
            self.h_pt = self.fh_pt
        elif orientation == "l" or orientation == "landscape":
            self.def_orientation = "L"
            self.w_pt = self.fh_pt
            self.h_pt = self.fw_pt
        else:
            self.error("Incorrect orientation: " + orientation)
        self.cur_orientation = self.def_orientation
        self.w = self.w_pt / self.k
        self.h = self.h_pt / self.k
        # Page margins (1 cm)
        margin = 0
        self.set_margins(8, 12)
        # Interior cell margin (1 mm)
        self.c_margin = 0
        # line width (0.2 mm)
        self.line_width = 0.567 / self.k
        # Automatic page break
        self.set_auto_page_break(1, 2 * margin)
        # Full width display mode
        self.set_display_mode("fullwidth")
        # Enable compression
        self.set_compression(1)
        # Set default PDF version number
        self.pdf_version = "1.3"

def print_service(print_data_queue, voice_count_queue):
    while True:
        while not print_data_queue.empty():
            the_words = print_data_queue.get()
            print("PRINT following: " + the_words)
            pdf = newPDF("P",
                         "pt")  # P(ortrait), points size ref, Letter-size paper
            pdf.add_page()  # add a blank page to start
            pdf.add_font("msjh", "", "微軟正黑體.ttf", 1)
            pdf.image("assets/top.png", x=None, y=None, w=50, h=15, type="",
                      link="")
            pdf.set_font("msjh",
                         size=2)  # optional here, but useful if most text is plain
            pdf.write(h=2, txt="\n")
            hello_string = the_words
            pdf.set_font("msjh", size=10)
            pdf.write(h=14, txt=hello_string)
            pdf.set_font("msjh", size=10)
            pdf.write(h=10, txt="\n")
            pdf.image("assets/bottom.png", x=None, y=None, w=50, h=15,
                      type="",
                      link="")
            # output the created page(s) as a PDF file
            pdf_filename = "storage/hello_world1.pdf"
            pdf.output(pdf_filename)
            # finally, print the PDF file to the printer
            GHOSTSCRIPT_PATH = "C:\\Program Files\\gs\\gs10.01.1\\bin\\gswin64.exe"
            GSPRINT_PATH = "C:\\Program Files\\Ghostgum\\gsview\\gsprint.exe"

            # YOU CAN PUT HERE THE NAME OF YOUR SPECIFIC PRINTER INSTEAD OF DEFAULT
            current_printer = win32print.GetDefaultPrinter()

            win32api.ShellExecute(
                0,
                "open",
                GSPRINT_PATH,
                '-ghostscript "'
                + GHOSTSCRIPT_PATH
                + '" -printer "'
                + current_printer
                + '" "storage/hello_world1.pdf"',
                ".",
                0,
            )
            break
