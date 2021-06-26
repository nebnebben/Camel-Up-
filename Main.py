import random
from Player import Player
from Round import Round
from copy import deepcopy

class Game:

    # Takes in players and initialises game
    def __init__(self, bots):
        # General information about all the game in general
        self.camels = ['A', 'B', 'C', 'D', 'E']
        self.no_camels = len(self.camels)
        # Betting tiles for a round
        self.round_tiles = [2, 3, 5]
        # Betting tiles for the entire game
        self.final_tiles = [1, 2, 3, 5, 8]
        self.starting_money = 3

        # Initialise all bots as Player classes
        self.players = [Player(self.starting_money, bot) for bot in bots]
        self.starting_player = random.randrange(len(bots))
        self.board = []
        # location of desert tiles, location:player_index
        self.desert_tiles = {}
        # Final tiles bids, list of [player_index, camel]
        self.final_bids_winners = []
        self.final_bids_losers = []

        # Board is length 16 + 1 square for terminal position
        for i in range(17):
            self.board.append([])

        # Get camel starting positions
        # Get order and position of camels first
        order = random.sample(self.camels, len(self.camels))
        dice = [random.randrange(1, 4) for i in range(len(self.camels))]
        for i in range(len(order)):
            self.board[dice[i]] += order[i]
            # self.positions[order[i]] = dice[i] - does nothing

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
            self.board, tile_money = cur_round.advance_game(self.board, self.desert_tiles)

            # Account for tiles stepped on
            # tile_money - list of players with tiles stepped on
            for player in tile_money:
                self.players[player].money += 1
                print(f'Player {player} gets a point from the tile')

        # Desert tile
        elif move[0] == 1:
            # if tile already placed
            if self.players[current_player].used_tile:
                print('Already place tile for the round')
                raise

            location = move[1][0]
            direction = move[1][1]

            # Get updated board
            self.board = cur_round.place_tile(deepcopy(self.board), location, direction)
            # Add desert tile
            self.desert_tiles[location] = current_player
            self.players[current_player].used_tile = True

        # Round betting tile
        elif move[0] == 2:
            # get camel
            camel = move[1]
            # Get value of current tile
            value = cur_round.tiles[camel].pop()
            # if no tiles
            if not value:
                print('No more tiles')
                raise
            # Record bid for player
            print(f'Bid {value} on {camel}')
            self.players[current_player].make_round_bid(value, camel)

        # Overall winner
        elif move[0] == 3:
            camel = move[1]
            if camel in self.players[current_player].total_winner_bids:
                print('Already bid on to win')
                raise
            if camel in self.players[current_player].total_loser_bids:
                print('Already bid on to lose')
                raise

            # Record bid made
            self.final_bids_winners.append([current_player, camel])
            self.players[current_player].total_winner_bids.append(camel)

        # Overall loser
        elif move[0] == 4:
            camel = move[1]
            if camel in self.players[current_player].total_winner_bids:
                print('Already bid on to win')
                raise
            if camel in self.players[current_player].total_loser_bids:
                print('Already bid on to lose')
                raise

            # Record bid made
            self.final_bids_losers.append([current_player, camel])
            self.players[current_player].total_loser_bids.append(camel)

        return cur_round

    def game_round(self):
        current_player = self.starting_player
        fin_round = False
        cur_round = Round(deepcopy(self.camels), deepcopy(self.round_tiles))

        while(not fin_round):
            print(self.board)
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

            # check finish line for game end or all camels moved
            if self.board[-1] or not cur_round.unmoved_camels:
                fin_round = True

            # Make the next player the current player
            current_player = (current_player + 1) % len(self.players)

        # Make starting player current player
        # Player after the one that got pyramid tile
        self.starting_player = current_player

        # Get round winners
        winners = cur_round.get_winners(self.board)

        # Remove desert tiles
        self.board = cur_round.remove_tiles(deepcopy(self.board))
        self.desert_tiles = {}
        for player in self.players:
            player.used_tile = False

        print('Round end')
        print('')
        # end round
        return winners

    def round_end_scoring(self, winners):
        for i, player in enumerate(self.players):
            for bid in player.cur_round_bids:
                # If won then gain money equal to tile
                if bid == winners[0]:
                    winnings = player.cur_round_bids[bid]
                # If came second then gain 1
                elif bid == winners[1]:
                    winnings = 1
                # else lose 1
                else:
                    winnings = -1

                player.money += winnings
                print(f'Player {i} bet on {bid} wins {winnings}')

            player.cur_round_bids = {}

    def game_end_bets(self, winners):
        # Resolve scoring for bidding on the losers
        rewards = self.final_tiles[:]
        for bid in self.final_bids_losers:
            cur_player = bid[0]
            camel = bid[1]
            # If bid was on losing camel
            if camel == winners[-1]:
                winnings = rewards.pop()
            else:
                winnings = -1

            print(f'Player {cur_player} bet on {camel} to lose and won {winnings}')
            self.players[cur_player].money += winnings

        # bidding on the winners
        rewards = self.final_tiles[:]
        for bid in self.final_bids_winners:
            cur_player = bid[0]
            camel = bid[1]
            # If bid was on winning camel
            if camel == winners[0]:
                winnings = rewards.pop()
            else:
                winnings = -1

            print(f'Player {cur_player} bet on {camel} to win and won {winnings}')
            self.players[cur_player].money += winnings

    def game_end_scoring(self, winners):
        # Add in final round bidding
        self.game_end_bets(winners)

        max_score = float('-inf')
        player_winner = - 1
        scores = []
        for i in range(len(self.players)):
            if self.players[i].money > max_score:
                max_score = self.players[i].money
                player_winner = i
            scores.append([i, self.players[i].money])

        return player_winner, scores

    def start_game(self):
        if not self.players:
            print('You need to initialise the game first!')
            return

        game_finished = False
        while(not game_finished):
            # Run round
            winners = self.game_round()
            # Update money for round end
            self.round_end_scoring(winners)
            # Check for end of game
            if self.board[-1]:
                game_finished = True

        # Final results
        overall_winner, results = self.game_end_scoring(winners)
        print(self.board)
        print(f'overall winner was {overall_winner} and results were {results}')






