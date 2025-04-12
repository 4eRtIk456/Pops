import pygame
import time
import random
import json
from connect import connect, delete_saved_game
from config import load_config

# Initialize game speed (базовая скорость)
base_snake_speed = 10
snake_speed = base_snake_speed

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

# Уровни (пример - вы можете добавить больше и сложнее)
levels_config = {
    1: {"speed_multiplier": 1, "walls": []},
    2: {"speed_multiplier": 1.2, "walls": [[100, 100, 20, 100], [300, 300, 100, 20]]}, # [x, y, width, height]
    3: {"speed_multiplier": 1.5, "walls": [[50, 50, 150, 20], [400, 150, 20, 150], [600, 300, 100, 20]]},
}

def load_user_level(conn, username):
    
    cursor = conn.cursor()
    cursor.execute("SELECT level FROM user_scores us JOIN users u ON us.user_id = u.user_id WHERE u.username = %s ORDER BY saved_at DESC LIMIT 1", (username,))
    result = cursor.fetchone()
    return result[0] if result else 1

def get_user_id(conn, username):
    
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users WHERE username = %s", (username,))
    user_id = cursor.fetchone()
    if user_id is None:
        cursor.execute("INSERT INTO users (username) VALUES (%s) RETURNING user_id", (username,))
        user_id = cursor.fetchone()
        conn.commit()
    return user_id[0]

def save_game_state(conn, user_id, score, level, snake_position, snake_body, fruit_position, direction):
    
    cursor = conn.cursor()
    game_state = json.dumps({
        "snake_position": snake_position,
        "snake_body": snake_body,
        "fruit_position": fruit_position,
        "direction": direction
    })
    cursor.execute("INSERT INTO user_scores (user_id, score, level, game_state) VALUES (%s, %s, %s, %s)",
                   (user_id, score, level, game_state))
    conn.commit()
    print("Игра сохранена!")

def load_game_state(conn, user_id):
   
    cursor = conn.cursor()
    cursor.execute("SELECT score, level, game_state FROM user_scores WHERE user_id = %s ORDER BY saved_at DESC LIMIT 1", (user_id,))
    result = cursor.fetchone()
    if result:
        score, level, game_state_json = result
        game_state = json.loads(game_state_json)
        return score, level, game_state["snake_position"], game_state["snake_body"], game_state["fruit_position"], game_state["direction"]
    return None

def draw_walls(level):
    
    if level in levels_config:
        for wall in levels_config[level]["walls"]:
            pygame.draw.rect(game_window, (100, 100, 100), pygame.Rect(wall[0], wall[1], wall[2], wall[3]))

def check_wall_collision(snake_head, level):
    
    if level in levels_config:
        for wall in levels_config[level]["walls"]:
            if wall[0] < snake_head[0] < wall[0] + wall[2] and \
               wall[1] < snake_head[1] < wall[1] + wall[3]:
                return True
    return False

def generate_random_snake(max_length):
    length = random.randint(3, max_length)
    x = random.randrange(0, window_x, 10)
    y = random.randrange(0, window_y, 10)
    snake = [[x, y]]
    direction = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
    for _ in range(length - 1):
        if direction == 'UP':
            y += 10
        elif direction == 'DOWN':
            y -= 10
        elif direction == 'LEFT':
            x += 10
        elif direction == 'RIGHT':
            x -= 10
        snake.append([x % window_x, y % window_y])  # Wrap around edges
    return snake, direction

def move_random_snake(snake, direction):
    head = list(snake[0])
    if direction == 'UP':
        head[1] -= 10
    elif direction == 'DOWN':
        head[1] += 10
    elif direction == 'LEFT':
        head[0] -= 10
    elif direction == 'RIGHT':
        head[0] += 10
    snake.insert(0, [head[0] % window_x, head[1] % window_y])
    snake.pop()
    # Randomly change direction
    if random.random() < 0.1:
        direction = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
    return snake, direction

def draw_snake(snake, color):
    for pos in snake:
        pygame.draw.rect(game_window, color, pygame.Rect(pos[0], pos[1], 10, 10))

