import pygame

# 1. 초기화
pygame.init() # 파이게임 내의 init 함수 실행 > 초기화

# 2. 게임 화면 설정
size = [400, 900]
screen = pygame.display.set_mode(size) # 400 x 900 해상도의 창을 만듬

title = 'Pygame Ex'
pygame.display.set_caption(title) # 제목 설정

# 3. 게임 내부에서의 설정
clock = pygame.time.Clock() # 시계

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

spaceship = Object()
spaceship.add_img("C:/Users/Administrator/Desktop/12-21/simple_game/spaceship.png",50,50)
spaceship.x = round(size[0] / 2) - round(spaceship.size_x / 2)
spaceship.y = size[1] - spaceship.size_y - 30
spaceship.move = 5 # 속도

to_x = 0
to_y = 0

space_move = False
"""
불러올 이미지(오브젝트)가 많기 때문에 클래스화 하여 사용
#spaceship = pygame.image.load("C:/Users/Administrator/Desktop/12-19/simple_game/spaceship.png").convert_alpha() # 이미지 경로 입력, \를 /로 바꿔줘야 함, png 파일 사용 시 convert_alpha() 붙여줘야 함
#spaceship = pygame.transform.scale(spaceship, (50, 50))
#spaceship_size_x, spaceship_size_y = spaceship.get_size()
#spaceship_x = round(size[0] / 2) - round(spaceship_size_x / 2) # round = 반올림
#spaceship_y = size[1] - spaceship_size_y - 30
"""

color = (0, 0, 0) # RGB 검정색

k = 0

# 4. 메인 이벤트
system_exit = 0 # 탈줄구 마련
while system_exit == 0:
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
    spaceship.x += to_x
    spaceship.y += to_y
    
    
    missile_list = []
    if space_move == True:
        missile = Object()
        missile.add_img('C:/Users/Administrator/Desktop/12-21/simple_game/missile.png',10,20)
        missile.move = 10
        missile.x = spaceship.x + round(spaceship.size_x / 2) - round(missile.size_x / 2)
        missile.y = spaceship.y
        missile_list.append(missile)
    
    delete_list = []
    for i in range(len(missile_list)):
        m = missile_list[i]
        m.y -= m.move
        if m.y <= -m.size_y:
            delete_list.append(m)
    
    delete_list.reverse()
    for d in delete_list:
        del missile_list[i]
            
    # 4-4. 전사작업(그리기)
    screen.fill(color) # 배경 color로 채우기
    spaceship.show() # 지정한 x,y자리에 배치
    for m in missile_list:
        m.show()
        
        
    # 4-5. 업데이트
    pygame.display.flip() # while문 내의 변경점 등을 화면에 보여주겠다
    
    
# 5. 종료
pygame.quit() # 종료 함수