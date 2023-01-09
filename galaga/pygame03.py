import pygame
from enum import Enum
from datetime import datetime

pygame.init()

size = [400,900]
screen = pygame.display.set_mode(size)
title = '갤러그'
pygame.display.set_caption(title)

clock = pygame.time.Clock()
ship_img = pygame.image.load('C:/git/simple_game/shooting/ship.png').convert_alpha()
background = pygame.image.load('C:/git/simple_game/shooting/map.png').convert_alpha()
laser_img = pygame.image.load('C:/git/simple_game/shooting/laser.png').convert_alpha()
enemy1_img = pygame.image.load('C:/git/simple_game/shooting/enemy1.png').convert_alpha()
enemy2_img = pygame.image.load('C:/git/simple_game/shooting/enemy2.png').convert_alpha()
enemy_laser_img = pygame.image.load('C:/git/simple_game/shooting/boss_laser.png').convert_alpha()
black = (0,0,0)
white = (255,255,255)
to_x = 0
to_y = 0

class Object(Enum):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.move = 0
        self.type = 0

    def add_img(self, address, x, y):
        self.img = address
        self.img = pygame.transform.scale(self.img, (x,y))
        self.size_x, self.size_y = self.img.get_size()
    
    def show(self):
        screen.blit(self.img, (self.x, self.y))

ship = Object()
ship.add_img(ship_img,50,50)
ship.x = round(size[0] / 2) - round(ship.size_x / 2)
ship.y = size[1] - ship.size_y - 40
ship.move = 5

missile_list = []
enemy_missile_list = []
enemy_list = []

attack = False
game_over = 0
score = 0
round_check = 0
system_exit = 0

while system_exit == 0:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                system_exit = 1
    
    screen.fill(black)
    font_press = pygame.font.Font('C:/git/simple_game/galaga/D2Coding-Ver1.3.2-20180524/D2Coding/D2Coding-Ver1.3.2-20180524.ttc',20)
    text_press = font_press.render('Press s button', True, (255,0,0))
    font_title = pygame.font.Font('C:/git/simple_game/galaga/D2Coding-Ver1.3.2-20180524/D2Coding/D2Coding-Ver1.3.2-20180524.ttc',40)
    text_title = font_title.render('좌우키 : 이동', True, white)
    text_title2 = font_title.render('S키 : 공격',True, white)
    screen.blit(text_title, ((size[0]/2) - 125, size[1]/2 - 200))
    screen.blit(text_title2, ((size[0]/2) - 100, size[1]/2 - 150))
    screen.blit(text_press, ((size[0]/2) - 65, size[1]/2 + 200))
    pygame.display.flip()

start_time = datetime.now()


