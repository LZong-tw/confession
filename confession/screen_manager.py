import pygame

def screen_manager(door_queue_for_screen, screen_queue, welcome_queue, ambient_queue):

    def screen_on(screen, fade_duration=3000):
        fade_color = (255, 255, 255)  # White color
        clock = pygame.time.Clock()
        start_time = pygame.time.get_ticks()
        
        while True:
            elapsed_time = pygame.time.get_ticks() - start_time
            fade_alpha = int((elapsed_time / fade_duration) * 255)
            
            if fade_alpha >= 255:
                break
            
            screen.fill((0, 0, 0))  # Start with a black screen
            fade_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
            fade_surface.fill(fade_color + (255 - fade_alpha,))
            screen.blit(fade_surface, (0, 0))
            
            pygame.display.update()
            clock.tick(60)

    def screen_off(screen, fade_duration=3000):
        fade_color = (255, 255, 255)  # White color
        clock = pygame.time.Clock()
        start_time = pygame.time.get_ticks()

        while True:
            elapsed_time = pygame.time.get_ticks() - start_time
            fade_alpha = int((elapsed_time / fade_duration) * 255)
            
            if fade_alpha >= 255:
                break
            
            screen.fill(fade_color)  # Start with a white screen
            fade_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
            fade_surface.fill((0, 0, 0) + (fade_alpha,))
            screen.blit(fade_surface, (0, 0))

            pygame.display.update()
            clock.tick(60)

    pygame.init()
    screen_width = 1920
    screen_height = 1080
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

        while not door_queue_for_screen.empty():
            content = door_queue_for_screen.get()
            if content == "OPEN":
                screen_on(screen)
                if welcome_queue.empty():
                    welcome_queue.put("welcome")
                    ambient_queue.put("START")
                while not door_queue_for_screen.empty():
                    door_queue_for_screen.get()
                break

        while not screen_queue.empty():
            content = screen_queue.get()
            if content == "Screen off":
                screen_off(screen)
                break
