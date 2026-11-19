# Jacob Arzadon
# 11/16/2026
import pygame
import random
import sys

pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chicken Drop!")

clock = pygame.time.Clock()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (141, 247, 242)
GREEN = (31, 99, 30)
RED = (200, 40, 40)
YELLOW = (255, 220, 50)
POWER_BLUE = (30, 100, 255)

# Fonts
bigFont = pygame.font.SysFont(None, 70)
smallFont = pygame.font.SysFont(None, 40)

chicken = pygame.image.load("chicken.png")
chicken = pygame.transform.scale(chicken, (60, 60))


# VARIABLES

numOfChickens = 5

startX = []
startY = []
speed = []

score = 0

gameOver = False
replayScreen = False

# Power-up variables
powerUpActive = False
powerUpX = 0
powerUpY = 0

powerUpRadius = 25

slowMotion = False
slowMotionTimer = 0

powerUpSpawnTimer = 0
powerUpSpawnDelay = 5000

slowMotionDuration = 3000


# 3. CREATE CHICKENS

def reset_chickens():

    global startX, startY, speed

    startX = []
    startY = []
    speed = []

    for i in range(numOfChickens):

        startX.append(
            random.randint(0, WIDTH - chicken.get_width())
        )

        startY.append(
            random.randint(-500, -60)
        )

        speed.append(
            random.randint(1, 3) + random.random()
        )

reset_chickens()

# CREATE POWER-UP

def spawn_powerup():

    global powerUpActive, powerUpX, powerUpY

    powerUpX = random.randint(
        powerUpRadius,
        WIDTH - powerUpRadius
    )

    powerUpY = random.randint(
        100,
        HEIGHT - 150
    )

    powerUpActive = True

while not gameOver:

    dt = clock.tick(60)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            gameOver = True

        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:

                mouseX, mouseY = pygame.mouse.get_pos()

                if not replayScreen:

                    # Check power up click
                    if powerUpActive:

                        distance = (
                            (mouseX - powerUpX) ** 2 +
                            (mouseY - powerUpY) ** 2
                        )

                        if distance <= powerUpRadius ** 2:

                            powerUpActive = False
                            slowMotion = True

                            slowMotionTimer = pygame.time.get_ticks()

                            powerUpSpawnTimer = pygame.time.get_ticks()

                    # Check chicken clicks
                    for i in range(numOfChickens):

                        chickenRect = pygame.Rect(
                            startX[i],
                            startY[i],
                            chicken.get_width(),
                            chicken.get_height()
                        )

                        if chickenRect.collidepoint(mouseX, mouseY):

                            score += 1

                            startX[i] = random.randint(
                                0,
                                WIDTH - chicken.get_width()
                            )

                            startY[i] = random.randint(-500, -60)

                            speed[i] = (
                                random.randint(1, 3) +
                                random.random()
                            )

                            break

                else:

                    # Replay button
                    if WIDTH // 2 - 100 < mouseX < WIDTH // 2 + 100:

                        if 320 < mouseY < 380:

                            score = 0
                            reset_chickens()

                            replayScreen = False
                            slowMotion = False
                            powerUpActive = False

                            powerUpSpawnTimer = pygame.time.get_ticks()

                        elif 400 < mouseY < 460:

                            gameOver = True


    if not replayScreen:

        currentTime = pygame.time.get_ticks()

        # Check slow motion timer
        if slowMotion:

            if currentTime - slowMotionTimer >= slowMotionDuration:

                slowMotion = False

        # Spawn power-up if one isn't active
        if not powerUpActive and not slowMotion:

            if currentTime - powerUpSpawnTimer >= powerUpSpawnDelay:

                spawn_powerup()

                powerUpSpawnDelay = random.randint(5000, 10000)

        # Move chickens
        for i in range(numOfChickens):

            # Slow down chickens during power-up
            if slowMotion:

                startY[i] += speed[i] * 0.3

            else:

                startY[i] += speed[i]

            # Check if chicken reached bottom
            if startY[i] + chicken.get_height() >= HEIGHT:

                replayScreen = True
                break

    if not replayScreen:

        screen.fill(BLUE)

        # Draw grass
        pygame.draw.rect(
            screen,
            GREEN,
            (0, 400, WIDTH, 200)
        )

        # Draw Chickens
        for i in range(numOfChickens):

            screen.blit(
                chicken,
                (startX[i], startY[i])
            )

        # Draw Score
        scoreText = smallFont.render(
            "Score: " + str(score),
            True,
            WHITE
        )

        screen.blit(scoreText, (20, 20))

        # Draw Power up
        if powerUpActive:

            pygame.draw.circle(
                screen,
                POWER_BLUE,
                (powerUpX, powerUpY),
                powerUpRadius
            )

            powerText = smallFont.render(
                "S",
                True,
                WHITE
            )

            screen.blit(
                powerText,
                (
                    powerUpX - powerText.get_width() // 2,
                    powerUpY - powerText.get_height() // 2
                )
            )

        # Show slow motion status
        if slowMotion:

            slowText = smallFont.render(
                "SLOW MOTION!",
                True,
                YELLOW
            )

            screen.blit(
                slowText,
                (WIDTH - slowText.get_width() - 20, 20)
            )

    else:

        screen.fill(RED)

        title = bigFont.render(
            "GAME OVER!",
            True,
            WHITE
        )

        scoreText = smallFont.render(
            "Final Score: " + str(score),
            True,
            WHITE
        )

        replayText = smallFont.render(
            "PLAY AGAIN",
            True,
            WHITE
        )

        quitText = smallFont.render(
            "QUIT",
            True,
            WHITE
        )

        screen.blit(
            title,
            (WIDTH // 2 - title.get_width() // 2, 150)
        )

        screen.blit(
            scoreText,
            (WIDTH // 2 - scoreText.get_width() // 2, 240)
        )

        pygame.draw.rect(
            screen,
            GREEN,
            (WIDTH // 2 - 100, 320, 200, 60)
        )

        pygame.draw.rect(
            screen,
            BLACK,
            (WIDTH // 2 - 100, 400, 200, 60)
        )

        screen.blit(
            replayText,
            (WIDTH // 2 - replayText.get_width() // 2, 335)
        )

        screen.blit(
            quitText,
            (WIDTH // 2 - quitText.get_width() // 2, 415)
        )

    pygame.display.flip()

pygame.quit()
sys.exit()