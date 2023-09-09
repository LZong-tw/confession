import win32print
import win32api

GHOSTSCRIPT_PATH = "C:\\Program Files\\gs\\gs10.01.1\\bin\\gswin64.exe"
GSPRINT_PATH = "C:\\Program Files\\Ghostgum\\gsview\\gsprint.exe"

# YOU CAN PUT HERE THE NAME OF YOUR SPECIFIC PRINTER INSTEAD OF DEFAULT
currentprinter = win32print.GetDefaultPrinter()

win32api.ShellExecute(0, 'open', GSPRINT_PATH, '-ghostscript "'+GHOSTSCRIPT_PATH+'" -printer "'+currentprinter+'" "hello_world_Copy.pdf"', '.', 0)