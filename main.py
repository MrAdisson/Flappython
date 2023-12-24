import pygame
from Game import Game
import os
import neat
from Bird import Bird
from Pipes import Pipes, Pipe
import events
import constants
import pickle

# Set up the Pygame window
pygame.init()
screen = pygame.display.set_mode((400, 700))
pygame.display.set_caption("Flappy Bird")
game = Game(screen)
clock = pygame.time.Clock()
# RUN 

#AI CONFIG
SHOW_TRAINING = False
MAX_GENERATION = 1000
TRAINING_FPS = 120
TARGET_SCORE = 500
PLAYING_FPS = 120

def initGame():
    game.birds.clear()
    Pipes.clear()
    game.nets.clear()
    game.ge.clear()   
    Pipe(game.screen.get_width(), game.screen.get_height(), 100)

def runWinnerGame(winner, config):
    print("RUN WINNER GAME")
    net = neat.nn.FeedForwardNetwork.create(winner, config)
    initGame()
    game.birds.append(Bird(game.screen.get_width() // 2, game.screen.get_height() // 2))
    game.nets.append(net)
    game.ge.append(winner)
    game.isWinner = True
    runGame(None, config)

def runGame(genomes, config):
    game.ai_mode = True

    if genomes is not None:
        initGame()
        game.gen += 1
        for _, g in genomes:
            net = neat.nn.FeedForwardNetwork.create(g, config)
            game.nets.append(net)
            g.fitness = 0
            game.ge.append(g)
            game.birds.append(Bird(game.screen.get_width() // 2, game.screen.get_height() // 2))

    game.running = True
    game.ended = False
    game.started = True

    # AI GAME LOOP
    while game.running:
    
        if not len(game.birds):
            game.ended = True
            game.running = False
            break

        elif (game.birds[0].score > TARGET_SCORE and not game.isWinner):
            for x, bird in enumerate(game.birds):
                game.ge[x].fitness += 100
                game.ended = True
                game.running = False
                break

        #TICKING
        dt = 1
        if game.isWinner or SHOW_TRAINING:
            if SHOW_TRAINING: 
                dt = clock.tick(TRAINING_FPS) / 1000
            else: 
                dt = clock.tick(PLAYING_FPS) / 1000

        # if game.started and not game.ended:
        for x, bird in enumerate(game.birds):
            # INCREMENT BIRD FITNESS FOR BEING ALIVE
            game.ge[x].fitness += .2
            nextPipe = None
            Pipes.sort(key=lambda pipe: pipe.x)
            for pipe in Pipes:
                if pipe.x > game.birds[0].x:
                    nextPipe = pipe
                    break
            if nextPipe is None:
                nextPipe = Pipes[0]

            #PYTHAGORE DISTANCE
            distanceToTopOfPipe = ((bird.y - nextPipe.height) ** 2 + (nextPipe.x - bird.x) ** 2) ** 0.5
            distanceToBottomOfPipe = ((bird.y - nextPipe.height - constants.PIPE_GAP) ** 2 + (nextPipe.x - bird.x) ** 2) ** 0.5

            output = game.nets[x].activate((bird.y, distanceToTopOfPipe, distanceToBottomOfPipe))
            if output[0] > 0.5:
                game.ge[x].fitness -= .5
                bird.jump(dt)
        game.update(dt)

        if (game.isWinner or SHOW_TRAINING) and not game.ended and game.started:
            game.draw(screen)
            pygame.display.flip()
        events.handle_events(game, dt)
                    
def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                            neat.DefaultSpeciesSet, neat.DefaultStagnation,
                            config_path)
    p = neat.Population(config)
    print(p)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    if not game.isLoaded:
        winner = p.run(runGame, MAX_GENERATION)
        print('\nBest genome:\n{!s}'.format(winner))
        # save winner
        with open('winner.pkl', 'wb') as output:
            pickle.dump(winner, output, 1)
        # run a game with winner
        runWinnerGame(winner, config)

    else:
        # OPEN WINNER FILE AND RUN WINNER GAME
        with open('winner.pkl', 'rb') as input_file:
            winner = pickle.load(input_file)
            runWinnerGame(winner, config)


# PATH FOR CONFIG FILE
if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    

# IA :
game.isLoaded = True # Uncomment this line to load the winner.pkl file and run the game
run(config_path) # Uncomment this line to run an AI training session (unless game.isLoaded is True)

# # HUMAN :
# game.run() # Uncomment this to play human game


