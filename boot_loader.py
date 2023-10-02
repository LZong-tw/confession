import subprocess
import win32gui

hwnd = win32gui.GetForegroundWindow()  # Get handle to the current window

# Set AppUserModelID for the window
win32gui.SetProp(hwnd, "AppUserModelID", "Confession.Bootloader")
subprocess.run(['python', 'main.py'], check=True)