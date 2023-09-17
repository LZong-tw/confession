import pygame
import time


def screen_manager(door_queue_for_screen, screen_queue, welcome_queue):
    def screen_on(screen, fade_duration=3000):
        fade_color = (255, 255, 255)  # Black color
        fade_alpha = 100

        clock = pygame.time.Clock()
        start_time = pygame.time.get_ticks()

        while fade_alpha < 255:
            elapsed_time = pygame.time.get_ticks() - start_time
            if elapsed_time >= fade_duration:
                break

            fade_alpha = int((elapsed_time / fade_duration) * 255)
            fade_surface = pygame.Surface(screen.get_size())
            fade_surface.fill(fade_color)
            fade_surface.set_alpha(fade_alpha)

            screen.blit(fade_surface, (0, 0))
            pygame.display.update()

            clock.tick(60)

    def screen_off(screen, fade_duration=3000):
        fade_color = (0, 0, 0)  # Black color
        fade_alpha = 255

        clock = pygame.time.Clock()
        start_time = pygame.time.get_ticks()

        while fade_alpha > 0:
            elapsed_time = pygame.time.get_ticks() - start_time
            if elapsed_time >= fade_duration:
                break

            fade_alpha = 255 - int((elapsed_time / fade_duration) * 255)
            fade_surface = pygame.Surface(screen.get_size())
            fade_surface.fill(fade_color)
            fade_surface.set_alpha(fade_alpha)

            screen.blit(fade_surface, (0, 0))
            pygame.display.update()

            clock.tick(60)

    # Initialize Pygame
    pygame.init()

    # Set the screen dimensions to match your display resolution
    screen_width = 1920  # Change this to your screen's width
    screen_height = 1080  # Change this to your screen's height

    # Create a full-screen window
    screen = pygame.display.set_mode((screen_width, screen_height),
                                     pygame.FULLSCREEN)

    # Set the background color to black
    background_color = (0, 0, 0)

    # Main loop
    running = True
    while running:

        # Fill the screen with black
        # screen.fill(background_color)

        # Update the display
        pygame.display.flip()
        while not door_queue_for_screen.empty():
            content =  door_queue_for_screen.get()
            if content == "OPEN":
                screen_on(screen)
                print("開螢幕")
                if welcome_queue.empty():
                    welcome_queue.put("welcome")
                while not door_queue_for_screen.empty():
                    door_queue_for_screen.get()
                time.sleep(4)
                while not welcome_queue.empty():
                    print("WELCOME QUEUE remains: " + welcome_queue.get())
            while not screen_queue.empty():
                content = screen_queue.get()
                if content == "Screen off":
                    screen_queue.get()
                    print("關螢幕")
                    screen_off(screen)
