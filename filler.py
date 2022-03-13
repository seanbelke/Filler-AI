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
        return '\n'.join([x.__repr__() for x in FillerBoard.unrotate_grid(self.board)])
    
    def unrotate_grid(grid):
        rows = len(grid)
        cols = len(grid[0])
        return [[grid[r][c] for r in range(rows)] for c in range(cols -1, -1, -1)]

    def get_player_a_color(self):
        return self.board[0][0]
    
    def get_player_b_color(self):
        return self.board[self.width - 1][self.height - 1]
    
    def get_player_region(self, player):
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
    def __init__(self, initial, max_search_depth = 4):
        super().__init__(initial, ['A', 'B'])
        self.search_depth = max_search_depth

    
    def to_move(self, s):
        return s.player

    def actions(self, s):
        actions = set([Color.RED, Color.GREEN, Color.BLUE, Color.BLACK, Color.YELLOW, Color.PURPLE])
        actions.discard(s.get_player_a_color())
        actions.discard(s.get_player_b_color())
        new_actions = set([])
        for a in actions:
            if any([a in row for row in s.board]):
                new_actions.add(a)
        return new_actions
    
    def result(self, s, a):
        newboard = [[col for col in row] for row in s.board]
        region = s.get_player_region(s.player)
        for (x, y) in region:
            newboard[x][y] = a
        new_player = 'A'
        if s.player == 'A':
            new_player = 'B'
        return FillerBoard(newboard, new_player)
    
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
        if depth >= self.search_depth:
            return True
        else:
            return self.is_terminal(s)
    
    def utility(self, s, p):
        notp = 'A'
        if p == 'A':
            notp = 'B'
        return len(s.get_player_region(p)) - len(s.get_player_region(notp))

def rotate_grid(grid):
    rows = len(grid)
    cols = len(grid[0])
    newgrid = [[grid[r][c] for r in range(rows)] for c in range(cols)]
    return [[newgrid[r][c] for c in range(rows - 1, -1, -1)] for r in range(cols)]



def play_perfect_game(game, initial=None):
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
        # move = alpha_beta_minimax(game, s)
        move = None
        if game.to_move(s) == 'A':
            move = alpha_beta_minimax(game, s)
        else:
            move = Color(int(input("move: ")))
        s = game.result(s, move)
    a_score = len(s.get_player_region('A'))
    b_score = len(s.get_player_region('B'))
    print('A Score: ' + str(a_score))
    print('B Score: ' + str(b_score))
    print(s)
    print()

    a_util = game.utility(s, 'A')
    b_util = game.utility(s, 'B')
    winner = 'A'
    if b_score > a_score:
        winner = 'B'
    elif b_score == a_score:
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
    [GR, BU, RD, YL, PU, BK, YL, BU],
    [YL, GR, BK, BU, BK, YL, PU, RD],
    [PU, BK, RD, PU, BU, GR, RD, PU],
    [BK, PU, BU, YL, GR, RD, PU, BK],
    [BU, RD, BK, RD, PU, BU, RD, GR],
    [PU, BK, GR, YL, GR, PU, GR, BK],
    [GR, RD, YL, GR, BU, BK, RD, GR]
]

initial_board = FillerBoard(rotate_grid(initial_grid), 'B')

game = Filler(initial_board)
play_perfect_game(Filler(initial_board, 8))


        



        
        

        


