import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QSizePolicy
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pyaudio
from scipy.interpolate import interp1d


class WaveFormApp(QMainWindow):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.setWindowOpacity(0.5)  # 50% transparency
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.stream = None
        self.pAud = pyaudio.PyAudio()
        self.width = QApplication.primaryScreen().size().width()
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.palette = QPalette()
        self.palette.setColor(QPalette.Window, QColor(0, 0, 0))  # Set window background color to black
        self.setPalette(self.palette)
        # Matplotlib Figure and Canvas
        self.fig, self.ax = self.init_matplotlib()
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding) # Set Size Policy to Expanding
        layout.addWidget(self.canvas)

        # Control Buttons
        button_layout = QHBoxLayout()
        self.listen_button = QPushButton('Listen', self)
        self.listen_button.setFixedSize(70, 30)  # Set the size of the button
        self.listen_button.clicked.connect(self.on_listen)
        button_layout.addWidget(self.listen_button)

        self.stop_button = QPushButton('Stop', self)
        self.stop_button.setFixedSize(70, 30)  # Set the size of the button
        self.stop_button.clicked.connect(self.on_stop)
        self.stop_button.setEnabled(False)
        # button_layout.addWidget(self.stop_button)

        self.exit_button = QPushButton('Exit', self)
        self.exit_button.setFixedSize(70, 30)  # Set the size of the button
        self.exit_button.clicked.connect(self.close)
        button_layout.addWidget(self.exit_button)

        button_layout.addStretch(1)
        layout.addLayout(button_layout)

        self.setCentralWidget(central_widget)
        self.setWindowTitle('Wave Form')
        self.show()

    def init_matplotlib(self):
        screen_res = QApplication.primaryScreen().size()
        width = screen_res.width() / 100  # converting to inches, assuming dpi=100
        height = 4  # keep the height constant
        
        fig = Figure(figsize=(width, height), dpi=100)
        ax = fig.add_subplot(111)
        ax.margins(x=0, y=0)  # No margins
        fig.patch.set_facecolor('black')
        ax.set_facecolor('black')
        ax.axis('off')
        
        return fig, ax

    def callback(self, in_data, frame_count, time_info, status):
        audio_data = np.frombuffer(in_data, dtype=np.int16)
        self.ax.clear()
        self.ax.axis('off')
        self.ax.margins(x=-0.4, y=0)  # No margins
        self.ax.set_facecolor('black')
        x = np.linspace(0, len(audio_data), len(audio_data))
        f2 = interp1d(x, audio_data, kind='cubic', fill_value="extrapolate")
        xnew = np.linspace(0, len(audio_data), num=self.width)  # Interpolate within the range of audio_data.
        self.ax.set_xlim(left=0, right=len(audio_data), auto=True)  # Set the x-axis limits to the width of the data
        self.ax.plot(np.linspace(0, self.width, num=self.width), f2(xnew), 'lime', linewidth=2)
        self.ax.set_ylim(-12000, 12000)
        self.canvas.draw()
        return in_data, pyaudio.paContinue

    def on_listen(self):
        self.stream = self.pAud.open(format=pyaudio.paInt16,
                                     channels=1,
                                     rate=44100,
                                     input=True,
                                     input_device_index=1,
                                     frames_per_buffer=1024,
                                     stream_callback=self.callback)
        self.stream.start_stream()
        self.listen_button.setEnabled(False)
        self.stop_button.setEnabled(True)

    def on_stop(self):
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.listen_button.setEnabled(True)
            self.stop_button.setEnabled(False)

    def closeEvent(self, event):
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.pAud.terminate()
        event.accept()  # let the window close


def main():
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps)
    screen_resolution = app.primaryScreen().size()  # Get screen size
    screen_width = screen_resolution.width()  # Screen Width
    screen_height = screen_resolution.height()  # Screen Height
    ex = WaveFormApp(screen_width, screen_height)
    ex.showFullScreen()
    ex.on_listen()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
