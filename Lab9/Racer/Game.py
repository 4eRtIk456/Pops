import pygame, sys
from pygame.locals import *
import random, time

# Initializing
pygame.init()

# Setting up FPS
FPS = 60
FramePerSec = pygame.time.Clock()

# Creating colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Other Variables for use in the program
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
COIN_SCORE = 0  # Track coin points
COIN_THRESHOLD = 10  # Points needed to increase speed

# Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

# Create a white screen
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")

# Load and play background music
pygame.mixer.music.load("D:\\Pops\\Lab8\\Racer\\background_music.mp3")
pygame.mixer.music.play(-1, 0.0)

coin_sound = pygame.mixer.Sound(r"D:\Pops\Lab8\Racer\CoinSound.mp3")


class Enemy(pygame.sprite.Sprite):
    enemy_images = [
        "D:\\Pops\\Lab9\\Racer\\Enemy_1.png",
        "D:\\Pops\\Lab9\\Racer\\Enemy_2.png",
        "D:\\Pops\\Lab9\\Racer\\Enemy_3.png",
        "D:\\Pops\\Lab9\\Racer\\Enemy_4.png"
    ]

    def __init__(self):
        super().__init__()
        self.change_skin()

    def change_skin(self):
        chosen_image = random.choice(self.enemy_images)
        self.image = pygame.image.load(chosen_image)
        self.rect = self.image.get_rect(center=(random.randint(40, SCREEN_WIDTH - 40), 0))

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            SCORE += 1
            self.change_skin()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("D:\\Pops\\Lab8\\Racer\\Player.png")
        self.rect = self.image.get_rect(center=(160, 520))

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0 and pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH and pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.value = random.choice([2, 5, 10])
        if self.value == 2:
            self.image = pygame.image.load("D:\\Pops\\Lab9\\Racer\\Coin_2.png")
        elif self.value == 5:
            self.image = pygame.image.load("D:\\Pops\\Lab9\\Racer\\Coin_5.png")
        else:
            self.image = pygame.image.load("D:\\Pops\\Lab9\\Racer\\Coin_10.png")

        self.rect = self.image.get_rect(center=(random.randint(40, SCREEN_WIDTH - 40), 0))


    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

    

class Background():
    def __init__(self):
        self.bgimage = pygame.image.load('D:\\Pops\\Lab8\\Racer\\AnimatedStreet.png')
        self.rectBGimg = self.bgimage.get_rect()

        self.bgY1 = 0
        self.bgX1 = 0

        self.bgY2 = self.rectBGimg.height
        self.bgX2 = 0

        self.movingUpSpeed = 5
         
    def update(self):
        self.bgY1 -= self.movingUpSpeed
        self.bgY2 -= self.movingUpSpeed
        if self.bgY1 <= -self.rectBGimg.height:
            self.bgY1 = self.rectBGimg.height
        if self.bgY2 <= -self.rectBGimg.height:
            self.bgY2 = self.rectBGimg.height
             
    def render(self):
        DISPLAYSURF.blit(self.bgimage, (self.bgX1, self.bgY1))
        DISPLAYSURF.blit(self.bgimage, (self.bgX2, self.bgY2))

def spawn_coin_avoiding_enemies():
        for _ in range(10): 
            new_coin = Coin()
            if not pygame.sprite.spritecollideany(new_coin, enemies):
                return new_coin
        return None


# Setting up Sprites
P1 = Player()
E1 = Enemy()
coins = pygame.sprite.Group()

back_ground = Background()

enemies = pygame.sprite.Group()
enemies.add(E1)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1, E1)


ADD_COIN = pygame.USEREVENT + 2
pygame.time.set_timer(ADD_COIN, 2000)  # Spawn a coin every 2 seconds

# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == ADD_COIN:
            new_coin = spawn_coin_avoiding_enemies()
            if new_coin:
                coins.add(new_coin)
                all_sprites.add(new_coin)
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    back_ground.update()
    back_ground.render()


    # Display scores
    score_text = font_small.render(f"Score: {SCORE}", True, BLACK)
    DISPLAYSURF.blit(score_text, (10, 10))

    coin_text = font_small.render(f"Coins: {COIN_SCORE}", True, BLACK)
    coin_text_rect = coin_text.get_rect(topright=(SCREEN_WIDTH - 10, 10))
    DISPLAYSURF.blit(coin_text, coin_text_rect)

    # Move and draw all sprites
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    # Check for coin collection
    collected_coins = pygame.sprite.spritecollide(P1, coins, True)
    for coin in collected_coins:
        COIN_SCORE += coin.value
        coin_sound.play()

    if COIN_SCORE >= 25:
        SPEED += 1
        COIN_SCORE = 0

    # Collision detection
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound("D:\\Pops\\Lab8\\Racer\\crash.wav").play()
        pygame.mixer.music.stop()
        time.sleep(0.8)
        pygame.mixer.Sound("D:\\Pops\\Lab8\\Racer\\GameOver.mp3").play()
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))
        pygame.display.update()
        time.sleep(1.5)
        pygame.quit()
        sys.exit()

    pygame.display.update()
    FramePerSec.tick(FPS)
