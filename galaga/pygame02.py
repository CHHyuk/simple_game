import pygame

# 1. 초기화
pygame.init()

# 2. 게임 화면 설정
size = [1024, 768]
screen = pygame.display.set_mode(size)

title = '갤러그 만들기'
pygame.display.set_caption(title) 

# 3. 게임 초기 설정
clock = pygame.time.Clock()

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

# 4. 메인 이벤트