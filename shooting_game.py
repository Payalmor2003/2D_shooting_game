import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH = 600
HEIGHT = 800
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Shooting Game")
clock = pygame.time.Clock()

# Load fonts
font = pygame.font.SysFont(None, 40)

# Load assets (player, bullet, enemy images)
player_img = pygame.Surface((50, 40))
player_img.fill((0, 255, 0))  # Green player

bullet_img = pygame.Surface((5, 10))
bullet_img.fill(WHITE)  # White bullet

enemy_img = pygame.Surface((40, 30))
enemy_img.fill(RED)  # Red enemy

# Game Variables
score = 0
game_over = False

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed = 7

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        bullets.add(bullet)
        all_sprites.add(bullet)


# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -10

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()


# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speedy = random.randint(2, 5)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.rect.y = random.randint(-100, -40)
            self.rect.x = random.randint(0, WIDTH - self.rect.width)


# Groups to manage sprites
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Create player
player = Player()
all_sprites.add(player)

# Create initial enemies
for _ in range(6):
    enemy = Enemy()
    enemies.add(enemy)
    all_sprites.add(enemy)


# Game loop
running = True
while running:
    clock.tick(FPS)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    if not game_over:
        # Update all sprites
        all_sprites.update()

        # Check for bullet-enemy collisions
        hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
        for hit in hits:
            score += 10
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        # Check for player-enemy collisions
        if pygame.sprite.spritecollideany(player, enemies):
            game_over = True

    # Draw everything
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # Display score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Show Game Over screen
    if game_over:
        over_text = font.render("GAME OVER! Press R to Restart", True, RED)
        screen.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 2))

    pygame.display.flip()

    # Restart game after Game Over
    if game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            score = 0
            game_over = False
            for sprite in all_sprites:
                sprite.kill()
            player = Player()
            all_sprites.add(player)
            for _ in range(6):
                enemy = Enemy()
                enemies.add(enemy)
                all_sprites.add(enemy)

pygame.quit()
sys.exit()