def start_screen():
    input_active = True
    user_name = ""
    input_box = pygame.Rect(window_x // 4, window_y // 2 + 50, 350, 40)
    title_font = pygame.font.SysFont('comicsansms', 72)
    prompt_font = pygame.font.SysFont('comicsansms', 28)
    random_snakes = [generate_random_snake(10) for _ in range(5)] 
    conn = connect(load_config()) 
    current_level = None

    try:
        while input_active:
            game_window.fill(black)
            for i in range(len(random_snakes)):
                random_snakes[i] = move_random_snake(random_snakes[i][0], random_snakes[i][1])
                draw_snake(random_snakes[i][0], random.choice([green, blue, purple]))

            # Title
            title_text = title_font.render("Snake Game", True, green)
            title_rect = title_text.get_rect(center=(window_x // 2, 150))
            game_window.blit(title_text, title_rect)

            # Instruction
            prompt_text = prompt_font.render("Enter your name and press Enter:", True, white)
            prompt_rect = prompt_text.get_rect(midtop=(window_x // 2, window_y // 2 - 50))
            game_window.blit(prompt_text, prompt_rect)

            if user_name and conn:
                level = load_user_level(conn, user_name)
                level_text = prompt_font.render(f"Current Level: {level}", True, white)
                level_rect = level_text.get_rect(midtop=(window_x // 2, window_y // 2 + 10))
                game_window.blit(level_text, level_rect)

            pygame.draw.rect(game_window, white, input_box, 2)
            name_surface = font.render(user_name, True, white)
            game_window.blit(name_surface, (input_box.x + 5, input_box.y + 5))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    input_active = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        input_active = False
                        if conn:
                            current_level = load_user_level(conn, user_name)
                    elif event.key == pygame.K_BACKSPACE:
                        user_name = user_name[:-1]
                    else:
                        if len(user_name) < 20:
                            user_name += event.unicode
            time.sleep(0.1)
    finally:
        if conn:
            conn.close()
            print("Соединение с базой данных закрыто на стартовом экране.")

    return user_name, current_level if current_level is not None else 1

def show_score_level():
    score_text = font.render(f'Score: {score}   Level: {level}', True, white)
    game_window.blit(score_text, (10, 10))

def game_over(conn, user_id):
    game_window.fill(black)
    game_over_font = pygame.font.SysFont('Bauhaus 93', 80)
    score_font = pygame.font.SysFont('times new roman', 36)
    game_over_text = game_over_font.render('Game Over!', True, red)
    score_text = score_font.render(f'Your Score: {score}', True, white)
    game_over_rect = game_over_text.get_rect(center=(window_x // 2, window_y // 2 - 40))
    score_rect = score_text.get_rect(center=(window_x // 2, window_y // 2 + 40))
    game_window.blit(game_over_text, game_over_rect)
    game_window.blit(score_text, score_rect)
    pygame.display.flip()
    time.sleep(3)
    if conn and user_id:
        delete_saved_game(conn, user_id)
    pygame.quit()
    quit()

def generate_fruit_position(level):

    while True:
        pos = [random.randrange(1, (window_x // 10)) * 10,
               random.randrange(1, (window_y // 10)) * 10]
        if not check_wall_collision(pos, level):
            return pos

def generate_fruit(level):
    global fruit_position, fruit_timer, fruit_value, fruit_color
    fruit_position = generate_fruit_position(level)
    fruit_timer = time.time()
    fruit_value = random.choice([5, 10, 15])  
    fruit_color = {5: blue, 10: white, 15: green}[fruit_value] 

# Initialize pygame
pygame.init()

pygame.display.set_caption('Snake Game with Levels')
game_window = pygame.display.set_mode((window_x, window_y))
fps = pygame.time.Clock()


font = pygame.font.SysFont('times new roman', 24)

username, level = start_screen()
print("Игрок:", username, "Текущий уровень:", level)

conn = connect(load_config()) 
user_id = None
if conn:
    user_id = get_user_id(conn, username)
    saved_game = load_game_state(conn, user_id)

    if saved_game:
        score, level, snake_position, snake_body, fruit_position, direction = saved_game
        change_to = direction
        fruit_timer = time.time()
        fruit_lifetime = 7
        foods_eaten = 0
        fruit_value = 10 
        fruit_color = {5: blue, 10: white, 15: green}[fruit_value]
        print("Загружено сохраненное состояние игры!")
    else:
        
        snake_position = [100, 50]
        snake_body = [[100, 50], [90, 50], [80, 50], [70, 50]]
        direction = 'RIGHT'
        change_to = direction
        score = 0
        foods_eaten = 0
        fruit_timer = time.time()
        fruit_lifetime = 7
        generate_fruit(level)
        snake_speed = base_snake_speed * levels_config[level].get("speed_multiplier", 1)
        print("Новая игра.")
else:
    print("Не удалось подключиться к базе данных для получения user_id.")
    
    snake_position = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50], [70, 50]]
    direction = 'RIGHT'
    change_to = direction
    score = 0
    foods_eaten = 0
    fruit_timer = time.time()
    fruit_lifetime = 7
    generate_fruit(level) 
    snake_speed = base_snake_speed * levels_config[level].get("speed_multiplier", 1)

paused = False

try:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise SystemExit
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
                    if paused and conn and user_id:
                        save_game_state(conn, user_id, score, level, snake_position, snake_body, fruit_position, direction)
                        print("Игра автоматически сохранена при паузе.")
                    elif paused:
                        print("Игра на паузе. Автоматическое сохранение...")
                    else:
                        print("Продолжение игры.")
                elif not paused:
                    if event.key == pygame.K_UP and direction != 'DOWN':
                        change_to = 'UP'
                    elif event.key == pygame.K_DOWN and direction != 'UP':
                        change_to = 'DOWN'
                    elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                        change_to = 'LEFT'
                    elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                        change_to = 'RIGHT'
                    elif event.key == pygame.K_s:
                        if conn and user_id:
                            save_game_state(conn, user_id, score, level, snake_position, snake_body, fruit_position, direction)
                        else:
                            print("Невозможно сохранить: нет подключения к базе данных или user_id.")

        if not paused:
            
            direction = change_to

            if direction == 'UP':
                snake_position[1] -= 10
            elif direction == 'DOWN':
                snake_position[1] += 10
            elif direction == 'LEFT':
                snake_position[0] -= 10
            elif direction == 'RIGHT':
                snake_position[0] += 10

            snake_head = snake_position[:]
            snake_body.insert(0, list(snake_head))
            if snake_position == fruit_position:
                score += fruit_value
                foods_eaten += 1
                generate_fruit(level)
            else:
                snake_body.pop()

            if time.time() - fruit_timer > fruit_lifetime:
                generate_fruit(level)

            if foods_eaten >= 4:
                level = min(level + 1, len(levels_config))
                snake_speed = base_snake_speed * levels_config[level].get("speed_multiplier", 1)
                foods_eaten = 0
                generate_fruit(level)

            game_window.fill(black)
            draw_walls(level)
            for pos in snake_body:
                pygame.draw.rect(game_window, purple, pygame.Rect(pos[0], pos[1], 10, 10))
            pygame.draw.rect(game_window, fruit_color, pygame.Rect(fruit_position[0], fruit_position[1], 10, 10))

            show_score_level()

            if check_wall_collision(snake_head, level) or \
               snake_position[0] < 0 or snake_position[0] >= window_x or \
               snake_position[1] < 0 or snake_position[1] >= window_y:
                game_over(conn, user_id)
            for block in snake_body[1:]:
                if snake_position == block:
                    game_over(conn, user_id)

            pygame.display.update()
            fps.tick(snake_speed)
        else:
            pause_font = pygame.font.SysFont('comicsansms', 48)
            pause_text = pause_font.render("PAUSED", True, white)
            pause_rect = pause_text.get_rect(center=(window_x // 2, window_y // 2))
            game_window.blit(pause_text, pause_rect)
            pygame.display.update()
            time.sleep(0.1)
except SystemExit:
    pass
finally:
    if conn:
        conn.close()
        print("Соединение с базой данных закрыто в основном цикле.")