
class Player:
    total_winner_bids = []
    total_loser_bids = []
    # Of the form camel: amount
    cur_round_bids = {}
    used_tile = False
    tile_location = None

    def __init__(self, money, bot):
        self.money = money
        self.ai = bot

    def get_info(self):
        return {
            'money': self.money,
            'tile': self.tile_location,
            'bids': self.cur_round_bids
        }

    def get_private_info(self):
        return {
            'money': self.money,
            'tile': self.tile_location,
            'bids': self.cur_round_bids,
            'winner_bids':self.total_winner_bids,
            'loser_bids':self.total_loser_bids
        }

