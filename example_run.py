from test_bot1 import test_bot
from human_player import human_player_actual
from Main import Game
# g = Game([human_player_actual, test_bot])
# g = Game([test_bot, test_bot])
g = Game([human_player_actual, human_player_actual])

g.start_game()