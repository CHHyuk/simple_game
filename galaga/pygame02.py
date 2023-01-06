import pygame
import random
import time
from datetime import datetime

# 1. 초기화
pygame.init()

# 2. 게임 화면 설정
size = [1024, 768]
screen = pygame.display.set_mode(size)

title = '갤러그 만들기'
pygame.display.set_caption(title) 

# 3. 게임 초기 설정
clock = pygame.time.Clock()
background = pygame.image.load('C:/git/simple_game/galaga/map.png').convert_alpha()
laser = pygame.image.load('C:/git/simple_game/galaga/laser.png').convert_alpha()
enemy1 = pygame.image.load('C:/git/simple_game/galaga/enemy1.png').convert_alpha()
enemy2 = pygame.image.load('C:/git/simple_game/galaga/enemy2.png').convert_alpha()
black = (0,0,0)
white = (255,255,255)
to_x = 0
to_y = 0

class Object:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.move = 0
        
    def add_img(self, address, x, y):
        if address[-3:] == 'png':
            self.img = pygame.image.load(address).convert_alpha()
        else:
            self.img = pygame.image.load(address)
        self.img = pygame.transform.scale(self.img, (x,y))
        self.size_x, self.size_y = self.img.get_size()
    
    def show(self):
        screen.blit(self.img, (self.x, self.y))

# 우주선 설정
ship = Object()
ship.add_img('C:/git/simple_game/galaga/ship.png',70,70)
ship.x = round(size[0] / 2) - round(ship.size_x / 2)
ship.y = size[1] - ship.size_y - 40
ship.move = 5

laser_list = []
enemy_list = []

score = 0

system_exit = 0
while system_exit == 0:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                system_exit = 1
                 
    screen.fill(black)
    font = pygame.font.Font('C:/git/simple_game/galaga/D2Coding-Ver1.3.2-20180524/D2Coding/D2Coding-Ver1.3.2-20180524.ttc', 40)
    text= font.render('Press Space to start!', True, white)
    screen.blit(text, (size[0]/2 - 200, size[1]/2 - 50))
    pygame.display.flip()

# 4. 메인 이벤트
start_time = datetime.now()
flag = True
while flag:

    # fps 설정
    clock.tick(60)

    # 입력 장치 감지
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            flag = False
        
        if event.type == pygame.KEYDOWN:    
            if event.key == pygame.K_LEFT:
                to_x -= ship.move
            elif event.key == pygame.K_RIGHT:
                to_x += ship.move
            elif event.key == pygame.K_UP:
                to_y -= ship.move
            elif event.key == pygame.K_DOWN:
                to_y += ship.move
            elif event.key == pygame.K_SPACE:
                space_move = True
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                to_x = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                to_y = 0
            elif event.key == pygame.K_SPACE:
                space_move = False

        if ship.x < 0:
            ship.x = 0
        elif ship.x > size[0] - ship.size_x:
            ship.x = size[0] - ship.size_x
    
        if ship.y < 0:
            ship.y = 0
        elif ship.y > size[1] - ship.size_y:
            ship.y = size[1] - ship.size_y
        
        ship.x += to_x
        ship.y += to_y
        
        current_time = datetime.now()
        delta_time = round((current_time - start_time).total_seconds())

        if space_move == True:
            laser = Object()
            laser.add_img('C:/git/simple_game/galaga/laser.png',5,10)
            laser.move = 20
            laser.x = ship.x + round(ship.size_x / 2) - round(laser.size_x / 2)
            laser.y = ship.y
            laser_list.append(laser)
            space_move = False
        
        delete_laser = []
        for i in range(len(laser_list)):
            l = laser_list[i]
            l.y -= l.move
            if l.y <= -l.size_y:
                delete_laser.append(i)
        
        try:
            delete_laser.reverse()
            for 