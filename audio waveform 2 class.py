import PySimpleGUI as sg
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class AudioVisualizer:
    def __init__(self):
        self._VARS = {'window': False, 'stream': False, 'line': None, 'fig_agg': None}
        self.screen_width, self.screen_height = sg.Window.get_screen_size()
        self.screen_height = self.screen_height - 80
        self.canvas_width = self.screen_width + 1200
        self.canvas_height = self.screen_height - 60
        self.init_window()
        self.init_mpl_figure()

    def init_window(self):
        AppFont = 'Any 16'
        sg.theme('DarkBlack')
        layout = [
            [sg.Canvas(key='-CANVAS-', size=(self.canvas_width, self.canvas_height))],
            [sg.ProgressBar(4000, orientation='h', size=(20, 20), key='-PROG-')],
            [sg.Button('Listen', font=AppFont), sg.Button('Stop', font=AppFont, disabled=True),
             sg.Button('Exit', font=AppFont)]
        ]
        self._VARS['window'] = sg.Window('    ', layout, no_titlebar=False, finalize=True,
                                         location=(0, 0), size=(self.screen_width, self.screen_height),
                                         keep_on_top=False, alpha_channel=0.8)

    def init_mpl_figure(self):
        self.fig = Figure(figsize=(self.canvas_width / 80, self.canvas_height / 100), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.fig.patch.set_facecolor('black')
        self.ax.set_facecolor('black')
        self.ax.axis('off')
        canvas_elem = self._VARS['window']['-CANVAS-']
        self.canvas = canvas_elem.TKCanvas
        self._VARS['fig_agg'] = FigureCanvasTkAgg(self.fig, self.canvas)
        self._VARS['fig_agg'].get_tk_widget().pack(side='left', fill='both', expand=1)

    def callback(self, in_data, frame_count, time_info, status):
        audio_data = np.frombuffer(in_data, dtype=np.int16)
        self.ax.clear()
        self.ax.axis('off')
        self.ax.set_facecolor('black')
        x = np.linspace(0, len(audio_data), len(audio_data))
        f2 = interp1d(x, audio_data, kind='cubic')
        xnew = np.linspace(0, len(audio_data), num=4096)
        self.ax.plot(xnew, f2(xnew), 'g')
        self.ax.set_ylim(-6000, 6000)
        self._VARS['window']['-PROG-'].update(np.amax(audio_data))
        self._VARS['fig_agg'].draw()
        return (in_data, pyaudio.paContinue)

    def listen(self):
        self._VARS['stream'] = self.pAud.open(format=pyaudio.paInt16,
                                         channels=1,
                                         rate=44100,
                                         input=True,
                                         frames_per_buffer=1024,
                                         stream_callback=self.callback)
        self._VARS['stream'].start_stream()

    def event_loop(self):
        while True:
            event, values = self._VARS['window'].read()
            if event == sg.WIN_CLOSED or event == 'Exit':
                break
            if event == 'Listen':
                self.listen()
                self._VARS['window']['Stop'].update(disabled=False)
                self._VARS['window']['Listen'].update(disabled=True)
            elif event == 'Stop':
                if self._VARS['stream']:
                    self._VARS['stream'].stop_stream()
                    self._VARS['stream'].close()
                    self._VARS['window']['Stop'].update(disabled=True)
                    self._VARS['window']['Listen'].update(disabled=False)
        self._VARS['window'].close()


if __name__ == '__main__':
    app = AudioVisualizer()
    app.event_loop()
