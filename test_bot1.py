
class test_bot:


    def __init__(self):
        id = 'test1'

    # Takes in information about the game state and returns a move
    def move(self, cur_player_info, other_player_info, board, unmoved_camels, tiles_left):
        """
        This is the function to make a move
        :param cur_player_info: Dict
        'money': amount of money
        'tile': location of tile if placed, None otherwise
        'bids': dict of bids made, camel: amount
        'winner_bids':self.total_winner_bids,
        'loser_bids':self.total_loser_bids

        :param other_player_info: List, each player is an element and a dict
        of the form {money:their money, tile:tile location if placed, bids: dict}
        :param board: list with board info on, letters are camels, < and > are tiles
        last space acts as finish line
        :param unmoved_camels: list with camels that haven't been moved
        :param tiles_left: Dict, camel: list of betting tiles avaliable
        e.g. 'A': [2,3] if 5 was already taken
        :return:
        """

        """
        Possible moves:
        - Return list of form [x, y] where x is the move and y is more info
        [0,0] - Pyramid tile
        [1, x] - Desert tile, x is the location on the board, starting from 0
        [2, x] - Round betting tile, x is the camel to bet on, e.g. 'A'
        [3, x] - Bet on overall winner, x is the camel to bet on
        [4, x] - Bet on overall loser, x is the camel to bet on
        """