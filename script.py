import pygame
import sys
import random

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


class Snake(object):
    """snake is the class implementation from which we create/instantiate our snake objects for the game

    Args:
        object (_type_): _description_
    """

    def __init__(self):
        self.length = 1
        self.score = 0
        # start from the center pointing to a random position
        self.positions = [((SCREEN_WIDTH/2), (SCREEN_HEIGHT/2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = (17, 24, 47)

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

    def reset(self):
        self.length = 1
        self.score = 0
        self.positions = [((SCREEN_WIDTH/2), (SCREEN_HEIGHT/2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

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
        self.position = (0, 0)
        self.color = (223, 163, 49)
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH-1) *
                         GRID_SIZE, random.randint(0, GRID_HEIGHT-1) * GRID_SIZE)

    def draw(self, surface):

        food_r = pygame.Rect(
            (self.position[0], self.position[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.color, food_r)
        #pygame.draw.rect(surface, (93, 216, 228), food_r, 1)


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


def main():
    pygame.init()

    clock = pygame.time.Clock()
    # The flags argument is a collection of additional options. The depth argument represents the number of bits to use for color.
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

    surface = pygame.Surface(screen.get_size())
    # we lose the alpha values here when we convert the surface, which we do not need
    # it will be optimized for fast alpha blitting to the destination
    surface = surface.convert()

    snake = Snake()
    food = Food()

    while True:
        clock.tick(10)
        snake.handle_keys()
        drawGrid(surface)
        snake.move()
        if snake.get_head_position() == food.position:
            snake.length += 1
            snake.score += 1
            food.randomize_position()

        snake.draw(surface)
        food.draw(surface)
        # handle the events here
        screen.blit(surface, (0, 0))
        font = pygame.font.SysFont("Arial", 15, True, False)
        text = font.render("Score {0}".format(snake.score), 1, (0, 0, 0))
        screen.blit(text, (5, 10))
        pygame.display.update()


main()
