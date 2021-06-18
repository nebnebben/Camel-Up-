import random
class Round:

    def __init__(self, camels, round_tiles):
        # Record betting tiles for current round
        self.tiles = {}
        for camel in camels:
            self.tiles[camel] = round_tiles

        # Initial camels
        self.initial_camels = camels

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
        for i, square in enumerate(board):
            if camel in square:
                position = i

        # Change board
        board, _ = self.calculate(board, position, camel, dice)

        return board

    # Place a tile down
    def place_tile(self, board, location, direction):
        # Check that the location selected is valid
        if location < 0 or location > 15:
            print('Out of range')
            raise
        if board[location] != '':
            print('Non empty square')
            raise
        if location > 0 and board[location-1] == '>' or board[location-1] == '<':
            print('Adjacent square with tile')
            raise
        if location < 15 and board[location+1] == '>' or board[location+1] == '<':
            print('Adjacent square with tile')
            raise

        # Amend board
        board[location] = direction

        return board

    # Clean board of desert tiles
    def remove_tiles(self, board):
        for i in range(len(board)):
            if board[i] == '>' or board[i] == '<':
                board[i] = ['']
        return board

    def get_winners(self, board):
        # Find camel positions
        positions = {}
        for camel in self.initial_camels:
            for i, square in enumerate(board):
                # List camel position
                if camel in square:
                    positions[camel] = i

        # Gets positions of camels in board, descending
        pos = sorted(list(set(positions.values())), reverse=True)
        outcome = []
        for position in pos:
            # from top of camel stack down
            for camel in board[position][::-1]:
                outcome += [camel]

        return outcome