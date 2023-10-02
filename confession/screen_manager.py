import pygame
import keyboard
import win32api
import win32con
import win32gui
import pygetwindow as gw

def screen_manager(door_queue_for_screen, screen_queue, welcome_queue, ambient_queue, audio_wave_from_queue):
    is_open = False
    def screen_on(fade_duration=3000):
        clock = pygame.time.Clock()
        fuchsia = (255, 0, 128)  # Transparency color

        # Create layered window
        hwnd = pygame.display.get_wm_info()["window"]
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                               win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
        # Set window transparency color (fully opaque black)
        win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*fuchsia[:3]), 0, win32con.LWA_COLORKEY)
        pygame.display.update()
        clock.tick(60)

        start_time = pygame.time.get_ticks()
        while True:
            elapsed_time = pygame.time.get_ticks() - start_time
            fade_alpha = int((elapsed_time / fade_duration) * 255)

            if fade_alpha >= 255:
                break

            # Reduce the window's alpha value for fading in
            win32gui.SetLayeredWindowAttributes(hwnd, 0, 255 - fade_alpha, win32con.LWA_ALPHA)

            pygame.display.update()
            clock.tick(60)

    def screen_off(fade_duration=3000):
        clock = pygame.time.Clock()
        start_time = pygame.time.get_ticks()

        while True:
            elapsed_time = pygame.time.get_ticks() - start_time
            fade_alpha = int((elapsed_time / fade_duration) * 255)

            if fade_alpha >= 255:
                break

            # Set the window's alpha value for fading out
            hwnd = pygame.display.get_wm_info()["window"]
            win32gui.SetLayeredWindowAttributes(hwnd, 0, fade_alpha, win32con.LWA_ALPHA)

            pygame.display.update()
            clock.tick(60)

    pygame.init()
    screen_width = 1920
    screen_height = 1080
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)
    pygame.display.set_caption("Always on Top Window")
    # Make the window always-on-top
    window = gw.getWindowsWithTitle('Always on Top Window')[0]
    window.alwaysOnTop = True
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

        if not door_queue_for_screen.empty():
            content = door_queue_for_screen.get()
            if content == "OPEN" and not is_open:
                audio_wave_from_queue.put('ON')
                screen_on()
                is_open = True
                if welcome_queue.empty():
                    welcome_queue.put("welcome")
                    ambient_queue.put("START")
                if not door_queue_for_screen.empty():
                    door_queue_for_screen.get()

        if not screen_queue.empty():
            content = screen_queue.get()
            if content == "Screen off" and is_open:
                audio_wave_from_queue.get()
                screen_off()
                is_open = False
