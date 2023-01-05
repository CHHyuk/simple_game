import pygame
import random
import time
from datetime import datetime

# 1. 초기화
pygame.init() # 파이게임 내의 init 함수 실행 > 초기화

# 2. 게임 화면 설정
size = [400, 900] # 가로, 세로 (좌측 상단이 0, 0)
screen = pygame.display.set_mode(size) # 400 x 900 해상도의 창을 만듬

title = 'Pygame Ex'
pygame.display.set_caption(title) # 제목 설정

# 3. 게임 내부에서의 설정
clock = pygame.time.Clock() # 시계

class Object: # 이미지 클래스
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
        
def crash(a, b):
    if (a.x - b.size_x <= b.x) and (b.x <= a.x + a.size_x): # 충돌 범위 설정
        if (a.y - b.size_y <= b.y) and (b.y <= a.y + a.size_y): # 충돌 범위 설정
            return True
        else:
            return False
    else:
        return False

spaceship = Object()
spaceship.add_img("C:/git/simple_game/spaceship.png",50,50)
spaceship.x = round(size[0] / 2) - round(spaceship.size_x / 2)
spaceship.y = size[1] - spaceship.size_y - 30
spaceship.move = 5 # 속도

left_move = False
right_move = False
space_move = False

to_x = 0
to_y = 0
"""
불러올 이미지(오브젝트)가 많기 때문에 클래스화 하여 사용
#spaceship = pygame.image.load("C:/Users/Administrator/Desktop/12-19/simple_game/spaceship.png").convert_alpha() # 이미지 경로 입력, \를 /로 바꿔줘야 함, png 파일 사용 시 convert_alpha() 붙여줘야 함
#spaceship = pygame.transform.scale(spaceship, (50, 50))
#spaceship_size_x, spaceship_size_y = spaceship.get_size()
#spaceship_x = round(size[0] / 2) - round(spaceship_size_x / 2) # round = 반올림
#spaceship_y = size[1] - spaceship_size_y - 30
"""

white = (255, 255, 255)
color = (21, 0, 50) # 배경색
yellow = (255, 255, 0)
red = (255, 0, 0) # RGB

missile_list = []
enemy_list = []
k = 0

game_over = 0

score = 0 # 미사일로 적 제거 시 score 1 증가
miss = 0 # 적이 화면 밖으로 나갈 시 miss 1 증가

# 시작 전 대기
system_exit = 0
while system_exit == 0:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # x 버튼 클릭
            pygame.quit()
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                system_exit = 1
    screen.fill(color)
    font  = pygame.font.Font("C:/git/simple_game/D2Coding-Ver1.3.2-20180524/D2Coding/D2Coding-Ver1.3.2-20180524.ttc", 40)
    text = font.render("press space!", True, white)
    screen.blit(text, (90, size[1]/2 - 50))
    pygame.display.flip()


