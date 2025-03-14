import pygame
import os

pygame.init()
pygame.mixer.init()

# Плейлист
playlist = [
    r"D:\Pops\Lab7\Music player\секси бетмен.mp3",
    r"D:\Pops\Lab7\Music player\Demrick & Brevi - Runway Walk.mp3",
    r"D:\Pops\Lab7\Music player\Kali Uchis - Telepatía.mp3",
    r"D:\Pops\Lab7\Music player\Shy Smith - Soaked.mp3"
]
current_index = 0
is_playing = False

def play_music():
    global is_playing
    pygame.mixer.music.load(playlist[current_index])
    pygame.mixer.music.play()
    is_playing = True
    print(f"Playing: {playlist[current_index]}")

def toggle_play_pause():
    global is_playing
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
        is_playing = False
        print("Paused")
    else:
        pygame.mixer.music.unpause()
        is_playing = True
        print("Resumed")

def next_track():
    global current_index
    current_index = (current_index + 1) % len(playlist)
    play_music()

def previous_track():
    global current_index
    current_index = (current_index - 1) % len(playlist)
    play_music()

# Управление
key_actions = {
    pygame.K_SPACE: toggle_play_pause,
    pygame.K_RIGHT: next_track,
    pygame.K_LEFT: previous_track,
}

# Окно
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Music Player")
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

def draw_controls():
    screen.fill((30, 30, 30))

    # Отображаем название текущего трека
    track_name = os.path.basename(playlist[current_index])  # Получаем только название файла
    wrapped_text = wrap_text(track_name, 350)  # Автоперенос текста на 350px ширины
    y_offset = 50
    for line in wrapped_text:
        track_text = font.render(line, True, (255, 255, 255))
        screen.blit(track_text, (50, y_offset))
        y_offset += 40

    controls = [
        "SPACE - Play/Pause",
        "<-- - Previous",
        "--> - Next"
    ]
    
    # Отображаем кнопки управления
    y_offset += 20
    for control in controls:
        text_surface = small_font.render(control, True, (255, 255, 255))
        screen.blit(text_surface, (50, y_offset))
        y_offset += 40

    pygame.display.flip()

def wrap_text(text, max_width):
    """Функция для переноса текста."""
    words = text.split()
    lines = []
    current_line = ""
    
    for word in words:
        # Пробуем добавить слово в текущую строку
        test_line = current_line + (" " if current_line else "") + word
        test_surface = font.render(test_line, True, (255, 255, 255))
        
        if test_surface.get_width() > max_width:
            # Если длина строки превышает максимальную ширину, начинаем новую строку
            if current_line:
                lines.append(current_line)
            current_line = word
        else:
            current_line = test_line
    
    if current_line:
        lines.append(current_line)
    
    return lines

# Автовоспроизведение первой песни
play_music()

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
