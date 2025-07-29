import pygame
import random

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Runner Game Simple")
clock = pygame.time.Clock()

# Colors
SKY_BLUE = (135, 206, 235)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
GROUND_COLOR = (0, 100, 0)

# Player
player = pygame.Rect(50, 300, 50, 50)
player_speed = 0
gravity = 1

# Obstacles (Multiple)
obstacles = []
obstacle_speed = 5

for i in range(3):
    x_pos = 800 + i * 300
    obstacle = pygame.Rect(x_pos, 300, 50, 50)
    obstacles.append(obstacle)

score = 0
high_score = 0

font = pygame.font.SysFont(None, 36)

running = True
game_over = False
paused = False

def draw_ground():
    pygame.draw.line(screen, GROUND_COLOR, (0, 350), (800, 350), 5)

def reset_game():
    global player, player_speed, obstacles, score, obstacle_speed, game_over
    player.topleft = (50, 300)
    player_speed = 0
    obstacles.clear()
    for i in range(3):
        x_pos = 800 + i * 300
        obstacle = pygame.Rect(x_pos, 300, 50, 50)
        obstacles.append(obstacle)
    score = 0
    obstacle_speed = 5
    game_over = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if not game_over and not paused:
                if event.key == pygame.K_SPACE and player.bottom >= 350:
                    player_speed = -15
            if event.key == pygame.K_p:
                paused = not paused
            if game_over and event.key == pygame.K_r:
                reset_game()

    if not paused and not game_over:
        player_speed += gravity
        player.y += player_speed
        if player.bottom > 350:
            player.bottom = 350
            player_speed = 0

        for obstacle in obstacles:
            obstacle.x -= obstacle_speed
            if obstacle.right < 0:
                obstacle.x = 800 + random.randint(200, 600)
                score += 1

                if score % 5 == 0:
                    obstacle_speed += 1

        for obstacle in obstacles:
            if player.colliderect(obstacle):
                game_over = True
                if score > high_score:
                    high_score = score

    screen.fill(SKY_BLUE)
    draw_ground()

    pygame.draw.rect(screen, RED, player)
    for obstacle in obstacles:
        pygame.draw.rect(screen, GREEN, obstacle)

    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))
    high_score_text = font.render(f"High Score: {high_score}", True, BLACK)
    screen.blit(high_score_text, (10, 40))

    if paused:
        pause_text = font.render("Paused - Press 'P' to Resume", True, BLACK)
        screen.blit(pause_text, (200, 180))

    if game_over:
        game_over_text = font.render("Game Over! Press 'R' to Restart", True, (255, 0, 0))
        screen.blit(game_over_text, (220, 180))

    pygame.display.flip()
    clock.tick(60)
