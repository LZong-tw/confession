import cv2
import pygame
import numpy as np
import PySimpleGUI as sg

# Initialize Pygame
pygame.init()

# Initialize the screen
screen_width, screen_height = sg.Window.get_screen_size()
size = (screen_width, screen_height)
screen = pygame.display.set_mode(size)

video = cv2.VideoCapture('assets/bg_video/actual.mp4')
frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

frame_aspect_ratio = frame_width / frame_height
screen_aspect_ratio = screen_width / screen_height

frames = []  # list to store each frame

# Main loop
clock = pygame.time.Clock()
mode = "forward_backward"  # Can be "forward_backward" or "forward_only"
reverse = False
while True:
    # Resize while maintaining aspect ratio
    if frame_aspect_ratio > screen_aspect_ratio:
        new_width = screen_width
        new_height = int(screen_width / frame_aspect_ratio)
    else:
        new_height = screen_height
        new_width = int(screen_height * frame_aspect_ratio)

    if not reverse or mode == "forward_only":
        ret, frame = video.read()
        if not ret:
            if mode == "forward_only":
                video.set(cv2.CAP_PROP_POS_FRAMES, 0)  # rewind the video
            else:
                reverse = True
            continue
        frames.append(frame)
    else:
        if len(frames) == 0:
            reverse = False
            video.set(cv2.CAP_PROP_POS_FRAMES, 0)  # rewind the video
            continue
        frame = frames.pop()
    
    frame = cv2.resize(frame, (new_width, new_height))

    # Convert the frame to RGB (OpenCV uses BGR by default)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Create a Pygame surface from the NumPy array
    frame = np.rot90(frame)
    frame = np.flipud(frame)
    frame = pygame.surfarray.make_surface(frame)

    # Calculate position to start drawing
    x = (screen_width - new_width) // 2
    y = (screen_height - new_height) // 2

    # Blit the frame onto the Pygame surface
    screen.blit(frame, (x, y))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            video.release()
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Switch mode when space bar is pressed
                if mode == "forward_backward":
                    mode = "forward_only"
                else:
                    mode = "forward_backward"

    pygame.display.flip()
    clock.tick(30)  # Limit to 30 FPS