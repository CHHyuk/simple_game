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
    
    def add_img(self, address, x, y):
        if address[-3:] == 'png':
            self.img = pygame.image.load(address).convert_alpha()
        else:
            self.img = pygame.image.load(address)
        self.img = pygame.transform.scale(self.img, (x,y))
        self.size_x, self.size_y = self.img.get_size()
        
    def locate(self,size,nx,ny):
        self.x = nx - round(self.size_x / 2)
        self.y = ny - round(self.size_y / 2) 

spaceship = Object()
spaceship.add_img("C:/Users/Administrator/Desktop/12-19/simple_game/spaceship.png",50,50)
spaceship.locate(size,200,800)
"""
불러올 이미지(오브젝트)가 많기 때문에 클래스화 하여 사용
#spaceship = pygame.image.load("C:/Users/Administrator/Desktop/12-19/simple_game/spaceship.png").convert_alpha() # 이미지 경로 입력, \를 /로 바꿔줘야 함, png 파일 사용 시 convert_alpha() 붙여줘야 함
#spaceship = pygame.transform.scale(spaceship, (50, 50))
#spaceship_size_x, spaceship_size_y = spaceship.get_size()
spaceship_x = round(size[0] / 2) - round(spaceship_size_x / 2) # round = 반올림
spaceship_y = size[1] - spaceship_size_y - 30
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
            
    # 4-3. 입력, 시간에 따른 변화
    
    # 4-4. 전사작업(그리기)
    screen.fill(color) # 배경 color로 채우기
    screen.blit(spaceship.img, (spaceship.x, spaceship.y)) # 지정한 x,y자리에 배치
    
    # 4-5. 업데이트
    pygame.display.flip() # while문 내의 변경점 등을 화면에 보여주겠다
    
    
# 5. 종료
pygame.quit() # 종료 함수