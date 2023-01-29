import pygame
import os
import sys
from random import randint


pygame.init()
pygame.display.set_caption('We need to rename')
size = width, height = 1100, 800
screen = pygame.display.set_mode(size)
running = True
all_sprites = pygame.sprite.Group()
clock = pygame.time.Clock()
fps = 30


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None, size=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    if size is not None:
        image = pygame.transform.scale(image, size)
    return image


def rotate_image(image, angle, x, y):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(center=(x, y)).center)

    return rotated_image, new_rect


class Board(pygame.sprite.Sprite):
    image = load_image('board.png', size=(50, 50))

    def __init__(self, group, x, y):
        super().__init__(all_sprites, group)
        self.image = rotate_image(Board.image, randint(0, 4) * 90, x + 25, y + 25)[0]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x * 50, y * 50


board_group = pygame.sprite.Group()
for i in range(width // 50):
    for j in range(height // 50):
        Board(board_group, i, j)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(pygame.Color('black'))
    board_group.draw(screen)
    pygame.display.flip()
    clock.tick(fps)

terminate()