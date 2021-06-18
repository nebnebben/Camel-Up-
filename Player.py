
class Player:
    total_winner_bids = []
    total_loser_bids = []
    # Of the form camel: amount
    cur_round_bids = {}
    used_tile = False
    tile_location = None

    def __init__(self, money, bot):
        self.money = money
        # initialise bot
        self.ai = bot()

    # make bid for current round
    def make_round_bid(self, amount, camel):
        # Check whether camel has already bid on and act accordingly
        if camel in self.cur_round_bids:
            self.cur_round_bids[camel] += amount
        else:
            self.cur_round_bids[camel] = amount

    def make_game_bid(self, camel, win):
        # If camel already bid on, raise error
        if camel in self.total_winner_bids or camel in self.total_loser_bids:
            print('Already bid on')
            raise

        # Check whether bid to lose or win
        if win:
            self.total_winner_bids.append(camel)
        else:
            self.total_loser_bids.append(camel)


    # get general info about player
    def get_info(self):
        return {
            'money': self.money,
            'tile': self.tile_location,
            'bids': self.cur_round_bids
        }

    # get private info about player
    def get_private_info(self):
        return {
            'money': self.money,
            'tile': self.tile_location,
            'bids': self.cur_round_bids,
            'winner_bids':self.total_winner_bids,
            'loser_bids':self.total_loser_bids
        }
