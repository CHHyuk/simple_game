import pygame
import random
import time
from datetime import datetime
import math

# 1. 초기화
pygame.init()

# 2. 게임 화면 설정
size = [1024, 768]
screen = pygame.display.set_mode(size)

title = '슈팅게임 만들기'
pygame.display.set_caption(title) 

# 3. 게임 초기 설정
clock = pygame.time.Clock()
ship_img = pygame.image.load('C:/git/simple_game/shooting/ship.png').convert_alpha()
background = pygame.image.load('C:/git/simple_game/shooting/map.png').convert_alpha()
laser_img = pygame.image.load('C:/git/simple_game/shooting/laser.png').convert_alpha()
enemy1_img = pygame.image.load('C:/git/simple_game/shooting/enemy1.png').convert_alpha()
enemy2_img = pygame.image.load('C:/git/simple_game/shooting/enemy2.png').convert_alpha()
boss_laser_img = pygame.image.load('C:/git/simple_game/shooting/boss_laser.png').convert_alpha()
black = (0,0,0)
white = (255,255,255)
to_x = 0
to_y = 0

class Object:
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

def crash(a, b):
    if (a.x - b.size_x <= b.x) and (b.x <= a.x + a.size_x): 
        if (a.y - b.size_y <= b.y) and (b.y <= a.y + a.size_y): 
            return True
        else:
            return False
    else:
        return False

# 우주선 설정
ship = Object()
ship.add_img(ship_img,70,70)
ship.x = round(size[0] / 2) - round(ship.size_x / 2)
ship.y = size[1] - ship.size_y - 40
ship.move = 5

laser_list = []
enemy_list = []
boss_list = []
boss_laser_list = []

