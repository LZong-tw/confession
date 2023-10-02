import PySimpleGUI as sg
import pyaudio
import numpy as np
from scipy.interpolate import interp1d
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import ctypes
import time

def audio_wave_form_body(audio_wave_form_queue):
    # Initialize variables and objects
    _VARS = {'window': False, 'stream': False, 'line': None, 'fig_agg': None}
    screen_width, screen_height = sg.Window.get_screen_size()
    screen_width = screen_width
    screen_height = screen_height
    canvas_width = screen_width + 2800
    canvas_height = screen_height - 60

    # Initialize PySimpleGUI
    AppFont = 'Any 16'
    sg.theme('DarkBlack')
    layout = [
        [sg.Canvas(key='-CANVAS-', size=(canvas_width, canvas_height), pad=((0, 0), (0, 0)), expand_x=True)],
        [sg.ProgressBar(4000, orientation='h', size=(20, 20), key='-PROG-')],
        [sg.Button('Listen', font=AppFont), sg.Button('Stop', font=AppFont, disabled=True), sg.Button('Exit', font=AppFont)]
    ]
    _VARS['window'] = sg.Window('    ', layout, no_titlebar=True, finalize=True, location=(0, 0), size=(screen_width, screen_height), keep_on_top=True, alpha_channel=0.0, resizable=True)

    # Initialize matplotlib figure and Pyaudio
    # fig, ax = plt.subplots(figsize=(canvas_width/80, canvas_height/110), dpi=100)
    fig = Figure(figsize=(canvas_width / 60, canvas_height / 100), dpi=100)
    ax = fig.add_subplot(111) 
    fig.patch.set_facecolor('black')
    ax.margins(x=-0.4, y=0)  # No margins
    ax.set_facecolor('black')
    ax.axis('off')

    canvas_elem = _VARS['window']['-CANVAS-']
    canvas = canvas_elem.TKCanvas
    _VARS['fig_agg'] = FigureCanvasTkAgg(fig, canvas)
    _VARS['fig_agg'].get_tk_widget().pack(side='left', fill='x', expand=1)

    # Initialize Pyaudio
    CHUNK = 1024
    RATE = 44100
    INTERVAL = 0.2
    TIMEOUT = 20000
    pAud = pyaudio.PyAudio()

    def callback(in_data, frame_count, time_info, status):
        audio_data = np.frombuffer(in_data, dtype=np.int16)
        ax.clear()
        ax.axis('off')
        ax.margins(x=-0.4, y=0)  # No margins
        ax.set_facecolor('black')
        x = np.linspace(0, len(audio_data), len(audio_data))
        f2 = interp1d(x, audio_data, kind='cubic')
        xnew = np.linspace(0, len(audio_data), num=4096)
        ax.plot(xnew, f2(xnew), 'g')
        ax.set_ylim(-10000, 10000)
        _VARS['window']['-PROG-'].update(np.amax(audio_data))
        _VARS['fig_agg'].draw()
        return (in_data, pyaudio.paContinue)

    def listen():
        _VARS['stream'] = pAud.open(format=pyaudio.paInt16,
                                channels=1,
                                rate=RATE,
                                input=True,
                                input_device_index=3,
                                frames_per_buffer=CHUNK,
                                stream_callback=callback)
        _VARS['stream'].start_stream()

    # ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 6)
    # Event Loop
    while True:
        event, values = _VARS['window'].read()
        _VARS['window']['Listen'].update(disabled=True)
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == 'Listen':
            listen()
            _VARS['window']['Stop'].update(disabled=False)
            _VARS['window']['Listen'].update(disabled=True)
        elif event == 'Stop':
            if _VARS['stream']:
                _VARS['stream'].stop_stream()
                _VARS['stream'].close()
                _VARS['window']['Stop'].update(disabled=True)
                _VARS['window']['Listen'].update(disabled=False)
        
        alpha = _VARS['window'].alpha_channel
        if not audio_wave_form_queue.empty():
            if alpha > 0:
                alpha -= 0.01  # Decrease alpha value
                _VARS['window'].set_alpha(alpha)
                time.sleep(0.05)  # Sleep for a while to make fade out effect visible
        else:
            if alpha < 0.5:
                alpha += 0.01  # Increase alpha value
                _VARS['window'].set_alpha(alpha)
                time.sleep(0.05)  # Sleep for a while to make the fade-in effect visible
    _VARS['window'].close()
