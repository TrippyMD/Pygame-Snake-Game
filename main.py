
import pygame
from pygame.locals import *
import time
import random

SIZE = 32
BACKGROUND_COLOR = (190,180,199)


class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resourses/apple.png")
        self.x = SIZE * 3
        self.y = SIZE * 3

    def move(self):
        self.x = random.randint(0,24) * SIZE
        self.y = random.randint(0,19) * SIZE

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()


class Snake:
    def __init__(self, parent_screen, length):
        self.parent_screen = parent_screen
        self.length = length
        self.block = pygame.image.load("resourses/block.png").convert()
        self.x = [SIZE]*length
        self.y = [SIZE]*length
        self.direction = "right"

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def move_up(self):
        self.direction = "up"

    def move_down(self):
        self.direction = "down"

    def move_left(self):
        self.direction = "left"

    def move_right(self):
        self.direction = "right"

    def walk(self):
        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == "up":
            self.y[0] -= SIZE
        if self.direction == "down":
            self.y[0] += SIZE
        if self.direction == "left":
            self.x[0] -= SIZE
        if self.direction == "right":
            self.x[0] += SIZE
        self.draw()


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.surface = pygame.display.set_mode((800,640))
        self.surface.fill(BACKGROUND_COLOR)
        self.play_background_music()

        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

        pygame.display.flip()

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    def render_background(self):
        bg = pygame.image.load("resourses/bg.png")
        self.surface.blit(bg, (0,0))

    def play_background_music(self):
        pygame.mixer.music.load("resourses/bg_music.mp3")
        pygame.mixer.music.play()

    def play_sound(self, value):
        if value == "ding":
            sound = pygame.mixer.Sound("resourses/ding.wav")
            pygame.mixer.Sound.play(sound)
        elif value == "crash":
            sound = pygame.mixer.Sound("resourses/crash.mp3")
            pygame.mixer.Sound.play(sound)

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound("ding")
            self.snake.increase_length()
            self.apple.move()

        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound("crash")
                raise "Game over"

    def display_score(self):
        font = pygame.font.SysFont('papyrus', 30)
        score = font.render(f"Score: {self.snake.length}", True, (10,20,30))
        self.surface.blit(score, (600,30))

    def reset(self):
        self.snake = Snake(self.surface, 1)
        pygame.display.flip()

    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('papyrus', 30)
        line1 = font.render(f"Score: {self.snake.length}", True, (10,20,30))
        self.surface.blit(line1, (350,230))
        line2 = font.render(f"To restart press Enter, or press Esc to Quit", True, (10,20,30))
        self.surface.blit(line2, (90,430))
        pygame.mixer.music.pause()
        pygame.display.flip()

    def run(self):
        running = True
        pause = False
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RETURN:
                        pause = False
                        pygame.mixer.music.unpause()
                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        if event.key == K_RIGHT:
                            self.snake.move_right()

                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()
            except:
                self.show_game_over()
                pause = True
                self.reset()
            time.sleep(0.3)


if __name__ == "__main__":
    game = Game()
    game.run()
