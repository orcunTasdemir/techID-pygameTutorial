import pygame
import sys
import random

# Draw the Snake on the Screen!

# Our global parameters for the screen size and what the directions mean to us in terms of the coordinate values - we need to subtract or add to - to make the movement happen.
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 480

GRID_SIZE = 20
GRID_WIDTH = SCREEN_HEIGHT / GRID_SIZE
GRID_HEIGHT = SCREEN_WIDTH / GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


def drawGrid(surface):
    for y in range(0, int(GRID_HEIGHT)):
        for x in range(0, int(GRID_WIDTH)):
            if (x+y) % 2 == 0:
                r_light = pygame.Rect((x*GRID_SIZE, y*GRID_SIZE),
                                      (GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(surface, (93, 216, 228), r_light)
            else:
                r_dark = pygame.Rect((x*GRID_SIZE, y*GRID_SIZE),
                                     (GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(surface, (84, 194, 205), r_dark)

# All classes inherit from the class object but it is not required
# for us to use it here we could have simply said:
# class Snake:


class Snake(object):

    def __init__(self):
        self.positions = [((SCREEN_WIDTH/2), (SCREEN_HEIGHT/2))]
        self.color = (17, 24, 47)
        self.length = 1
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + (x*GRID_SIZE)) %
               SCREEN_WIDTH), (cur[1] + (y*GRID_SIZE)) % SCREEN_HEIGHT)
        if len(self.positions) > 2 and new in self.positions[2:]:
            # snake ate itself
            self.reset()
        else:
            # insert as the new head of the snake
            self.positions.insert(0, new)
            # the reason we use an if here is the possibility that the snake ate something as they moved
            if len(self.positions) > self.length:
                self.positions.pop()

    def draw(self, surface):
        for p in self.positions:
            snake_body_r = pygame.Rect((p[0], p[1]), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.color, snake_body_r)
            #pygame.draw.rect(surface, (93, 216, 228), snake_body_r, 1)

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(UP)
                elif event.key == pygame.K_DOWN:
                    self.turn(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.turn(RIGHT)


class Food(object):

    def __init__(self):
        pass


def main():
    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((480, 480), 0, 32)
    surface = pygame.Surface(screen.get_size())

    snake = Snake()
    food = Food()

    while(True):
        clock.tick(10)
        snake.handle_keys()
        drawGrid(surface)
        snake.move()
        snake.draw(surface)
        screen.blit(surface, (0, 0))
        pygame.display.update()


main()
