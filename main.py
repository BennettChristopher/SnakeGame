import pygame
from pygame.locals import *
import time
import random

size = 40  # dimension of block - 40x40px
bgcolour = (110, 110, 5)  # background colour
bg = pygame.image.load("resources/background.jpg")  # background image
font = "Arial"  # font


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("Snake Game")
        self.surface = pygame.display.set_mode((1200, 600))  # bg
        self.surface.fill(bgcolour)
        self.render_background()
        self.snake = Snake(self.surface, 2)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()
        self.pause = False

    def run(self):
        running = True
        self.pause = False
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RETURN:
                        self.pause = False
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
            if not self.pause:
                self.play()
                time.sleep(0.3)

    def eat(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + size:
            if y1 >= y2 and y1 < y2 + size:
                return True
        return False

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        if self.eat(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.snake.grow()
            self.apple.move()
            self.sound("eat")
        if self.collision():
            self.sound("crash")
        self.display()
        pygame.display.flip()  # refresh display

    def collision(self):
        for i in range(3, self.snake.length):
            if self.eat(
                self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]
            ):
                return True
        if not (0 <= self.snake.x[0] <= 1200 and 0 <= self.snake.y[0] <= 600):
            return True
        return False

    def game_over(self):
        self.render_background()
        font1 = pygame.font.SysFont(f"{font}", 100)
        font2 = pygame.font.SysFont(f"{font}", 40)
        message = font1.render(f"Game Over!", True, (225, 225, 225))
        message1 = font2.render(
            f"Your Score: {self.snake.length-2}", True, (225, 225, 225)
        )
        message2 = font2.render(
            f"Press ENTER to Try Again OR ESC to Quit...", True, (225, 225, 225)
        )
        self.surface.blit(message, (375, 200))
        self.surface.blit(message1, (500, 315))
        self.surface.blit(message2, (300, 525))
        self.pause = True
        pygame.display.flip()  # refresh display
        self.reset()

    def display(self):
        font0 = pygame.font.SysFont(f"{font}", 30)
        score = font0.render(f"Score: {self.snake.length - 2}", True, (225, 225, 225))
        info = font0.render(f"Press ESC to quit the game...", True, (225, 225, 225))
        self.surface.blit(score, (900, 10))
        self.surface.blit(info, (10, 550))
        if self.collision():
            self.game_over()

    def intro(self):
        self.render_background()
        font1 = pygame.font.SysFont(f"{font}", 100)
        font2 = pygame.font.SysFont(f"{font}", 40)
        message = font1.render(f"Snake Game!", True, (225, 225, 225))
        message1 = font2.render(f"Loading...", True, (225, 225, 225))
        self.surface.blit(message, (365, 200))
        self.surface.blit(message1, (550, 315))
        pygame.display.flip()  # refresh display
        time.sleep(3)

    def reset(self):
        self.snake = Snake(self.surface, 2)
        self.apple = Apple(self.surface)

    def sound(self, sound):
        sound = pygame.mixer.Sound(f"resources/{sound}.mp3")  #
        pygame.mixer.Sound.play(sound)

    def render_background(self):
        self.surface.blit(bg, (0, 0))


class Apple:
    def __init__(self, parent_surface):
        self.surface = parent_surface
        self.apple = pygame.image.load("resources/apple.jpg").convert()
        self.x = size * 3
        self.y = size * 3

    def draw(self):
        self.surface.blit(self.apple, (self.x, self.y))
        pygame.display.flip()  # refresh display

    def move(self):  # ensures alignment of apple and snake
        self.x = random.randint(0, 29) * size
        self.y = random.randint(0, 14) * size


class Snake:
    def __init__(self, parent_surface, length):
        self.surface = parent_surface
        self.length = length
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.x = [size] * length
        self.y = [size] * length
        self.direction = "right"

    def draw(self):
        for i in range(self.length):
            self.surface.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()  # refresh display

    def move_up(self):
        self.direction = "up"

    def move_down(self):
        self.direction = "down"

    def move_left(self):
        self.direction = "left"

    def move_right(self):
        self.direction = "right"

    def walk(self):

        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == "up":
            self.y[0] -= size

        if self.direction == "down":
            self.y[0] += size

        if self.direction == "left":
            self.x[0] -= size

        if self.direction == "right":
            self.x[0] += size

        self.draw()

    def grow(self):  # dynamically increasing the size of the array
        self.length += 1
        self.x.append(1)
        self.y.append(1)


if __name__ == "__main__":
    game = Game()
    game.intro()
    game.run()