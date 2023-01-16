import pygame
from datetime import datetime
import random


pygame.init()

size = [400,900]
screen = pygame.display.set_mode(size)
title = '갤러그'
pygame.display.set_caption(title)

clock = pygame.time.Clock()
ship_img = pygame.image.load('img/ship.png').convert_alpha()
background = pygame.image.load('img/map.png').convert_alpha()
background = pygame.transform.scale(background, (400,900))
laser_img = pygame.image.load('img/laser.png').convert_alpha()
enemy1_img = pygame.image.load('img/enemy1.png').convert_alpha()
enemy2_img = pygame.image.load('img/enemy2.png').convert_alpha()
enemy_laser_img = pygame.image.load('img/enemy_laser.png').convert_alpha()
black = (0,0,0)
white = (255,255,255)
to_x = 0
to_y = 0
t = 0

class Object():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.move = 0

    def add_img(self, address, x, y):
        self.img = address
        self.img = pygame.transform.scale(self.img, (x,y))
        self.size_x, self.size_y = self.img.get_size()
    
    def show(self):
        screen.blit(self.img, (self.x, self.y))

class Enemy(Object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.start_x = 0
        self.start_y = 0
        self.end_x = 0
        self.end_y = 0
        self.t = 0
        self.move = 0.3 + (round_check * 0.1)

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
ship.add_img(ship_img,50,50)
ship.x = round(size[0] / 2) - round(ship.size_x / 2)
ship.y = size[1] - ship.size_y - 100
ship.move = 8


missile_list = []
enemy_missile_list = []
enemy_list = []

attack = False
game_over = 0
game_clear = 0
score = 0
check = 1
system_exit = 0
round_check = 1
k = 0

while system_exit == 0:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                system_exit = 1
    
    screen.fill(black)
    font_press = pygame.font.Font('font/D2Coding-Ver1.3.2-20180524.ttc',20)
    text_press = font_press.render('Press s button', True, (255,0,0))
    font_title = pygame.font.Font('font/D2Coding-Ver1.3.2-20180524.ttc',40)
    text_title = font_title.render('좌우키 : 이동', True, white)
    text_title2 = font_title.render('S키 : 공격',True, white)
    screen.blit(text_title, ((size[0]/2) - 125, size[1]/2 - 200))
    screen.blit(text_title2, ((size[0]/2) - 100, size[1]/2 - 150))
    screen.blit(text_press, ((size[0]/2) - 65, size[1]/2 + 200))
    pygame.display.flip()

t = 0
# 메인 이벤트 시작
start_time = datetime.now()
flag = True
while flag:
    clock.tick(30)
    
    # 키 입력 반응
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            flag = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                to_x -= ship.move
            elif event.key == pygame.K_RIGHT:
                to_x += ship.move
            elif event.key == pygame.K_s:
                attack = True
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                to_x = 0
            elif event.key == pygame.K_s:
                attack = False
    
    if ship.x < 0:
        ship.x = 0
    elif ship.x > size[0] - ship.size_x:
        ship.x = size[0] - ship.size_x
    
    # to_x 만큼 ship 위치 이동
    ship.x += to_x

    # 시간
    current_time = datetime.now()
    delta_time = round((current_time - start_time).total_seconds())
    
    # 공격
    if attack == True and len(missile_list) < 2:
        missile = Object()
        missile.add_img(laser_img,5,10)
        missile.move = 20
        missile.x = ship.x + round(ship.size_x / 2) - round(missile.size_x / 2)
        missile.y = ship.y
        missile_list.append(missile)
        attack = False
    
    # 공격 관리
    delete_missile = []
    for i in range(len(missile_list)):
        m = missile_list[i]
        m.y -= m.move
        if m.y <= -m.size_y:
            delete_missile.append(i)
    
    try:
        delete_missile.reverse()
        for d in delete_missile:
            del missile_list[d]
    except:
        pass

    # 적 관리
    delete_enemy = []
    if check == 1:
        for i in range(1,17):
            if i < 5:
                enemy = Enemy()
                enemy.add_img(enemy1_img,30,30)
                enemy.start_x = 0 - enemy.size_x
                enemy.start_y = 700
                enemy.end_x = (75 * i) - 20
                enemy.end_y = 100
                enemy_list.append(enemy)
            elif i < 9:
                enemy = Enemy()
                enemy.add_img(enemy2_img,30,30)
                enemy.start_x = size[0]
                enemy.start_y = 700
                enemy.end_x = (75 * (i-4)) + 20
                enemy.end_y = 150
                enemy_list.append(enemy)
            elif i < 13:
                enemy = Enemy()
                enemy.add_img(enemy1_img,30,30)
                enemy.start_x = 0 - enemy.size_x
                enemy.start_y = 900
                enemy.end_x = (75 * (i-8)) - 20
                enemy.end_y = 200
                enemy_list.append(enemy)
            else:
                enemy = Enemy()
                enemy.add_img(enemy2_img,30,30)
                enemy.start_x = size[0]
                enemy.start_y = 900
                enemy.end_x = (75 * (i-12)) + 20
                enemy.end_y = 250
                enemy_list.append(enemy)
        check = 0
    
    if len(enemy_list) == 0:
        check = 1
        round_check += 1

    if round_check == 11 and enemy_list == []:
        game_clear = 1
        flag = False

    for i in range(len(enemy_list)):
        e = enemy_list[i]
        if e.t < 1:
            e.t += 0.03
            e.x = ((1-e.t) ** 2)*e.start_x + 2 * (1-e.t) * e.t * 200 + (e.t ** 2) * e.end_x
            e.y = ((1-e.t) ** 2)*e.start_y + 2 * (1-e.t) * e.t * 400 + (e.t ** 2) * e.end_y
        
    for i in enemy_list:
        if i.t >= 1:
            i.y += i.move
        if i.y >= size[1]:
            flag = False
            game_over = 1
    
    for i in enemy_list:
        if random.random() > 0.997 - (0.001 * round_check)  and i.t >= 1:
            enemy_missile = Object()
            enemy_missile.add_img(enemy_laser_img,2,10)
            enemy_missile.move = 5
            enemy_missile.x = i.x + 15
            enemy_missile.y = i.y + 20
            enemy_missile_list.append(enemy_missile)

    delete_enemy_missile_list = []
    for i in range(len(enemy_missile_list)):
        em = enemy_missile_list[i]
        em.y += em.move
        if em.y >= size[1]:
            delete_enemy_missile_list.append(i)

    try:
        delete_enemy_missile_list.reverse()
        for d in delete_enemy_missile_list:
            del enemy_missile_list[d]
    except:
        pass

    # 피격 관리
    for i in range(len(enemy_list)):
        e = enemy_list[i]
        if crash(e,ship) == True:
            flag = False
            game_over = 1
    
    delete_missile_list = []
    delete_enemy_list = []

    for i in range(len(missile_list)):
        for j in range(len(enemy_list)):
            m = missile_list[i]
            e = enemy_list[j]
            if crash(m,e) == True:
                delete_enemy_list.append(j)
                delete_missile_list.append(i)
    
    for i in range(len(enemy_missile_list)):
        el = enemy_missile_list[i]
        if crash(el,ship) == True:
            flag = False
            game_over = 1

    delete_missile_list = list(set(delete_missile_list))
    delete_enemy_list = list(set(delete_enemy_list))
    
    try:
        delete_missile_list.reverse()
        delete_enemy_list.reverse()
        for dl in delete_missile_list:
            del missile_list[dl]
        for de in delete_enemy_list:
            del enemy_list[de]
            score += int((100 * random.random()) // 1)
    
    except:
        pass
        
        
    # 출력
    screen.blit(background, (0,0))
    ship.show()
    for m in missile_list:
        m.show()
    for e in enemy_list:
        e.show()
    for em in enemy_missile_list:
        em.show()
    
    font = pygame.font.Font('font/D2Coding-Ver1.3.2-20180524.ttc',20)
    text_score = font.render('score : {}'.format(score),True, white)
    text_round = font.render('round : {}'.format(round_check),True, white)
    screen.blit(text_score, (10,10))
    screen.blit(text_round, (260,10))
    pygame.display.flip()


    while game_over == 1:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = 0
        screen.fill(black)
        font = pygame.font.Font('font/D2Coding-Ver1.3.2-20180524.ttc',40)
        text_over = font.render('GAME OVER',True,white)
        text_over_score = font.render('점수 : {}'.format(score),True, white)
        screen.blit(text_over,(size[0]/2 - 90, size[1]/2 - 20))
        screen.blit(text_over_score,(size[0]/2 - 100, size[1]/2 + 40))
        pygame.display.flip()

    while game_clear == 1:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_clear = 0
        screen.fill(black)
        font = pygame.font.Font('font/D2Coding-Ver1.3.2-20180524.ttc',40)
        text_over = font.render('CLEAR',True,white)
        text_end_score = font.render('점수 : {}'.format(score),True, white)
        screen.blit(text_over,(size[0]/2 - 50, size[1]/2 - 40))
        screen.blit(text_end_score,(size[0]/2 - 100, size[1]/2 + 40))
        pygame.display.flip()

pygame.quit()

