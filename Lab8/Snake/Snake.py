import pygame
import time
import random

snake_speed = 10

window_x = 720
window_y = 480

black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
purple = pygame.Color(128, 0, 128)
blue = pygame.Color(0, 0, 255)

def show_score_level():
    score_text = font.render(f'Score: {score}  Level: {level}', True, white)
    game_window.blit(score_text, (10, 10))

def game_over():
    game_window.fill(black)
    final_text = font.render(f'Game Over! Your Score: {score}', True, red)
    game_window.blit(final_text, (window_x // 4, window_y // 3))
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    quit()

def generate_fruit_position():
    while True:
        pos = [random.randrange(1, (window_x // 10)) * 10, 
               random.randrange(1, (window_y // 10)) * 10]
        if pos not in snake_body and 0 < pos[0] < window_x - 10 and 0 < pos[1] < window_y - 10:
            return pos

pygame.init()
pygame.display.set_caption('Snake Game with Levels')
game_window = pygame.display.set_mode((window_x, window_y))
fps = pygame.time.Clock()

font = pygame.font.SysFont('times new roman', 24)

snake_position = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50], [70, 50]]

fruit_position = generate_fruit_position()
fruit_spawn = True

direction = 'RIGHT'
change_to = direction

score = 0
level = 1
foods_eaten = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 'DOWN':
                change_to = 'UP'
            elif event.key == pygame.K_DOWN and direction != 'UP':
                change_to = 'DOWN'
            elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                change_to = 'LEFT'
            elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                change_to = 'RIGHT'
    
    direction = change_to

    if direction == 'UP':
        snake_position[1] -= 10
    elif direction == 'DOWN':
        snake_position[1] += 10
    elif direction == 'LEFT':
        snake_position[0] -= 10
    elif direction == 'RIGHT':
        snake_position[0] += 10
    
    snake_body.insert(0, list(snake_position))
    if snake_position == fruit_position:
        score += 10
        foods_eaten += 1
        fruit_spawn = False
    else:
        snake_body.pop()
    
    if not fruit_spawn:
        fruit_position = generate_fruit_position()
        fruit_spawn = True
    
    if foods_eaten >= 4:
        level += 1
        snake_speed += 2
        foods_eaten = 0
    
    game_window.fill(black)
    for pos in snake_body:
        pygame.draw.rect(game_window, purple, pygame.Rect(pos[0], pos[1], 10, 10))
    pygame.draw.rect(game_window, white, pygame.Rect(fruit_position[0], fruit_position[1], 10, 10))
    
    show_score_level()
    
    if snake_position[0] < 0 or snake_position[0] >= window_x or \
       snake_position[1] < 0 or snake_position[1] >= window_y:
        game_over()
    for block in snake_body[1:]:
        if snake_position == block:
            game_over()
    
    pygame.display.update()
    fps.tick(snake_speed)
