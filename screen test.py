import pygame
import keyboard
import win32api
import win32con
import win32gui

def screen_on(screen, fade_duration=3000):
    clock = pygame.time.Clock()
    fuchsia = (255, 0, 128)  # Transparency color

    # Create layered window
    hwnd = pygame.display.get_wm_info()["window"]
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                        win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
    # Set window transparency color
    win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*fuchsia), 0, win32con.LWA_COLORKEY)
    screen.fill(fuchsia)  # Transparent background
    pygame.display.update()
    clock.tick(60)

def screen_off(screen, fade_duration=3000):
    fade_color = (0, 0, 0, 0)  # Black color with full transparency
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()

    while True:
        elapsed_time = pygame.time.get_ticks() - start_time
        fade_alpha = int((elapsed_time / fade_duration) * 255)
        
        if fade_alpha >= 255:
            break
        
        screen.fill(fade_color)  # Start with a fully transparent surface
        fade_surface = pygame.Surface((screen_width, screen_height), pygame.FULLSCREEN)
        fade_surface.fill(fade_color[:3] + (fade_alpha,))
        screen.blit(fade_surface, (0, 0))

        pygame.display.update()
        clock.tick(60)

pygame.init()
screen_width = 1920
screen_height = 1080
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN) # FULLSCREEN
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

    if keyboard.is_pressed('k'):
        print("K pressed")
        screen_on(screen)

    if keyboard.is_pressed('l'):
        print("L pressed")
        screen_off(screen)
