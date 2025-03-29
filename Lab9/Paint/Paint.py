import pygame
import math

pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Extended Paint Program")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Create a drawing canvas
canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(WHITE)

clock = pygame.time.Clock()
drawing = False
previewing = False
last_pos = None
radius = 5
mode = "pencil"
color = BLACK

font = pygame.font.SysFont(None, 24)

def draw_text(text, pos):
    """Displays text on the screen."""
    img = font.render(text, True, BLACK)
    screen.blit(img, pos)

def draw_menu():
    """Draws the menu buttons for color and tool selection."""
    pygame.draw.rect(screen, RED, (10, 10, 50, 30))
    pygame.draw.rect(screen, GREEN, (70, 10, 50, 30))
    pygame.draw.rect(screen, BLUE, (130, 10, 50, 30))
    pygame.draw.rect(screen, BLACK, (190, 10, 50, 30))
    pygame.draw.line(screen, BLACK, (260, 20), (290, 20), 3)  # Pencil
    pygame.draw.rect(screen, BLACK, (320, 15, 30, 20), 2)  # Rectangle
    pygame.draw.circle(screen, BLACK, (400, 25), 10, 2)  # Circle
    screen.blit(font.render("Eraser", True, BLACK), (440, 20))  # Eraser (diagonal line)
    pygame.draw.rect(screen, BLACK, (520, 15, 20, 20), 2)  # Square
    pygame.draw.polygon(screen, BLACK, [(580, 35), (615, 35), (615, 15)], 2)  # Right Triangle
    pygame.draw.polygon(screen, BLACK, [(680, 35), (700, 35), (690, 15)], 2)  # Equilateral Triangle
    pygame.draw.polygon(screen, BLACK, [(770, 25), (780, 15), (790, 25), (780, 35)], 2)  # Rhombus

draw_menu()

running = True
start_pos = None
preview_shape = None
preview_rect = None
preview_circle = None

while running:
    screen.blit(canvas, (0, 0))
    draw_menu()
    
    if preview_shape:
        pygame.draw.polygon(screen, color, preview_shape, 1)
    if preview_rect:
        pygame.draw.rect(screen, color, preview_rect, 1)
    if preview_circle:
        pygame.draw.circle(screen, color, preview_circle[0], preview_circle[1], 1)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if 10 <= x <= 60 and 10 <= y <= 40:
                color = RED
            elif 70 <= x <= 120 and 10 <= y <= 40:
                color = GREEN
            elif 130 <= x <= 180 and 10 <= y <= 40:
                color = BLUE
            elif 190 <= x <= 240 and 10 <= y <= 40:
                color = BLACK
            elif 250 <= x <= 300 and 10 <= y <= 40:
                mode = "pencil"
            elif 320 <= x <= 370 and 10 <= y <= 40:
                mode = "rect"
            elif 380 <= x <= 430 and 10 <= y <= 40:
                mode = "circle"
            elif 450 <= x <= 500 and 10 <= y <= 40:
                mode = "eraser"
            elif 520 <= x <= 570 and 10 <= y <= 40:
                mode = "square"
            elif 590 <= x <= 670 and 10 <= y <= 40:
                mode = "right_triangle"
            elif 680 <= x <= 760 and 10 <= y <= 40:
                mode = "equilateral_triangle"
            elif 770 <= x <= 850 and 10 <= y <= 40:
                mode = "rhombus"
            else:
                drawing = True
                previewing = True
                start_pos = event.pos
                last_pos = event.pos
        
        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            previewing = False
            end_pos = event.pos
            x2, y2 = end_pos
            if y2 > 40:
                if mode == "rect":
                    pygame.draw.rect(canvas, color, pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1)), 2)
                elif mode == "square":
                    side = min(abs(x2 - x1), abs(y2 - y1))
                    top_left_x = x1 if x2 >= x1 else x1 - side
                    top_left_y = y1 if y2 >= y1 else y1 - side
                    pygame.draw.rect(canvas, color, pygame.Rect(top_left_x, top_left_y, side, side), 2)
                elif mode == "right_triangle":
                    points = [(x1, y1), (x1, y2), (x2, y2)]
                    pygame.draw.polygon(canvas, color, points, 2)
                elif mode == "equilateral_triangle":
                    height = abs(y2 - y1)
                    base_half = (math.sqrt(3) / 2) * height
                    points = [(x1, y1), (x1 - base_half, y2), (x1 + base_half, y2)]
                    pygame.draw.polygon(canvas, color, points, 2)
                elif mode == "rhombus":
                    width = abs(x2 - x1)
                    height = abs(y2 - y1)
                    points = [(x1, y1 - height // 2), (x1 + width // 2, y1), (x1, y1 + height // 2), (x1 - width // 2, y1)]
                    pygame.draw.polygon(canvas, color, points, 2)
                elif mode == "circle":
                    radius = int(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))
                    pygame.draw.circle(canvas, color, start_pos, radius, 2)
            preview_shape = None
            preview_rect = None
            preview_circle = None
        
        if event.type == pygame.MOUSEMOTION:
            if drawing and mode == "pencil":
                if last_pos is not None:
                    pygame.draw.line(canvas, color, last_pos, event.pos, 3)
                last_pos = event.pos
            elif drawing and mode == "eraser":
                pygame.draw.circle(canvas, WHITE, event.pos, 10)
            elif previewing:
                x1, y1 = start_pos
                x2, y2 = event.pos
                if mode == "square":
                    side = min(abs(x2 - x1), abs(y2 - y1))
                    top_left_x = x1 if x2 >= x1 else x1 - side
                    top_left_y = y1 if y2 >= y1 else y1 - side
                    preview_shape = [
                        (top_left_x, top_left_y),
                        (top_left_x + side, top_left_y),
                        (top_left_x + side, top_left_y + side),
                        (top_left_x, top_left_y + side)
                    ]
                elif mode == "rect":
                    preview_rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
                elif mode == "circle":
                    end_pos = event.pos
                    radius = int(((end_pos[0] - start_pos[0]) ** 2 + (end_pos[1] - start_pos[1]) ** 2) ** 0.5)
                    preview_circle = (start_pos, radius)
                elif mode == "right_triangle":
                    preview_shape = [(x1, y1), (x1, y2), (x2, y2)]
                elif mode == "equilateral_triangle":
                    height = abs(y2 - y1)
                    base_half = (math.sqrt(3) / 2) * height
                    preview_shape = [(x1, y1), (x1 - base_half, y2), (x1 + base_half, y2)]
                elif mode == "rhombus":
                    width = abs(x2 - x1)
                    height = abs(y2 - y1)
                    preview_shape = [(x1, y1 - height // 2), (x1 + width // 2, y1), (x1, y1 + height // 2), (x1 - width // 2, y1)]
    
    pygame.display.update()
    clock.tick(60)

pygame.quit()