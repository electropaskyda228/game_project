import pygame
import os
import sys
from random import randint
from math import atan, pi, cos, sin


pygame.init()
pygame.display.set_caption('We need to rename this')
size = width, height = 1100, 800
screen = pygame.display.set_mode(size)
running = True
all_sprites = pygame.sprite.Group()
clock = pygame.time.Clock()
fps = 30
left_button_pressed = False


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


def rotate_image(image, angle, centre):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=centre)

    return rotated_image, new_rect


class Board(pygame.sprite.Sprite):
    board_image = load_image('board.png', size=(50, 50))

    def __init__(self, group, x, y):
        super().__init__(all_sprites, group)
        self.image = pygame.transform.rotate(Board.board_image, randint(0, 4) * 90)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x * Board.board_image.get_rect().width, y * Board.board_image.get_rect().height


class Wall(pygame.sprite.Sprite):
    wall_image = load_image('wall.png', size=(50, 50))

    def __init__(self, group, angle, x, y):
        super().__init__(all_sprites, group)
        self.image = pygame.transform.rotate(Wall.wall_image, angle)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x * Wall.wall_image.get_rect().width, y * Wall.wall_image.get_rect().height


class Hero(pygame.sprite.Sprite):
    hero_image = load_image('hero7.png', size=(65, 52))

    def __init__(self, group, x, y):
        super().__init__(all_sprites, group)
        self.image = Hero.hero_image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.direction = 0
        self.v = 5

    def change_direction(self, pos):
        if pos[0] - self.rect.centerx != 0:
            angle = atan((self.rect.centery - pos[1]) / (pos[0] - self.rect.centerx))
        elif pos[1] > self.rect.centery:
            angle = - pi / 2
        else:
            angle = pi / 2
        if pos[0] < self.rect.centerx:
            angle += pi
        angle = angle / pi * 180
        self.image, self.rect = rotate_image(Hero.hero_image, angle, self.rect.center)
        self.direction = angle

    def move(self, v_x, v_y):
        self.rect = self.rect.move(v_x * self.v, v_y * self.v)
        if pygame.sprite.spritecollideany(self, wall_group):
            self.rect = self.rect.move(-v_x * self.v, -v_y * self.v)


class Shoot(pygame.sprite.Sprite):
    shoot_image = pygame.Surface([10, 10])

    def __init__(self, group, x, y, angle):
        super().__init__(all_sprites, group)
        self.image = Shoot.shoot_image
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = x, y
        pygame.draw.circle(self.image, pygame.Color('white'), (5, 5), 5)
        self.image.set_colorkey(self.image.get_at((0, 0)))
        self.direction = angle
        self.v = 20

    def update(self):
        self.rect = self.rect.move(self.v * cos(self.direction), - self.v * sin(self.direction))
        if pygame.sprite.spritecollideany(self, wall_group) or self.rect.centerx > width or self.rect.centerx < 0 or \
                self.rect.centery < 0 or self.rect.centery > height or \
                pygame.sprite.spritecollideany(self, zoombie_group):
            self.kill()


board_group = pygame.sprite.Group()
for i in range(width // Board.board_image.get_rect().width):
    for j in range(height // Board.board_image.get_rect().height):
        Board(board_group, i, j)

wall_group = pygame.sprite.Group()
for i in range(width // Wall.wall_image.get_rect().width):
    if i == width // 2 // Wall.wall_image.get_rect().width or \
            i == width // 2 // Wall.wall_image.get_rect().width - 1:
        continue
    Wall(wall_group, 0, i, 0)
    Wall(wall_group, 0, i, height // Wall.wall_image.get_rect().height - 1)
for i in range(height // Wall.wall_image.get_rect().height):
    if i == height // 2 // Wall.wall_image.get_rect().height or \
            i == height // 2 // Wall.wall_image.get_rect().height - 1:
        continue
    Wall(wall_group, 90, 0, i)
    Wall(wall_group, 90, width // Wall.wall_image.get_rect().width - 1, i)

hero_group = pygame.sprite.Group()
hero = Hero(hero_group, 100, 100)
shoot_group = pygame.sprite.Group()
zoombie_group = pygame.sprite.Group()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            hero.change_direction(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and not left_button_pressed:
            Shoot(shoot_group, hero.rect.centerx, hero.rect.centery, hero.direction * pi / 180)
            left_button_pressed = True
        if event.type == pygame.MOUSEBUTTONUP and not pygame.mouse.get_pressed()[0]:
            left_button_pressed = False

    all_key = pygame.key.get_pressed()
    if all_key[pygame.K_d]:
        hero.move(1, 0)
    if all_key[pygame.K_a]:
        hero.move(-1, 0)
    if all_key[pygame.K_w]:
        hero.move(0, -1)
    if all_key[pygame.K_s]:
        hero.move(0, 1)

    screen.fill(pygame.Color('black'))
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()
    clock.tick(fps)

terminate()
