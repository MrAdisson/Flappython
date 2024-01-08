# BIRD CLASS:
from Pipes import Pipe, Pipes
from Bird import Bird
import pygame
import constants

class Game: 
    def __init__(self, screen: pygame.Surface, ai_mode = False):
        self.gen = 0
        self.running = True
        self.screen = screen
        self.started = True
        self.ended = False
        self.birds: list[Bird] = []
        self.clock = pygame.time.Clock()
        self.nets = []
        self.ge = []
        self.ai_mode = ai_mode
        self.isWinner = False
        self.isLoaded = False
        Pipe(screen.get_width(), screen.get_height(), 100)


    def update(self, dt):

        for x, bird in enumerate(self.birds):
            bird.update(dt, self.screen)
            if bird.isDead:
                self.birds.pop(x)
                if self.ai_mode:
                    self.ge.pop(x)
                    self.nets.pop(x)
                if len(self.birds) == 0:
                    print('All birds are dead')
                    self.ended = True
                    self.started = False
                    self.running = False
                    return True
                continue
        
        for pipe in Pipes:
            pipe.update(self, dt)
            for bird in self.birds:
                pipe.check_collision(bird)

    def draw(self, screen: pygame.Surface):
        screen.fill(constants.BLACK)
        if not self.started:
            font = pygame.font.Font(None, 50)
            text = font.render("Press any key to start", True, constants.WHITE)
            text_rect = text.get_rect()
            text_rect.center = (screen.get_width() // 2, screen.get_height() // 2)
            screen.blit(text, text_rect)
            return
        
        for bird in self.birds:
            bird.draw(screen)
        for pipe in Pipes:
            pipe.draw(screen)
        font = pygame.font.Font(None, 50)


        text = font.render('Alive : ' + str(len(self.birds)), True, constants.WHITE)
        text_rect = text.get_rect()
        screen.blit(text, text_rect)
        text = font.render('Gen : ' + str(self.gen), True, constants.WHITE)
        text_rect = text.get_rect()
        text_rect.topleft= (0, 50)
        screen.blit(text, text_rect)

        text = font.render("Score : " + str(self.birds[0].score), True, constants.WHITE)
        text_rect = text.get_rect()
        # text_rect.center = (screen.get_width() // 2, 50)
        text_rect.topleft = (0, 100)
        screen.blit(text, text_rect)

    def run(self):
        self.started = False
        self.ended = False
        self.running = True
        self.birds.append(Bird(self.screen.get_width() // 2, self.screen.get_height() // 2))
        from events import handle_events
        while self.running:
            dt = self.clock.tick(60) / 1000
            if self.started and not self.ended:
                self.update(dt)
            self.draw(self.screen)
            pygame.display.flip()
            handle_events(self, dt)

   