difficulty = 0.97
space_move = False
game_over = 0
round_score = 0
boss_alert = 0
boss_check = 0
boss_life = 300
round_clear = 0

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
    font = pygame.font.Font('C:/git/simple_game/shooting/D2Coding-Ver1.3.2-20180524/D2Coding/D2Coding-Ver1.3.2-20180524.ttc', 40)
    text= font.render('Press Space to start!', True, white)
    screen.blit(text, (size[0]/2 - 225, size[1]/2 - 50))
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
        laser.add_img(laser_img,5,10)
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
        for d in delete_laser:
            del laser_list[d]
    except:
        pass

    delete_enemy = []
    for i in range(len(enemy_list)):
        e = enemy_list[i]
        e.y += e.move
        if e.y >= size[1]:
            delete_enemy.append(i)
        
    try:
        delete_enemy.reverse()
        for d in delete_enemy:
            del enemy_list[d]
    except:
        pass
    
    delete_boss_laser = []
    for i in range(len(boss_laser_list)):
        bl = boss_laser_list[i]
        bl.y += bl.move
        if bl.y >= size[1]:
            delete_boss_laser.append(i)
    
    try:
        delete_boss_laser.reverse()
        for d in delete_boss_laser:
            del boss_laser_list[d]
    except:
        pass

    delete_laser_list = []
    delete_enemy_list = []
    
    for i in range(len(laser_list)):
        for j in range(len(enemy_list)):
            l = laser_list[i]
            e = enemy_list[j]
            if crash(l,e) == True:
                delete_enemy_list.append(j)
                delete_laser_list.append(i)

    for i in range(len(laser_list)):
        for j in range(len(boss_list)):
            l = laser_list[i]
            b = boss_list[j]
            if crash(l,b) == True:
                delete_laser_list.append(i)   
                boss_life -= 1
    for i in range(len(boss_laser_list)):
        bl = boss_laser_list[i]
        if crash(bl,ship) == True:
            flag = False
            game_over = 1         

    delete_laser_list = list(set(delete_laser_list))
    delete_enemy_list = list(set(delete_enemy_list))

    try:
        delete_laser_list.reverse()
        delete_enemy_list.reverse()
        for dl in delete_laser_list:
            del laser_list[dl]
        for de in delete_enemy_list:
            del enemy_list[de]
            round_score += 1
    except:
        pass

    for i in range(len(enemy_list)):
        e = enemy_list[i]
        if crash(e,ship) == True:
            flag = False
            game_over = 1
    
    for i in range(len(boss_list)):
        b = boss_list[i]
        if crash(b,ship) == True:
            flag = False
            game_over = 1

    if random.random() > difficulty:
        enemy = Object()
        enemy.add_img(enemy1_img,40,40)  
        enemy.move = 2
        enemy.x = random.randrange(0 + ship.size_x, size[0]-enemy.size_x - ship.size_x)
        enemy.y = 15
        enemy_list.append(enemy)
        if round_score >= 100:
            difficulty = 1

    if random.random() > 0.90 and round_score >= 100:
        boss_laser = Object()
        boss_laser.add_img(boss_laser_img,5,10)
        boss_laser.move = random.randrange(1,5)
        boss_laser.x = random.randrange(0, size[0])
        boss_laser.y = 0
        boss_laser_list.append(boss_laser)

    if round_score == 99:
        boss_alert = 1
        boss_check = 1
        round_score += 1

    if boss_check == 1:
        boss = Object()
        boss.add_img(enemy2_img,200,200)
        boss.move = 0
        boss.x = ((size[0] / 2) - 100)
        boss.y = 30
        boss_list.append(boss)
        boss_check = 0
    
    if boss_life == 0:
        flag = False
        round_clear = 1

    screen.blit(background, (0,0))
    ship.show()
    for l in laser_list:
        l.show()
    for e in enemy_list:
        e.show()
    for b in boss_list:
        b.show()
    for bl in boss_laser_list:
        bl.show()

    font = pygame.font.Font('C:/git/simple_game/shooting/D2Coding-Ver1.3.2-20180524/D2Coding/D2Coding-Ver1.3.2-20180524.ttc',20)
    text_score = font.render('round score : {} / 100'.format(round_score),True, white)
    screen.blit(text_score, (10,10))

    text_time = font.render('time : {}'.format(delta_time),True, white)
    screen.blit(text_time,(size[0] - 100, 10))

    if round_score >= 100:
        font = pygame.font.Font('C:/git/simple_game/shooting/D2Coding-Ver1.3.2-20180524/D2Coding/D2Coding-Ver1.3.2-20180524.ttc',20)
        text_boss_life = font.render('boss life : {}'. format(boss_life),True,white)
        screen.blit(text_boss_life, (10 , 30))

    pygame.display.flip()

    while boss_alert == 1:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = 0
        font = pygame.font.Font('C:/git/simple_game/shooting/D2Coding-Ver1.3.2-20180524/D2Coding/D2Coding-Ver1.3.2-20180524.ttc',80)
        text_boss = font.render('Warning!!', True, white)
        screen.blit(text_boss,(size[0]/2 - 200, size[1]/2 - 50))
        pygame.display.flip()
        time.sleep(1)
        boss_alert = 0
        
    while game_over == 1:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = 0
        screen.fill(black)
        font = pygame.font.Font('C:/git/simple_game/shooting/D2Coding-Ver1.3.2-20180524/D2Coding/D2Coding-Ver1.3.2-20180524.ttc',80)
        text_over = font.render('GAME OVER',True,white)
        screen.blit(text_over,(size[0]/2 - 200, size[1]/2 - 50))
        pygame.display.flip()

    while round_clear == 1:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                round_clear = 0
        screen.fill(black)
        font = pygame.font.Font('C:/git/simple_game/shooting/D2Coding-Ver1.3.2-20180524/D2Coding/D2Coding-Ver1.3.2-20180524.ttc',80)
        text_over = font.render('CLEAR!!!!',True,white)
        screen.blit(text_over,(size[0]/2 - 200, size[1]/2 - 50))
        pygame.display.flip()
    
pygame.quit()