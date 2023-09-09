from fpdf import FPDF  # for pdf creation
import win32print
import win32api


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


# def AddCustomPaperSize(str_width_mm, str_height_mm, printer_name='PDF24', level=2):
#     width_mm = int(str_width_mm if isinstance(str_width_mm, str) and str_width_mm.isdigit() else 0)
#     height_mm = int(str_height_mm if isinstance(str_height_mm, str) and str_height_mm.isdigit() else 0)
#     width_mm = int(height_mm if bool(width_mm > height_mm) else width_mm)
#     height_mm = int(width_mm if bool(width_mm > height_mm) else height_mm)
#     if bool(width_mm > 0 < height_mm):
#         # Get a handle for the default printer
#         device_name = win32print.GetDefaultPrinter()
#         print("Default printer name: " + device_name)
#         format_name = 'CustomSize ' + str(width_mm) + 'x' + str(height_mm)
#         if printer_name != device_name: win32print.SetDefaultPrinter(printer_name)
#         PRINTER_DEFAULTS = {'DesiredAccess': win32print.PRINTER_ALL_ACCESS}
#         width, height = int(float(width_mm * 1000)), int(float(height_mm * 1000))
#         custom_form = ({'Flags': 0, 'Name': format_name, 'Size': {'cx': width, 'cy': height},
#                         'ImageableArea': {'left': 0, 'top': 0, 'right': width, 'bottom': height}})

#         hprinter = win32print.OpenPrinter(device_name, PRINTER_DEFAULTS)
#         if bool(hprinter):
#             try:
#                 win32print.GetForm(hprinter, format_name)
#                 win32print.DeleteForm(hprinter, format_name)
#             except: pass
#             try:
#                 win32print.AddForm(hprinter, custom_form)
#                 attributes = win32print.GetPrinter(hprinter, level)
#                 win32print.SetPrinter(hprinter, level, attributes, 0)
#                 print("Custom paper size: {}x{}".format(width_mm, height_mm))
#                 print("... Script Add custom paper size successfully")
#                 win32print.ClosePrinter(hprinter)
#             except Exception as error:
#                 print(error)

# set up pdf basics:
pdf = newPDF("P", "pt")  # P(ortrait), points size ref, Letter-size paper
pdf.add_page()  # add a blank page to start
pdf.add_font("msjh", "", "微軟正黑體.ttf", 1)
# printer = win32print.GetDefaultPrinterW()
# handle = win32print.OpenPrinter(printer)
# info = win32print.GetPrinter(handle, 2)
# AddCustomPaperSize(24, 30, printer)

pdf.image("top.png", x=None, y=None, w=50, h=15, type="", link="")
pdf.set_font("msjh", size=6)  # optional here, but useful if most text is plain
pdf.write(h=6, txt="\n")
hello_string = (
    "特休斯之船，乃變化與恆常之議。物質持續變換，心靈之船能否仍是原船？我所見，一切物質皆過客，心靈卻永恆。船無非心之外在象徵，而心乃真我，超越時空，永不變異。"
)
pdf.set_font("msjh", size=10)
pdf.write(h=14, txt=hello_string)
pdf.set_font("msjh", size=6)
pdf.write(h=6, txt="\n ")
pdf.image("bottom.png", x=None, y=None, w=50, h=15, type="", link="")
# output the created page(s) as a PDF file
pdf_filename = "hello_world1.pdf"
pdf.output(pdf_filename)
# finally, print the PDF file to the printer
GHOSTSCRIPT_PATH = "C:\\Program Files\\gs\\gs10.01.1\\bin\\gswin64.exe"
GSPRINT_PATH = "C:\\Program Files\\Ghostgum\\gsview\\gsprint.exe"

# YOU CAN PUT HERE THE NAME OF YOUR SPECIFIC PRINTER INSTEAD OF DEFAULT
currentprinter = win32print.GetDefaultPrinter()

win32api.ShellExecute(
    0,
    "open",
    GSPRINT_PATH,
    '-ghostscript "'
    + GHOSTSCRIPT_PATH
    + '" -printer "'
    + currentprinter
    + '" "hello_world1.pdf"',
    ".",
    0,
)
