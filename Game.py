import os
import random
from random import*
import math
import pygame
from os import listdir
from os.path import isfile, join
pygame. init()
#seed(320)

pygame.display.set_caption('Game')             #Survival game
BG_COLOR = (255,255,255)
WIDTH, HEIGHT = 1500, 800
FPS = 60
PLAYER_VELOCITY = 5
window = pygame.display.set_mode((WIDTH,HEIGHT))

lBlue=(204,255,255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
white=(255,255,255)
font = pygame.font.SysFont('Georgia',30, bold=True)
font2 = pygame.font.SysFont('Georgia',20, bold=True)

def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

def load_sprite_sheets(dir1, dir2, width, height, direction = False):
    path = join("rocnikova", dir1, dir2)
    images =[f for f in listdir(path) if isfile(join(path, f))]

    all_sprites={}

    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()

        sprites = []
        for i in range (sprite_sheet.get_width()//width):
            surface = pygame.Surface((width,height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0 , width, height)
            surface.blit(sprite_sheet, (0,0),rect)
            sprites.append(pygame.transform.scale2x(surface))

        if direction:
            all_sprites[image.replace(".png", "")+ "_right"] = sprites
            all_sprites[image.replace(".png", "")+ "_left"] = flip(sprites)

        else:
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites

class Player(pygame.sprite.Sprite):
    COLOR = (255, 0 , 0)
    GRAVITY = 1
    SPRITES = load_sprite_sheets("MainCharacter","GirlWithFrlbs", 48,62, True)
    ANIMATION_DELAY = 5

    def __init__(self,x,y,width,height):
        super().__init__()
        self.rect = pygame.Rect(x,y,width,height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = 'left'
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 0
        self.hit = False
        self.hit_count = 0
        self.health=3
        self.max_health = self.health
        self.dead_count = 0

    def jump(self):
        self.y_vel = -self.GRAVITY * 8
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 1:
            self.fall_count = 0


    def move(self,dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def make_hit (self):
        if self.hit == False:
            self.hit = True
            self.hit_count = 0
            self.health -= 1

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != 'left':
            self.direction = 'left'
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != 'right':
            self.direction = 'right'
            self.animation_count = 0

    def loop(self,fps):
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        if self.health > 0:
            self.move(self.x_vel, self.y_vel)
        else:
            self.dead_count +=1

        if self.hit:
            self.hit_count += 1

        if self.hit_count > fps * 2:
            self.hit = False
            self.hit_count = 0

        self.fall_count += 1
        self.update_sprite()

    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    def hit_head(self):
        self.count =0
        self.y_vel *= -1

    def update_sprite(self):
        sprite_sheets = "GirlM"
        if self.hit:
            sprite_sheets = "hit"
            if self.health == 0:
                sprite_sheets = "die"
                self.hit_count = 0
        elif self.x_vel != 0:
            sprite_sheets = "run"

        sprite_sheets_name = sprite_sheets + "_" + self.direction
        sprites = self.SPRITES[sprite_sheets_name]
        sprite_index = self.animation_count // self.ANIMATION_DELAY % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count +=1
        self.update()

    def is_dead(self):
        if self.dead_count > FPS * 2:
            return True
        return False
    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, win, offset_x):
        #self.sprite = self.SPRITES["GirlM_" + self.direction][0]
        win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y))

class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self, window, offset_x):
        window.blit(self.image, (self.rect.x - offset_x, self.rect.y))


class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block = get_block(size)
        self.image.blit(block,(0, 0))
        self.mask = pygame.mask.from_surface(self.image)

class Fire(Object):
    ANIMATION_DELAY = 3

    def __init__(self, x,y, width, height):
        super().__init__(x, y ,width, height, "fire")
        self.fire = load_sprite_sheets("Traps", "Fire", width, height)
        self.image = self. fire["off"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = "off"
        self.offset = randint(0,(len(self.fire["on"])))

    def on(self):
        self.animation_name = "on"

    def off(self):
        self.animation_name = "off"

    def loop(self):
        sprites = self.fire[self.animation_name]
        sprite_index = ((self.animation_count // self.ANIMATION_DELAY) + self.offset) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1

        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0

class HealthBar(pygame.sprite.Sprite):
    heart = load_sprite_sheets("Other","health", 33, 39, False)
    def __init__(self,x,y,health, max_health):
        super().__init__()
        self.rect = pygame.Rect(x, y, health, max_health)
        self.x = x
        self.y = y
        self.hit = False
        self.health = health
        self.max_health = max_health

    def draw_health(self, health):
        self.health = health

        sprite_sheets = "heart"
        if health<1:
            sprite_sheets = "bl_heart"

        sprite_sheets2 = "heart"
        if health<2:
            sprite_sheets2 = "bl_heart"

        sprite_sheets3 = "heart"
        if health<3:
            sprite_sheets3 = "bl_heart"

        sprite = self.heart[sprite_sheets][0]
        sprite2 = self.heart[sprite_sheets2][0]
        sprite3 = self.heart[sprite_sheets3][0]
        '''ratio = self.health / self.max_health
        pygame.draw.rect(window, BLACK,  (self.x - 2, self.y - 2, 154, 24))
        pygame.draw.rect(window, RED, (self.x, self.y, 150, 20))
        pygame.draw.rect(window, GREEN, (self.x, self.y, 150 * ratio, 20))'''
        window.blit(sprite,(self.rect.x, self.rect.y))
        window.blit(sprite2,(self.rect.x + self.x+64, self.rect.y))
        window.blit(sprite3, (self.rect.x + self.x+140, self.rect.y))

def get_background(name):
    image = pygame.image.load(join("rocnikova",name))
    _, _, width, height = image.get_rect()

    tiles=[]

    for i in range (WIDTH//width + 1):
        for j in range (HEIGHT// height +1):
            pos = (i* width, j * height)
            tiles.append(pos)

    return tiles, image

def get_block(size):
    path = join("Rocnikova", "Terrain", "Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(96, 130, size, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)

def draw(background, bg_image, player, objects, offset_x, health_bar):
    for tile in background:
        window.blit(bg_image, tile)

    for obj in objects:
        obj.draw(window, offset_x)

    health_bar.draw_health(player.health)
    player.draw(window, offset_x)

    pygame.display.update()

def handle_vertical_collision (player, objects, dy):
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player,obj):
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()

            collided_objects.append(obj)

    return collided_objects

def collide(player, objects, dx):
    player.move(dx, 0)
    player.update()
    collided_object = None
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            collided_object = obj
            break

    player.move(-dx, 0)
    player.update()
    return collided_object

def handle_move(player, objects):
    keys = pygame.key.get_pressed()

    player.x_vel = 0
    collide_left = collide(player, objects, -PLAYER_VELOCITY * 2)
    collide_right = collide(player, objects, PLAYER_VELOCITY * 2)


    if keys[pygame.K_LEFT] and not collide_left:
        player.move_left(PLAYER_VELOCITY)
    if keys[pygame.K_RIGHT] and not collide_right:
        player.move_right(PLAYER_VELOCITY)


    vertical_collide = handle_vertical_collision(player, objects, player.y_vel)
    to_check = [collide_left, collide_right, *vertical_collide]
    for obj in to_check:
        if obj and obj.name == "fire":
             player.make_hit()

def main():
    clock = pygame.time.Clock()
    background, bg_image = get_background('DBlue.png')

    block_size = 96
    player = Player (0,580,50,50)
    floor = [Block(i * block_size, HEIGHT - block_size, block_size) for i in range(-WIDTH // block_size, (WIDTH * 100) // block_size)]
    health_bar = HealthBar(10, 10, player.health, player.health)



    '''z = randint(100, 500)
    fire = Fire(z, HEIGHT - block_size - 64, 16, 32)
    fire.on()'''


    second_floor_x = []
    second_floor = []
    for sc_fl in range(1000):
        x = randint(0, 1900)
        object = Block(x * block_size, HEIGHT - block_size * 4.45, block_size)
        second_floor.append(object)
        second_floor_x.append(x)

    first_floor_x = []
    first_floor = []
    for fr_floor in range(100):
        x2 = randint(0, 700)
        object = Block(x2 * block_size, HEIGHT - block_size * 1.95, block_size)
        if x2 in second_floor_x :
            x3 = randint(0, 1900)
            object2 = Block(x3 * block_size, HEIGHT - block_size * 4.45, block_size)
            first_floor.append(object2)
            first_floor_x.append(x3)

        else:
            first_floor.append(object)
            first_floor_x.append(x2)

    trap_fire = []
    for fir in range(100):
        x4 = randint(10, 90000)
        fire = Fire(x4, HEIGHT - block_size - 64, 16, 32)
        fire.on()
        if x4 in first_floor_x :
            x5 = randint(0, 6000)
            fire2 = Fire(x5, HEIGHT - block_size - 64, 16, 32)
            fire.on()
            trap_fire.append(fire2)
        else:
            trap_fire.append(fire)


    objects = [* floor, *second_floor, *first_floor, *trap_fire]
    offset_x = 0
    scroll_area_width = 200

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE and player.jump_count < 2:
                    player.jump()

        if player.is_dead():
            run = False

        player.loop(FPS)
        for fire in trap_fire:
            fire.loop()
        handle_move(player,objects)
        draw(background, bg_image, player, objects, offset_x, health_bar)

        if ((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0) or (
                (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
            offset_x += player.x_vel

    pygame.quit()
    quit()
if __name__ =='__main__':
    main()