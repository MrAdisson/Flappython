### FLAPPYTHON
## Une implémentation de NEAT sur un jeu de Flappy Bird

En bas du fichier main.py, vous pouvez retrouver ce code : 

`# IA TRAINING`
`run(config_path) # Uncomment this line to run an AI training session (unless game.isLoaded is True)`

`# IA LOAD & PLAY MODEL:`
`# game.isLoaded = True # Uncomment this line to load the winner.pkl file and run the game`
`# run(config_path) # Uncomment this line to run an AI training session (unless game.isLoaded is True)`

`# # HUMAN :`
`# game.run() # Uncomment this to play human game`

## IA TRAINING
La partie IA TRAINING va générer un réseau de neurone aléatoire de population X (à configurer dans le fichier de configuration de NEAT config-feedforward.txt)
## IA LOAD & PLAY MODEL
La partie IA LOAD & PLAY MODEL va chercher un fichier `winner.pkl` à la racine du projet et lancer une partie avec ce réseau de neuronnes. 
## HUMAN :
Pour jouer soi même !

### CONFIGURATION :

Des paramètres sont modifiables afin de modifier le cours des parties et de l'entrainement. 

Dans le fichier main.py, vous pouvez retrouver le bloc suivant : 

`#AI CONFIG
SHOW_TRAINING = False
MAX_GENERATION = 100
TRAINING_FPS = 120
TARGET_SCORE = 500
PLAYING_FPS = 60
`
SHOW_TRAINING : vous permet de visualiser ou non l'entrainement
TRAINING_FPS : Le framerate pendant l'entrainement
PLAYING_FPS : Le framerate en winner game (partie lancée à la fin de l'entrainement avec le réseau gagnant)
MAX_GENERATION : le nombre maximum de générations 
TARGET_SCORE : le score au dela duquel, si il est atteint, la partie actuelle s'arrête et on relance une partie d'entrainement (sauf si le fitness_threshold défini dans le config-feedforward.txt a été atteint)
