import random
from Player import Player
from Round import Round
from copy import deepcopy

class Game:
    # General information about all the game in general
    camels = ['A', 'B', 'C', 'D', 'E']
    no_camels = len(camels)
    # Betting tiles for a round
    round_tiles = [2, 3, 5]
    # Betting tiles for the entire game
    final_tiles = [1, 2, 3, 5, 8]
    starting_money = 3
    players = []

    # Takes in players and initialises game
    def __init__(self, bots):
        # Initialise all bots as Player classes
        self.players = [Player(3, bot) for bot in bots]
        self.starting_player = random.randrange(len(bots))
        self.board = []
        # positions of the camels
        self.positions = {}

        # Board is length 16 + 1 square for terminal position
        for i in range(17):
            self.board.append([])

        # Get camel starting positions
        # Get order and position of camels first
        order = random.sample(self.camels, len(self.camels))
        dice = [random.randrange(1, 4) for i in range(len(self.camels))]
        for i in range(len(order)):
            self.board[dice[i]] += order[i]
            self.positions[order[i]] = dice[i]

    # Gets all the relevant info from players and sends to a bot
    def get_relevant_info(self, current_player):
        # Get info on all the other players
        other_player_info = []
        for i in range(len(self.players)):
            if i != current_player:
                p = self.players[i].get_info()
                other_player_info.append(p)

        # Get private info on current player
        current_player_info = self.players[current_player].get_private_info()

        return current_player_info, other_player_info


    def make_move(self, move, cur_round, current_player):
        # If pyramid tile
        if move[0] == 0:
            # increment players money
            self.players[current_player].money += 1
            self.board = cur_round.advance_game(self.board)

        # Desert tile
        # elif move[0] == 1:
        # # Round betting tle
        # elif move[0] == 2:
        # # Overall winner
        # elif move[0] == 3:
        # # Overall loser
        # elif move[0] == 4:

        return cur_round


    def game_round(self):
        current_player = self.starting_player
        fin_round = False
        cur_round = Round(self.camels, self.round_tiles)

        while(not fin_round):
            # Get the current move
            # Feed in all info about player + board state
            current_player_info, other_player_info = self.get_relevant_info(current_player)
            # Get the result of the move
            move = self.players[current_player].ai.move(
                current_player_info,
                other_player_info,
                deepcopy(self.board),
                deepcopy(cur_round.unmoved_camels),
                deepcopy(cur_round.tiles)
            )

            # Make the move
            cur_round = self.make_move(move, cur_round, current_player)

            # check finish line for game end
            if self.board[-1]:
                fin_round = False

            # Make the next player the current player
            current_player = (current_player+ 1) % len(self.players)

        # Make starting player current player
        # Player after the one that got pyramid tile
        self.starting_player = current_player

        # end round
        return


    def start_game(self):
        if not self.players:
            print('You need to initialise the game first!')
            return

        game_finished = False
        self.final_tiles_bids = []

        while(not game_finished):
            res = self.game_round()

