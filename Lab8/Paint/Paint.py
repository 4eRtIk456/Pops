import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Paint Program")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

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
    img = font.render(text, True, BLACK)
    screen.blit(img, pos)

def draw_menu():
    pygame.draw.rect(screen, RED, (10, 10, 50, 30))
    pygame.draw.rect(screen, GREEN, (70, 10, 50, 30))
    pygame.draw.rect(screen, BLUE, (130, 10, 50, 30))
    pygame.draw.rect(screen, BLACK, (190, 10, 50, 30))
    draw_text("Pencil", (250, 15))
    draw_text("Rect", (320, 15))
    draw_text("Circle", (380, 15))
    draw_text("Eraser", (450, 15))

draw_menu()

running = True
start_pos = None
preview_rect = None
preview_circle = None

while running:
    screen.blit(canvas, (0, 0))
    draw_menu()
    
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
                    x1, y1 = start_pos
                    rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
                    pygame.draw.rect(canvas, color, rect, 2)
                    preview_rect = None
                elif mode == "circle":
                    
                    radius = int(((end_pos[0] - start_pos[0]) ** 2 + (end_pos[1] - start_pos[1]) ** 2) ** 0.5)
                    pygame.draw.circle(canvas, color, start_pos, radius, 2)
                    preview_circle = None
            
        if event.type == pygame.MOUSEMOTION:
            if drawing and mode == "pencil":
                if last_pos is not None:
                    pygame.draw.line(canvas, color, last_pos, event.pos, 3)
                last_pos = event.pos
            elif drawing and mode == "eraser":
                pygame.draw.circle(canvas, WHITE, event.pos, 10)
            elif previewing and mode == "rect":
                x1, y1 = start_pos
                x2, y2 = event.pos
                preview_rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
            elif previewing and mode == "circle":
                end_pos = event.pos
                radius = int(((end_pos[0] - start_pos[0]) ** 2 + (end_pos[1] - start_pos[1]) ** 2) ** 0.5)
                preview_circle = (start_pos, radius)
    
    pygame.display.update()
    clock.tick(60)

pygame.quit()