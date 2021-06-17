import random
class Round:

    def __init__(self, camels, round_tiles):
        # Record betting tiles for current round
        self.tiles = {}
        for camel in camels:
            self.tiles[camel] = round_tiles

        # camels that haven't yet moved
        self.unmoved_camels = camels

    # board: full board state
    # positions of the camels: dict, Letter: board pos
    def calculate(self, board, pos, cur_camel, cur_roll):
        money = 0
        # Get camel position in camel stack
        ind = board[pos].index(cur_camel)
        # Camel stack is that camel and everything after
        stack = board[pos][ind:]
        # delete that part of the board
        del board[pos][ind:]
        # Update current position
        pos += cur_roll
        # if winning roll
        if pos > 15:
            pos = 16

        # Check for traps and update final board positions
        if board[pos] == '>':
            money += 1
            pos += 1
            board[pos] += stack
        elif board[pos] == '<':
            money += 1
            pos -= 1
            board[pos] = stack + board[pos]
        else:
            board[pos] += stack

        return board, money

    def advance_game(self, board):
        # picks a random unmoved camel
        camel = random.choice(self.unmoved_camels)
        self.unmoved_camels.remove(camel)
        # pick a random number
        dice = random.randrange(1, 4)
        # Find camel position
        for i,square in enumerate(board):
            if camel in square:
                position = i

        # Change board
        board, _ = self.calculate(board, position, camel, dice)

        return board

