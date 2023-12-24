import pygame
from Pipes import Pipe, Pipes
from Bird import Bird
from Game import Game

def handle_events(game: Game, dt: float ):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.running = False
        elif (event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN) and not game.ai_mode:
            if not game.started:
                game.started = True
                return
            if game.ended:
                reset_game(game)
                return
            for bird in game.birds:
                bird.jump(dt)

def reset_game(game: Game): 
    # RESET GAME:
    game.ended = False
    game.started = False
    game.birds.clear()
    game.birds.append(Bird(game.screen.get_width() // 2, game.screen.get_height() // 2))
    Pipes.clear()
    Pipe(game.screen.get_width(), game.screen.get_height())
