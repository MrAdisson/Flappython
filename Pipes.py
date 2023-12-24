import pygame 
import constants
import random
from Bird import Bird


class Pipe:
    def __init__(self, screen_width, screen_height, height= 0 ):
        if height == 0:
            height = random.randint(100, screen_height - constants.PIPE_GAP - 100)
        self.x = screen_width + constants.PIPE_WIDTH
        self.y = 0
        self.height = height
        self.speed = constants.PIPE_SPEED
        self.width = constants.PIPE_WIDTH
        self.hasGeneratedNextPipe = False
        self.isPassed = False
        Pipes.append(self)

    def move(self, dt):
        self.x -= self.speed

    def update(self, game: pygame.Surface, dt):
        self.move(dt)
        if self.x < game.screen.get_width() - constants.SPACE_BETWEEN_PIPES:
            if not self.hasGeneratedNextPipe:
                Pipe(game.screen.get_width(), game.screen.get_height())
                self.hasGeneratedNextPipe = True
        if self.x < -self.width:
            Pipes.remove(self)

        # UPDATE SCORE:
        if self.x + self.width < game.screen.get_width() // 2 and not self.isPassed:
            self.isPassed = True
            for x, bird in enumerate(game.birds):
                if not bird.isDead:
                    bird.score += 1
                    if game.ai_mode:
                        game.ge[x].fitness += 10
        
    def draw(self, screen):
        pygame.draw.rect(screen, constants.GREEN, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, constants.GREEN, (self.x, self.height + constants.PIPE_GAP, self.width, screen.get_height() - self.height - constants.PIPE_GAP))

    def check_collision(self, bird: Bird):
        if bird.x + bird.radius > self.x and bird.x - bird.radius < self.x + self.width:
            if bird.y - bird.radius < self.height or bird.y + bird.radius > self.height + constants.PIPE_GAP:
                bird.isDead = True
    

Pipes: list[Pipe] = []
