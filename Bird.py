import pygame
import constants

class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.acceleration = 0
        self.speed = 0
        self.jump_speed = constants.JUMP_SPEED
        self.radius = constants.BIRD_RADIUS
        self.isDead = False
        self.score = 0
        self.distanceTravelled = 0

    def move(self, dt):
        self.acceleration += constants.GRAVITY
        self.speed += self.acceleration
        self.y += self.speed 
        self.distanceTravelled += constants.PIPE_SPEED
        
    def update(self, dt, screen: pygame.Surface):
        self.move(dt)
        # IF BIRD HITS THE GROUND OR THE SKY:
        if self.y + self.radius > screen.get_height() or self.y - self.radius < 0:
            self.isDead = True
            return self.isDead
        return False

    def jump(self, dt):
        self.speed = -self.jump_speed
        self.acceleration = 0

    def draw(self, screen):
        pygame.draw.rect(screen, constants.WHITE, (self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2))

