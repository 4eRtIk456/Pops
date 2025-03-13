from datetime import datetime
import pygame

w, h = 900, 675
run = True

pygame.init()

screen = pygame.display.set_mode((w, h))
clock = pygame.time.Clock()

background = pygame.image.load(r"D:\Pops\Lab7\Сlock\bg.jpg")
big_hand = pygame.image.load(r"D:\Pops\Lab7\Сlock\big_hand.png")
small_hand = pygame.image.load(r"D:\Pops\Lab7\Сlock\small_hand.png")

original_rect_sh = small_hand.get_rect(center=(w // 2, h // 2))
original_rect_bh = big_hand.get_rect(center=(w // 2, h // 2))

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            print("Good bye <3")
    screen.blit(background, (0, 0))

    now = datetime.now()
    seconds = now.second
    minutes = now.minute

    rotated_sh = pygame.transform.rotate(small_hand, seconds * -6)
    rotated_bh = pygame.transform.rotate(big_hand, minutes * -6)
    rotated_rect_sh = rotated_sh.get_rect(center=original_rect_sh.center)
    rotated_rect_bh = rotated_bh.get_rect(center=original_rect_bh.center)

    screen.blit(rotated_sh, rotated_rect_sh.topleft)
    screen.blit(rotated_bh, rotated_rect_bh.topleft)

    print(f"seconds = {seconds}")

    pygame.display.flip()
    clock.tick(30)