# 4. 메인 이벤트
start_time = datetime.now()
system_exit = 0 # 탈줄구 마련
while system_exit == 0:
#    print('score : {}'.format(score))
#    print('miss : {}'.format(miss))

    # 4-1. FPS 설정
    clock.tick(60) # FPS 60으로 설정, 1초에 60번 while문 반복하겠다.
    
    # 4-2. 입력장치의 감지
    for event in pygame.event.get(): # 키보드, 마우스 동작 감지, get해온다(가져온다), 여러 입력 동시에 가져올 수 있음
        if event.type == pygame.QUIT: # 대문자 QUIT = 상태를 나타냄, quit()는 프로그램 종료 함수
            system_exit = 1 # 종료(while문 종료)
        
        if event.type == pygame.KEYDOWN: # 키다운중일 경우
            if event.key == pygame.K_LEFT:
                to_x -= spaceship.move
            elif event.key == pygame.K_RIGHT:
                to_x += spaceship.move
            elif event.key == pygame.K_UP:
                to_y -= spaceship.move
            elif event.key == pygame.K_DOWN:
                to_y += spaceship.move
            elif event.key == pygame.K_SPACE:
                space_move = True
                
        
        if event.type == pygame.KEYUP: # 키업중일 경우
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                to_x = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                to_y = 0
            elif event.key == pygame.K_SPACE:
                space_move = False
    
    # 화면 밖으로 spaceship이 나가지 못하게 제한
    if spaceship.x < 0:
        spaceship.x = 0
    elif spaceship.x > size[0] - spaceship.size_x:
        spaceship.x = size[0] - spaceship.size_x
    
    if spaceship.y < 0:
        spaceship.y = 0
    elif spaceship.y > size[1] - spaceship.size_y:
        spaceship.y = size[1] - spaceship.size_y
        
    # 4-3. 입력, 시간에 따른 변화
    current_time = datetime.now()
    delta_time = round((current_time - start_time).total_seconds())

    
    spaceship.x += to_x
    spaceship.y += to_y
    
    
    if space_move == True:
        missile = Object()
        missile.add_img('C:/git/simple_game/missile.png',10,20)
        missile.move = 10
        missile.x = spaceship.x + round(spaceship.size_x / 2) - round(missile.size_x / 2)
        missile.y = spaceship.y
        missile_list.append(missile)
        space_move = False
    
    k += 1

    delete_list = []
    for i in range(len(missile_list)):
        m = missile_list[i]
        m.y -= m.move
        if m.y <= -m.size_y:
            delete_list.append(i)
    try:
        delete_list.reverse()
        for d in delete_list:
            del missile_list[d]
    except:
        pass
    
    delete_list2 = []
    for i in range(len(enemy_list)):
        e = enemy_list[i]
        e.y += e.move
        if e.y >= size[1]:
            delete_list2.append(i)
    try:
        delete_list2.reverse()
        for d in delete_list2:
            del enemy_list[d]
            miss += 1
    except:
        pass
    
    delete_missile_list = []
    delete_enemy_list = []

    for i in range(len(missile_list)):
        for j in range(len(enemy_list)):
            m = missile_list[i]
            e = enemy_list[j]
            if crash(m,e) == True:
                delete_missile_list.append(i)
                delete_enemy_list.append(j)

    delete_missile_list = list(set(delete_missile_list))
    delete_enemy_list = list(set(delete_enemy_list))

    try:
        delete_missile_list.reverse()
        delete_enemy_list.reverse()
        for dm in delete_missile_list:
            del missile_list[dm]
        for de in delete_enemy_list:
            del enemy_list[de]
            score += 1
    except:
        pass

    for i in range(len(enemy_list)):
        e = enemy_list[i]
        if crash(e,spaceship) == True:
            system_exit = 1
            game_over = 1
            time.sleep(1)
    
    if random.random() > 0.97:
        enemy = Object()
        enemy.add_img('C:/git/simple_game/enemy.png',40,40)
        enemy.move = 2
        enemy.x = random.randrange(0 + spaceship.size_x, size[0]-enemy.size_x - spaceship.size_x)
        enemy.y = 15
        enemy_list.append(enemy)
    
    # 4-4. 전사작업(그리기)
    screen.fill(color) # 배경 color로 채우기
    spaceship.show() # 지정한 x,y자리에 배치
    for m in missile_list:
        m.show()
    for e in enemy_list:
        e.show()

    font = pygame.font.Font("C:/git/simple_game/D2Coding-Ver1.3.2-20180524/D2Coding/D2Coding-Ver1.3.2-20180524.ttc", 20)
    text_score = font.render('score : {}  miss : {}'.format(score,miss), True, yellow)
    screen.blit(text_score, (10,10))

    text_time = font.render('time : {}'.format(delta_time), True, white)
    screen.blit(text_time,(size[0] - 100, 10))
        
        
    # 4-5. 업데이트
    pygame.display.flip() # while문 내의 변경점 등을 화면에 보여주겠다
    
    
# 5. 종료
    while game_over == 1:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = 0
        screen.fill((61, 61, 61))
        font  = pygame.font.Font("C:/git/simple_game/D2Coding-Ver1.3.2-20180524/D2Coding/D2Coding-Ver1.3.2-20180524.ttc", 50)
        text = font.render("GAME OVER", True, red)
        screen.blit(text, (90, size[1]/2 - 50))
        pygame.display.flip()

pygame.quit()



"""
오브젝트 풀 (최적화 방법)
처음에 게임 로드할때 하나씩 생성을 해놔 > 복사
갤러그랑 똑같이 만들기
"""