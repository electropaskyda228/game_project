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
    board_image = load_image('board.png', size=(50, 50))

    def __init__(self, group, x, y):
        super().__init__(all_sprites, group)
        self.image = rotate_image(Board.board_image, randint(0, 4) * 90, x + Board.board_image.get_rect().width // 2,
                                  y + Board.board_image.get_rect().height // 2)[0]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x * Board.board_image.get_rect().width, y * Board.board_image.get_rect().height


class Wall(pygame.sprite.Sprite):
    wall_image = load_image('wall.png', size=(50, 50))

    def __init__(self, group, angle, x, y):
        super().__init__(all_sprites, group)
        self.image = rotate_image(Wall.wall_image, angle, x + Wall.wall_image.get_rect().width // 2,
                                  y + Wall.wall_image.get_rect().height // 2)[0]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x * Wall.wall_image.get_rect().width, y * Wall.wall_image.get_rect().height


board_group = pygame.sprite.Group()
for i in range(width // Board.board_image.get_rect().width):
    for j in range(height // Board.board_image.get_rect().height):
        Board(board_group, i, j)

wall_group = pygame.sprite.Group()
for i in range(width // Wall.wall_image.get_rect().width):
    Wall(wall_group, 0, i, 0)
    Wall(wall_group, 0, i, height // Wall.wall_image.get_rect().height - 1)
for i in range(height // Wall.wall_image.get_rect().height):
    Wall(wall_group, 90, 0, i)
    Wall(wall_group, 90, width // Wall.wall_image.get_rect().width - 1, i)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(pygame.Color('black'))
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(fps)

terminate()
