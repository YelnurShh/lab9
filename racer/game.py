import pygame, sys
from pygame.locals import *
import random, time

pygame.init()

# Background music 
pygame.mixer.music.load('/Users/elnrsahar/Desktop/Python tasks/lab8/racer/background.wav')
pygame.mixer.music.play(-1)

# FPS
FPS = 60
FramePerSec = pygame.time.Clock()

# Colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
COINS_FOR_SPEEDUP = 5  # 5 ұпай сайын жылдамдық артады

font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

class GameState:
    def __init__(self):
        self.speed = 5
        self.score = 0
        self.coins_collected = 0

game_state = GameState()

# Load images
def load_images():
    images = {
        "background": pygame.image.load('/Users/elnrsahar/Desktop/Python tasks/lab9/racer/AnimatedStreet.png'),
        "enemy": pygame.image.load('/Users/elnrsahar/Desktop/Python tasks/lab9/racer/Enemy.png'),
        "player": pygame.image.load('/Users/elnrsahar/Desktop/Python tasks/lab9/racer/Player.png'),
        "coin_gold": pygame.image.load('/Users/elnrsahar/Desktop/Python tasks/lab9/racer/Coin.png'),
        "coin_silver": pygame.image.load('/Users/elnrsahar/Desktop/Python tasks/lab9/racer/coin3.png'),
        "coin_bronze": pygame.image.load('/Users/elnrsahar/Desktop/Python tasks/lab9/racer/coin2.png'),
        "crash_sound": pygame.mixer.Sound('/Users/elnrsahar/Desktop/Python tasks/lab9/racer/crash.wav')
    }
    images["coin_gold"] = pygame.transform.scale(images["coin_gold"], (30, 30))
    images["coin_silver"] = pygame.transform.scale(images["coin_silver"], (30, 30))
    images["coin_bronze"] = pygame.transform.scale(images["coin_bronze"], (30, 30))
    return images

images = load_images()

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game")

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = images["enemy"]
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        self.rect.move_ip(0, game_state.speed)
        if self.rect.bottom > SCREEN_HEIGHT:
            game_state.score += 1
            if game_state.score % COINS_FOR_SPEEDUP == 0:  # Ұпай бойынша жылдамдықты арттыру
                game_state.speed += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = images["player"]
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0 and pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH and pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

class Coin(pygame.sprite.Sprite):
    def __init__(self, enemies, x_position, coin_type):
        super().__init__()
        self.coin_type = coin_type
        self.image = images[f"coin_{self.coin_type}"]
        self.value = {"gold": 3, "silver": 2, "bronze": 1}[self.coin_type]
        self.rect = self.image.get_rect()
        self.enemies = enemies  
        self.spawn_coin(x_position)

    def spawn_coin(self, x_position):
        """Монетаны дұшпанға тимейтіндей етіп орналастыру"""
        while True:
            y = random.randint(-200, -50)
            new_rect = pygame.Rect(x_position, y, self.rect.width, self.rect.height)

            
            if not any(new_rect.colliderect(enemy.rect) for enemy in self.enemies):
                self.rect.center = (x_position, y)
                break

    def move(self):
        self.rect.move_ip(0, game_state.speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.spawn_coin(self.rect.centerx)  


P1 = Player()
E1 = Enemy()


enemies = pygame.sprite.Group()
enemies.add(E1)

coins = pygame.sprite.Group()


coin_positions = [100, 200, 300]  
coin_types = ["gold", "silver", "bronze"]  

for i in range(3):  
    coins.add(Coin(enemies, coin_positions[i], coin_types[i]))

all_sprites = pygame.sprite.Group()
all_sprites.add(P1, E1, *coins)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    DISPLAYSURF.blit(images["background"], (0, 0))
    scores = font_small.render(f"Score: {game_state.score}", True, BLACK)
    coins_text = font_small.render(f"Coins: {game_state.coins_collected}", True, BLACK)
    DISPLAYSURF.blit(scores, (10, 10))
    DISPLAYSURF.blit(coins_text, (300, 10))

    for entity in all_sprites:
        entity.move()
        DISPLAYSURF.blit(entity.image, entity.rect)

    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.music.stop()
        images["crash_sound"].play()
        time.sleep(1)
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))
        pygame.display.update()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    for coin in coins:
        if P1.rect.colliderect(coin.rect):
            game_state.coins_collected += coin.value
            coin.rect.center = (coin.rect.centerx, random.randint(-200, -50))

            if game_state.coins_collected % COINS_FOR_SPEEDUP == 0:  # Әр 5 монета сайын
                game_state.speed += 2  #  Жылдамдық артады

    pygame.display.update()
    FramePerSec.tick(FPS)
