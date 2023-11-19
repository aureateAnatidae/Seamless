import pygame
import random

pygame.init()


font = pygame.font.Font('freesansbold.ttf', 20)

# Basic parameters of the screen
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

clock = pygame.time.Clock()
FPS = 60
global running
running = True

global difficulty
difficulty = "normal"
global difficulty_settings
global ball_speed
ball_speed = 6

difficulty_settings = {
    "easy": 4,
    "normal": 6,
    "hard": 8
}


class Paddle:
    def __init__(self, x, y, width, height, speed):
        self.x = x
        self.y = y

        self.width = width
        self.height = height

        self.speed = speed
        self.color = (255, 255, 255)

        self.rect = pygame.Rect(x, y, width, height)

        self.draw = pygame.draw.rect(screen, self.color, self.rect)

    # Used to display the object on the screen
    def display(self):
        self.draw = pygame.draw.rect(screen, self.color, self.rect)

    def update(self, xFac):
        self.x = self.x + self.speed*xFac

        # left
        if self.x <= 0:
            self.x = 0
        # right
        elif self.x + self.width >= WIDTH:
            self.x = WIDTH-self.width

        # Update
        self.rect = (self.x, self.y, self.width, self.height)

    def displayScore(self, text, score, x, y, color):
        text = font.render(text+str(score), True, color)
        textRect = text.get_rect()
        textRect.center = (x, y)

        screen.blit(text, textRect)

    def get_rect(self):
        return self.rect


class Ball:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = (255, 255, 255)
        self.xFac = 1
        self.yFac = -1
        self.ball = pygame.draw.circle(
            screen, self.color, (self.x, self.y), self.radius)

    def display(self):
        self.ball = pygame.draw.circle(
            screen, self.color, (self.x, self.y), self.radius)

    def update(self):
        # ball_speed = difficulty_settings[difficulty]
        global ball_speed

        self.x += ball_speed*self.xFac
        self.y += ball_speed*self.yFac

        if self.y >= HEIGHT:
            return 1

        if self.y <= 0:
            self.yFac *= -1

        if self.x <= 0 or self.x >= WIDTH:
            self.xFac *= -1

        else:
            return 0

    def reset(self):
        self.x = WIDTH//2
        self.y = HEIGHT//2
        self.xFac = random.choice([-1, 1])
        self.yFac = random.choice([-1, 1])

    # Used to reflect the ball along the X-axis
    def hit(self, sides, playerY):
        if sides:
            self.xFac *= -1
        self.yFac *= -1
        self.y = playerY - 10

    def get_rect(self):
        return self.ball


class difficulty_indicator:
    def __init__(self, difficulty):
        self.color_map = {"easy": (0, 255, 0), "normal": (
            255, 255, 0), "hard": (255, 0, 0)}
        self.rect = pygame.Rect(20, 20, 15, 15)
        self.difficulty = difficulty
        self.color = self.color_map[self.difficulty]

    def display(self):
        pygame.draw.rect(screen, self.color_map[difficulty], self.rect)


def main(second_cap=100):
    global difficulty
    global running
    running = True

    start_state = True
    countdown_timer = FPS * 3

    frame_cap = second_cap * FPS

    # Defining the objects
    player = Paddle(0, 500, 100, 10, 10)
    ball = Ball(WIDTH//2, HEIGHT//2, 7)

    # Initial parameters of the players
    Score = 0
    paddleVel = 0
    frames = 0
    difficultyind = difficulty_indicator(difficulty)
    left_key_down = False
    right_key_down = False

    while running:
        if frames >= frame_cap:
            running = False

        screen.fill((0, 0, 0))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    left_key_down = True
                if event.key == pygame.K_RIGHT:
                    right_key_down = True
                if event.key == pygame.K_1:
                    difficulty = "easy"
                if event.key == pygame.K_2:
                    difficulty = "normal"
                if event.key == pygame.K_3:
                    difficulty = "hard"

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    left_key_down = False
                if event.key == pygame.K_RIGHT:
                    right_key_down = False

        # ball paddle collision
        if pygame.Rect.colliderect(ball.get_rect(), player.get_rect()):
            if ((ball.x == player.x or ball.x == player.x + player.width) and player.y <= ball.y <= player.y+player.height):
                ball.hit(True, player.y)
            else:
                ball.hit(False, player.y)

        if start_state:
            text_display(
                f"Start in: {countdown_timer // FPS}", 400, 300, (255, 255, 255))
            countdown_timer -= 1
            if countdown_timer <= 0:
                start_state = False
        else:
            frames += 1

            if left_key_down:
                paddleVel = -1
            elif right_key_down:
                paddleVel = 1
            else:
                paddleVel = 0

            # Updating the objects
            player.update(paddleVel)
            point = ball.update()

            if point:
                Score += 1
                ball.reset()

            # Displaying the objects on the screen
            player.display()
            ball.display()
            difficultyind.display()

        # Displaying the scores of the players
        # player.displayScore("Score : ",
        #                    Score, 100, 20, (255, 255, 255))

        pygame.display.update()
        clock.tick(FPS)


def text_display(text, x, y, color):
    text = font.render(text, True, color)
    textRect = text.get_rect()
    textRect.center = (x, y)

    screen.blit(text, textRect)


if __name__ == "__main__":
    main()
    pygame.quit()
