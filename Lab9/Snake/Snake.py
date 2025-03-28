import pygame
import time
import random

# Initialize game speed
snake_speed = 10

# Window size
window_x = 720
window_y = 480

# Colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
purple = pygame.Color(128, 0, 128)
blue = pygame.Color(0, 0, 255)
green = pygame.Color(0, 255, 0)

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
    return [random.randrange(1, (window_x // 10)) * 10,
            random.randrange(1, (window_y // 10)) * 10]

def generate_fruit():
    global fruit_position, fruit_timer, fruit_value, fruit_color
    fruit_position = generate_fruit_position()
    fruit_timer = time.time()
    fruit_value = random.choice([5, 10, 15])  # Different weights
    fruit_color = {5: blue, 10: white, 15: green}[fruit_value]  # Color mapping

# Initialize pygame
pygame.init()
pygame.display.set_caption('Snake Game with Levels')
game_window = pygame.display.set_mode((window_x, window_y))
fps = pygame.time.Clock()

# Load font
font = pygame.font.SysFont('times new roman', 24)

# Initial snake and fruit settings
snake_position = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50], [70, 50]]
direction = 'RIGHT'
change_to = direction
score = 0
level = 1
foods_eaten = 0
fruit_timer = 0  # Track when the fruit was spawned
fruit_lifetime = 7  # Seconds before fruit disappears

generate_fruit()

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
    
    # Update direction
    direction = change_to
    
    # Move snake
    if direction == 'UP':
        snake_position[1] -= 10
    elif direction == 'DOWN':
        snake_position[1] += 10
    elif direction == 'LEFT':
        snake_position[0] -= 10
    elif direction == 'RIGHT':
        snake_position[0] += 10
    
    # Update snake body
    snake_body.insert(0, list(snake_position))
    if snake_position == fruit_position:
        score += fruit_value
        foods_eaten += 1
        generate_fruit()
    else:
        snake_body.pop()
    
    # Remove food if it stays too long
    if time.time() - fruit_timer > fruit_lifetime:
        generate_fruit()
    
    # Level up logic
    if foods_eaten >= 4:
        level += 1
        snake_speed += 2
        foods_eaten = 0
    
    # Update game window
    game_window.fill(black)
    for pos in snake_body:
        pygame.draw.rect(game_window, purple, pygame.Rect(pos[0], pos[1], 10, 10))
    pygame.draw.rect(game_window, fruit_color, pygame.Rect(fruit_position[0], fruit_position[1], 10, 10))
    
    show_score_level()
    
    # Check for collisions
    if snake_position[0] < 0 or snake_position[0] >= window_x or \
       snake_position[1] < 0 or snake_position[1] >= window_y:
        game_over()
    for block in snake_body[1:]:
        if snake_position == block:
            game_over()
    
    pygame.display.update()
    fps.tick(snake_speed)
