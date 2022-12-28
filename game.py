# Pygame шаблон - скелет для нового проекта Pygame
import pygame
import random
import os
import keyboard
from random import randint

from pygame.locals import (
    K_ESCAPE,
    QUIT,
    K_UP,
    K_LEFT,
    K_RIGHT,
    K_w,
    K_s,
    K_a,
    K_d,
)

WIDTH = 1920
HEIGHT = 1080
FPS = 120
# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
DARK_RED = (187,18,0)

pygame.init()
files = os.path.join(os.path.dirname(__file__), "files")
game_folder = os.path.dirname(__file__)

music = pygame.mixer.music.load(os.path.join(files,"sound.mp3"))
player_img = pygame.image.load(os.path.join(files,'guts.png'))
enemy_img = pygame.image.load(os.path.join(files,'enemy.png'))
health_img = pygame.image.load(os.path.join(files,'health.png'))
gameover_img = pygame.image.load(os.path.join(files,'gameover.png'))
#restart_img = pygame.image.load(os.path.join(files,'restart.png'))
fon_img = pygame.image.load(os.path.join(files,'fon.png'))
font_name = pygame.font.match_font((os.path.join(files,'DePixel.ttf')),12)

def draw_text(surf, text, size, x, y,text_surface1):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, text_surface1)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

class GameOver(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = gameover_img
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2,HEIGHT/2)

"""class Restart(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = restart_img
        self.rect = self.image.get_rect()
        self.rect.center = ((WIDTH/2)-280,(HEIGHT/2)+300)"""

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = fon_img
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

class Health(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = health_img
        self.rect = self.image.get_rect()

    def update1(self):
        self.rect.x = 1810
        self.rect.y = 1
    def update2(self):
        self.rect.x = 1700
        self.rect.y = 1
    def update3(self):
        self.rect.x = 1590
        self.rect.y = 1

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, 890)
        
    def update(self,pressed_keys):
    	if pressed_keys[K_a]:
    		self.rect.x -= 7
    	elif pressed_keys[K_d]:
    		self.rect.x += 7

    	if self.rect.left > WIDTH:
    		self.rect.right = 0
    	elif self.rect.right < 0:
    		self.rect.left = WIDTH

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(3, 10)
        self.speedx = random.randrange(-3, 6)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.bottom = y+70
        self.rect.centerx = x
        self.speedy = 0
        self.speedx = 0

    def update(self):
        if (self.speedy == 0) and (self.speedx == 0):
            a = True
        else:
            a = False

        if a == True:
            if pressed_keys[K_RIGHT]:
                self.speedx = 10
            elif pressed_keys[K_LEFT]:
                self.speedx = -10
            elif pressed_keys[K_UP]:
                self.speedy = -10
            else:
                self.kill()
            a = False

        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if (self.rect.left > WIDTH) or (self.rect.bottom > HEIGHT) or (self.rect.right < 0) or (self.rect.top < 0) or Life == 0:
            self.kill()
            a = True

# Создаем игру и окно

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
mobs,bullets,restart,player,background,health,gameover= pygame.sprite.Group(),pygame.sprite.Group(),pygame.sprite.Group(),pygame.sprite.Group(),pygame.sprite.Group(),pygame.sprite.Group(),pygame.sprite.Group()

health1,health2,health3 = Health(),Health(),Health()
player = Player()
#restart = Restart()
gameover = GameOver()
background = Background(fon_img, [0,0])
all_sprites.add(player)
all_sprites.add(health1)
all_sprites.add(health2)
all_sprites.add(health3)
pygame.mixer.music.play(-1, 0.0)

for i in range(10):
    mob = Mob()
    all_sprites.add(mob)
    mobs.add(mob)

# Цикл игры
Life,score = 1,0
kill,kill1 = False,False
running = True
while running:
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # проверка для закрытия окна
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_UP or event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):
                player.shoot()
            elif event.key == pygame.K_ESCAPE:
                running = False

    pressed_keys = pygame.key.get_pressed()
    mobs.update()
    bullets.update()
    if Life == 1:
        player.update(pressed_keys)
        health1.update1()
        health2.update2()
        health3.update3()
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        mob = Mob()
        all_sprites.add(mob)
        mobs.add(mob)
        score += 1

    # Проверка, не ударил ли моб игрока
    
    if Life == 1:
        hits = pygame.sprite.spritecollide(player, mobs, False)
        for i in range(1):
            if hits and (kill == False):
                health3.kill()
                kill = True
                hits = pygame.sprite.spritecollide(player, mobs, True)
                break
            elif hits and (kill == True) and (kill1 == False):
                health2.kill()
                kill1 = True
                hits = pygame.sprite.spritecollide(player, mobs, True)
                break
            elif hits and (kill1 == True):
                health1.kill()
                hits = pygame.sprite.spritecollide(player, mobs, True)
                player.kill()
                Life = 0
                all_sprites.add(gameover)
                #all_sprites.add(restart)
                break

    # Рендеринг
    screen.fill([255, 255, 255])
    screen.blit(background.image, background.rect)
    if Life == 1:
        draw_text(screen, str("Kills"), 55, 1850, 90, BLACK)
        draw_text(screen, str(score), 60, 1850, 130, DARK_RED)
        
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()