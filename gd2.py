import pygame
import sys
import random
import math

pygame.init()

WIDTH, HEIGHT = 900, 550
FPS = 60

PLAYER_SIZE = 30
GROUND_Y = HEIGHT - 50

WHITE = (255, 255, 255)
RED = (255, 60, 60)
CYAN = (0, 255, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Easy Dash Ultimate")

clock = pygame.time.Clock()

font = pygame.font.SysFont("arial", 40)
small_font = pygame.font.SysFont("arial", 24)

score = 0
try :
    with open("best_score.txt", "r") as f:
        best_score = int(f.read())
except:
    with open("best_score.txt", "w") as f:
        f.write("0")
    best_score = 0

player_x = 200
player_y = HEIGHT // 2

player_vel_y = 0
gravity = 1

wave = True
is_flying = False

obstacle_speed = 8
obstacle_x = WIDTH

gap = 300

trail = []
TRAIL_LENGTH = 40

particles = []

pulse = 0
rotation = 0
shake = 0


def spawn_obstacle():
    global obstacle_x
    global top_rect
    global bottom_rect

    width = random.randint(40, 100)

    top_height = random.randint(60, 220)

    bottom_y = top_height + gap
    bottom_height = HEIGHT - bottom_y

    obstacle_x = WIDTH

    top_rect = pygame.Rect(
        obstacle_x,
        0,
        width,
        top_height
    )

    bottom_rect = pygame.Rect(
        obstacle_x,
        bottom_y,
        width,
        bottom_height
    )


def add_particles(x, y):

    for _ in range(50):

        particles.append(
            [
                x,
                y,
                random.uniform(-8, 8),
                random.uniform(-8, 8),
                random.randint(20, 50)
            ]
        )


spawn_obstacle()

passed = False

while True:

    pulse += 0.01
    pulse += score/1000

    bg = (
        int(15 + 15 * math.sin(pulse)),
        0,
        int(25 + 25 * math.sin(pulse))
    )

    screen.fill(bg)

    vary=min(score,255)
    scale=random.randint(255-vary, 255)
    RED=(scale,int(scale*0.2),int(scale*0.2))
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE or event.key == pygame.K_w or event.key == pygame.K_p:
                is_flying = True

            if event.key == pygame.K_q:
                wave = not wave

        if event.type == pygame.KEYUP:

            if event.key == pygame.K_SPACE or event.key == pygame.K_w or event.key == pygame.K_p:
                is_flying = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            is_flying = True

        if event.type == pygame.MOUSEBUTTONUP:
            is_flying = False

    speed = obstacle_speed + math.ceil(math.sqrt(max(score, 1)))*3

    if wave:

        if is_flying:
            player_vel_y = -speed
        else:
            player_vel_y = speed

    else:

        if is_flying:
            player_vel_y -= gravity

        else:
            player_vel_y += gravity

        player_vel_y = max(-12, min(12, player_vel_y))

        rotation = player_vel_y * 3

    player_y += player_vel_y

    if player_y < 0:
        player_y = 0

    if player_y > GROUND_Y - PLAYER_SIZE:
        player_y = GROUND_Y - PLAYER_SIZE
        player_vel_y = 0

    obstacle_x -= speed

    top_rect.x = obstacle_x
    bottom_rect.x = obstacle_x

    if obstacle_x + top_rect.width < player_x and not passed:

        score += 1
        best_score = max(best_score, score)
        with open("best_score.txt", "w") as f:
            f.write(str(best_score))

        passed = True

        gap = max(180, int(gap * 0.99))

    if obstacle_x < -150:

        passed = False
        spawn_obstacle()

    trail.append(
        (
            player_x + PLAYER_SIZE // 2,
            player_y + PLAYER_SIZE // 2
        )
    )

    if len(trail) > TRAIL_LENGTH:
        trail.pop(0)

    colour_shift = pygame.time.get_ticks() / 300

    for i, pos in enumerate(trail):

        alpha = int(255 * (i / TRAIL_LENGTH))
        size = max(3, int(PLAYER_SIZE * i / TRAIL_LENGTH))

        r = int(128 + 127 * math.sin(colour_shift))
        g = int(128 + 127 * math.sin(colour_shift + 2))
        b = int(128 + 127 * math.sin(colour_shift + 4))

        surf = pygame.Surface((size, size), pygame.SRCALPHA)

        pygame.draw.circle(
            surf,
            (r, g, b, alpha),
            (size // 2, size // 2),
            size // 2,
        )

        screen.blit(
            surf,
            (
                pos[0] - size // 2,
                pos[1] - size // 2
            )
        )

    offset_x = 0
    offset_y = 0

    if shake > 0:

        offset_x = random.randint(-shake, shake)
        offset_y = random.randint(-shake, shake)

        shake -= 1

    glow_top = pygame.Surface(
        (top_rect.width + 20, top_rect.height + 20),
        pygame.SRCALPHA
    )

    glow_top.fill((255, 0, 0, 50))

    screen.blit(
        glow_top,
        (top_rect.x - 10, top_rect.y - 10)
    )

    glow_bottom = pygame.Surface(
        (bottom_rect.width + 20, bottom_rect.height + 20),
        pygame.SRCALPHA
    )

    glow_bottom.fill((255, 0, 0, 50))

    screen.blit(
        glow_bottom,
        (bottom_rect.x - 10, bottom_rect.y - 10)
    )

    pygame.draw.rect(screen, RED, top_rect)
    pygame.draw.rect(screen, RED, bottom_rect)

    player_rect = pygame.Rect(
        player_x,
        player_y,
        PLAYER_SIZE,
        PLAYER_SIZE
    )

    if wave:

        points = [
            (player_x + PLAYER_SIZE, player_y + PLAYER_SIZE // 2),
            (player_x, player_y),
            (player_x, player_y + PLAYER_SIZE)
        ]

        pygame.draw.polygon(
            screen,
            CYAN,
            points
        )

    else:

        surf = pygame.Surface(
            (PLAYER_SIZE * 2, PLAYER_SIZE * 2),
            pygame.SRCALPHA
        )

        pygame.draw.rect(
            surf,
            CYAN,
            (
                PLAYER_SIZE // 2,
                PLAYER_SIZE // 2,
                PLAYER_SIZE,
                PLAYER_SIZE
            )
        )

        rotated = pygame.transform.rotate(
            surf,
            rotation
        )

        rect = rotated.get_rect(
            center=(
                player_x + PLAYER_SIZE // 2 + offset_x,
                player_y + PLAYER_SIZE // 2 + offset_y
            )
        )

        screen.blit(rotated, rect)

    if player_rect.colliderect(top_rect) or player_rect.colliderect(bottom_rect):

        shake = 12

        add_particles(
            player_x + PLAYER_SIZE // 2,
            player_y + PLAYER_SIZE // 2
        )

        score = 0
        gap = 300

        player_y = HEIGHT // 2
        player_vel_y = 0

        passed = False

        trail.clear()

        spawn_obstacle()

    for p in particles[:]:

        p[0] += p[2]
        p[1] += p[3]

        p[4] -= 1

        pygame.draw.circle(
            screen,
            CYAN,
            (int(p[0]), int(p[1])),
            3
        )

        if p[4] <= 0:
            particles.remove(p)

    pygame.draw.rect(
        screen,
        WHITE,
        (
            0,
            GROUND_Y,
            WIDTH,
            HEIGHT - GROUND_Y
        )
    )

    score_text = font.render(
        f"Score: {score}",
        True,
        WHITE
    )

    best_text = small_font.render(
        f"Best: {best_score}",
        True,
        CYAN
    )

    mode_text = small_font.render(
        f"Mode: {'wave' if wave else 'ship'}",
        True,
        CYAN
    )

    screen.blit(score_text, (20, 20))
    screen.blit(best_text, (20, 70))
    screen.blit(mode_text, (20, 100))

    pygame.display.flip()
    clock.tick(FPS)
