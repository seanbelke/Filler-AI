from gamesearch import *
from enum import Enum
from copy import deepcopy


class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3
    BLACK = 4
    YELLOW = 5
    PURPLE = 6

    def __repr__(self):
        if self is self.RED:
            return 'RED'
        elif self is self.GREEN:
            return 'GRE'
        elif self is self.BLUE:
            return 'BLU'
        elif self is self.BLACK:
            return 'BLA'
        elif self is self.YELLOW:
            return 'YEL'
        elif self is self.PURPLE:
            return 'PUR'


class FillerBoard():
    def __init__(self, colors, player='A'):
        self.board = colors
        self.width = len(colors)  # not canonical indexing
        self.height = len(colors[0])
        self.player = player

    def __repr__(self):
        return '\n'.join([x.__repr__() for x in unrotate_grid(self.board)])

    def get_player_a_color(self):
        return self.board[0][0]

    def get_player_b_color(self):
        return self.board[self.width - 1][self.height - 1]

    def get_player_region(self, player):
        if player == 'A':
            color = self.board[0][0]
            region = [(0, 0)]
        if player == 'B':
            color = self.board[self.width - 1][self.height - 1]
            region = [(self.width - 1, self.height - 1)]
        frontier = region.copy()
        while len(frontier) > 0:
            (x, y) = frontier.pop()
            if self.location_is_color((x + 1, y), color) and (x + 1, y) not in region:
                frontier.append((x + 1, y))
                region.append((x + 1, y))
            if self.location_is_color((x, y + 1), color) and (x, y + 1) not in region:
                frontier.append((x, y + 1))
                region.append((x, y + 1))
            if self.location_is_color((x - 1, y), color) and (x - 1, y) not in region:
                frontier.append((x - 1, y))
                region.append((x - 1, y))
            if self.location_is_color((x, y - 1), color) and (x, y - 1) not in region:
                frontier.append((x, y - 1))
                region.append((x, y - 1))
        return region

    def location_is_color(self, loc, color):
        (x, y) = loc
        if x not in range(self.width) or y not in range(self.height):
            return False
        return self.board[x][y] == color


class Filler(Game):
    def __init__(self, initial, max_search_depth=4):
        super().__init__(initial, ['A', 'B'])
        self.search_depth = max_search_depth

    def to_move(self, s):
        return s.player

    def actions(self, s):
        actions = set([Color.RED, Color.GREEN, Color.BLUE, Color.BLACK, Color.YELLOW, Color.PURPLE])
        actions.discard(s.get_player_a_color())
        actions.discard(s.get_player_b_color())
        # new_actions = set([])
        # for a in actions:
        #     if any([a in row for row in s.board]):
        #         new_actions.add(a)
        return actions # was return new_actions

    def result(self, s, a):
        new_board = [[col for col in row] for row in s.board]
        region = s.get_player_region(s.player)
        for (x, y) in region:
            new_board[x][y] = a
        new_player = 'A'
        if s.player == 'A':
            new_player = 'B'
        return FillerBoard(new_board, new_player)

    def is_terminal(self, s):
        player_a_score = len(s.get_player_region('A'))
        if player_a_score > (s.width * s.height) // 2:
            return True
        player_b_score = len(s.get_player_region('B'))
        if player_b_score > (s.width * s.height) // 2:
            return True
        elif (player_a_score + player_b_score) == (s.width * s.height):
            return True

        return False

    def is_cutoff(self, s, depth):
        return depth >= self.search_depth or self.is_terminal(s)

    def utility(self, s, p):
        if p == 'A':
            notp = 'B'
        else:
            notp = 'A'
        return len(s.get_player_region(p)) - len(s.get_player_region(notp))


def unrotate_grid(grid):
    rows = len(grid)
    cols = len(grid[0])
    return [[grid[r][c] for r in range(rows)] for c in range(cols - 1, -1, -1)]

def rotate_grid(grid):
    rows = len(grid)
    cols = len(grid[0])
    newgrid = [[grid[r][c] for r in range(rows)] for c in range(cols)]
    return [[newgrid[r][c] for c in range(rows - 1, -1, -1)] for r in range(cols)]


def play_game(game, initial=None):
    s = initial or game.initial
    while not game.is_terminal(s):
        a_score = len(s.get_player_region('A'))
        b_score = len(s.get_player_region('B'))
        print('A Score: ' + str(a_score))
        print('B Score: ' + str(b_score))
        print(s)
        print('To Move: ' + s.player)
        print('Actions: ' + str(game.actions(s)))
        print()
        if game.to_move(s) == 'A':
            move = alpha_beta_minimax(game, s) # AI plays for player A
        else:
            move = Color(int(input("move: "))) # Player B must input a move
        s = game.result(s, move)
    a_score = len(s.get_player_region('A'))
    b_score = len(s.get_player_region('B'))
    print('A Score: ' + str(a_score))
    print('B Score: ' + str(b_score))
    print(s)
    print()

    if a_score > b_score:
        winner = 'A'
    elif b_score > a_score:
        winner = 'B'
    else:
        winner = 'Tie'
    print("winner: " + winner)


RD = Color.RED
YL = Color.YELLOW
BK = Color.BLACK
BU = Color.BLUE
GR = Color.GREEN
PU = Color.PURPLE

initial_grid = [
    [RD, YL, BK, GR],
    [YL, RD, YL, PU],
    [RD, BK, BU, GR]
]

initial_grid = [
    [PU, BK, GR, BU, GR, RD, YL, GR],
    [BU, GR, PU, BK, PU, YL, PU, BU],
    [YL, RD, GR, RD, YL, GR, RD, PU],
    [BU, GR, BK, YL, BK, PU, GR, BU],
    [GR, RD, BU, RD, PU, BK, PU, RD],
    [YL, PU, GR, BU, RD, GR, YL, BK],
    [BK, BU, PU, GR, BU, PU, BK, BU]
]

initial_board = FillerBoard(rotate_grid(initial_grid), 'A')

game = Filler(initial_board)
play_game(Filler(initial_board, 8))
