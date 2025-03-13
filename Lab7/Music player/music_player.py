import pygame
import os

# Initialize pygame mixer and pygame\pygame.mixer.init()
pygame.init()

# Define music files (Ensure these exist in the same directory)
playlist = ["D:\Pops\Lab7\Music player\Demrick & Brevi - Runway Walk.mp3", "D:\Pops\Lab7\Music player\Kali Uchis - Telepatía.mp3", "D:\Pops\Lab7\Music player\Shy Smith - Soaked.mp3", "D:\Pops\Lab7\Music player\секси бетмен.mp3"]
current_index = 0

def play_music():
    pygame.mixer.music.load(playlist[current_index])
    pygame.mixer.music.play()
    print(f"Playing: {playlist[current_index]}")

def stop_music():
    pygame.mixer.music.stop()
    print("Music stopped")

def next_track():
    global current_index
    current_index = (current_index + 1) % len(playlist)
    play_music()

def previous_track():
    global current_index
    current_index = (current_index - 1) % len(playlist)
    play_music()

# Mapping keys to functions
key_actions = {
    pygame.K_SPACE: play_music,
    pygame.K_s: stop_music,
    pygame.K_n: next_track,
    pygame.K_p: previous_track,
}

# Start pygame window
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Music Player")
font = pygame.font.Font(None, 36)

def draw_controls():
    screen.fill((30, 30, 30))
    controls = [
        "SPACE - Play",
        "S - Stop",
        "N - Next",
        "P - Previous"
    ]
    
    y_offset = 50
    for control in controls:
        text_surface = font.render(control, True, (255, 255, 255))
        screen.blit(text_surface, (50, y_offset))
        y_offset += 40
    
    pygame.display.flip()

running = True
while running:
    draw_controls()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            action = key_actions.get(event.key)
            if action:
                action()

pygame.quit()
