import pygame
import os
import sys
from random import randint
from math import atan, pi, cos, sin
from Random_Rooms import random_rooms

pygame.init()
pygame.display.set_caption('We need to rename this')
size = width, height = 1100, 800
screen = pygame.display.set_mode(size)
running = True
all_sprites = pygame.sprite.Group()
now = pygame.sprite.Group()
clock = pygame.time.Clock()
fps = 30
left_button_pressed = False
spavn_event = pygame.USEREVENT + 1
pygame.time.set_timer(spavn_event, 2000)


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
        super().__init__(all_sprites, now, group)
        self.image = pygame.transform.rotate(Wall.wall_image, angle)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x * Wall.wall_image.get_rect().width, y * Wall.wall_image.get_rect().height


class Hero(pygame.sprite.Sprite):
    hero_image = load_image('hero7.png', size=(65, 52))

    def __init__(self, group):
        super().__init__(all_sprites, group)
        self.image = Hero.hero_image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = randint(0, width), randint(0, height)
        while pygame.sprite.spritecollideany(self, now):
            self.rect.x, self.rect.y = randint(0, width), randint(0, height)
        now.add(self)
        self.direction = 0
        self.v = 5
        self.hp = 500

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
        if pygame.sprite.spritecollideany(self, wall_group) or pygame.sprite.spritecollideany(self, box_group):
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
                pygame.sprite.spritecollideany(self, zombie_group) or pygame.sprite.spritecollideany(self, box_group):
            zombie = pygame.sprite.spritecollideany(self, zombie_group)
            if zombie:
                zombie.hp -= 1
            self.kill()


class Zombie(pygame.sprite.Sprite):
    zombie_image = load_image('monstr.png', size=(65, 52))

    def __init__(self, group):
        super().__init__(all_sprites, group)
        self.image = Zombie.zombie_image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = randint(0, width), randint(0, height)
        while pygame.sprite.spritecollideany(self, now):
            self.rect.x, self.rect.y = randint(0, width), randint(0, height)
        now.add(self)
        self.direction = 0
        self.change_direction()
        self.v = 5
        self.hp = randint(1, 10)

    def change_direction(self):
        if hero.rect.centerx - self.rect.centerx != 0:
            angle = atan((self.rect.centery - hero.rect.centery) / (hero.rect.centerx - self.rect.centerx))
        elif hero.rect.centery > self.rect.centery:
            angle = - pi / 2
        else:
            angle = pi / 2
        if hero.rect.centerx < self.rect.centerx:
            angle += pi
        angle = angle / pi * 180
        self.image, self.rect = rotate_image(Zombie.zombie_image, angle, self.rect.center)
        self.direction = angle

    def update(self):
        if self.hp <= 0:
            self.kill()
        self.rect = self.rect.move(self.v * cos(self.direction), 0)
        if pygame.sprite.collide_rect(self, hero):
            hero.hp -= 100
            self.kill()
        if pygame.sprite.spritecollideany(self, box_group) or pygame.sprite.spritecollideany(self, wall_group):
            self.rect = self.rect.move(- self.v * cos(self.direction), 0)
        self.rect = self.rect.move(0, - self.v * sin(self.direction))
        if pygame.sprite.spritecollideany(self, box_group) or pygame.sprite.spritecollideany(self, wall_group):
            self.rect = self.rect.move(0, self.v * sin(self.direction))
        self.change_direction()


class Box(pygame.sprite.Sprite):
    box_image = load_image('box2.jpg', size=(50, 50))

    def __init__(self, group):
        super().__init__(all_sprites, group)
        self.image = Box.box_image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = randint(0, width), randint(0, height)
        while pygame.sprite.spritecollideany(self, now):
            self.rect.x, self.rect.y = randint(0, width), randint(0, height)
        now.add(self)


def new_room():
    if hero.rect[0] <= 0:
        hero.rect.x, hero.rect.y = 999, 370
        for i in board_group:
            i.rect.x, i.rect.y = i.rect.x - 1100, i.rect.y
    if hero.rect[0] >= width:
        hero.rect.x, hero.rect.y = 10, 370
    if hero.rect[1] <= 0:
        hero.rect.x, hero.rect.y = 530, 750
    if hero.rect[1] >= height:
        hero.rect.x, hero.rect.y = 530, 10


board_group = pygame.sprite.Group()
rooms = random_rooms()
for n in rooms:
    for i in range(width // Board.board_image.get_rect().width):
        for j in range(height // Board.board_image.get_rect().height):
            Board(board_group, i + n[0], j + n[1])

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

box_group = pygame.sprite.Group()
for i in range(randint(2, 10)):
    Box(box_group)

hero_group = pygame.sprite.Group()
hero = Hero(hero_group)
shoot_group = pygame.sprite.Group()
zombie_group = pygame.sprite.Group()


def start_screen():
    intro_text = ["Перемещение героя - " "Клавиши WASD",
                  "Стрельба - " " Мышь",
                  "Цель:", "Найти выход и ВЫЖИТЬ"]

    fon = pygame.transform.scale(load_image('start_screen.png'), (1100, 800))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(50)


def final_screen(flag):
    if flag:
        name = 'loose_screen.webp'
        intro_text = ["","","","","","","","                                                                                  Поражение"]
        color = 'red'
    else:
        name = 'final_screen.jpg'
        intro_text = ["                                      Победа!!!!!"]
        color = 'white'
    fon = pygame.transform.scale(load_image(name), (1100, 800))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color(color))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        pygame.display.flip()
        clock.tick(50)


start_screen()
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
        if event.type == spavn_event:
            Zombie(zombie_group)

    all_key = pygame.key.get_pressed()
    if all_key[pygame.K_d]:
        hero.move(1, 0)
    if all_key[pygame.K_a]:
        hero.move(-1, 0)
    if all_key[pygame.K_w]:
        hero.move(0, -1)
    if all_key[pygame.K_s]:
        hero.move(0, 1)
    new_room()
    if hero.hp == 0:
        final_screen(True)

    screen.fill(pygame.Color('black'))
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()
    clock.tick(fps)

terminate()
