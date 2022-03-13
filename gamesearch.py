import numpy as np

class Game:
    def __init__(self, initial, players, terminal=None):
        self.initial = initial  # the initial state of the game
        self.players = players
        self.terminal = terminal

    def to_move(self, s):
        """Returns the player whose turn it if we are in state s."""
        raise NotImplementedError

    def actions(self, s):
        """Returns the set of legal moves from state s."""
        raise NotImplementedError

    def result(self, s, a):
        """Defines the transition model, i.e. the state that results from taking action a in state s."""
        raise NotImplementedError

    def is_terminal(self, s):
        """Tests the state to see if it is a terminal state for the game, which means the game is over.
        For many games this will not be sufficient, and will need to be overridden."""
        if isinstance(self.terminal, list):
            return s in self.terminal
        else:
            return s == self.terminal
        
    def is_cutoff(self, s, depth):
        return self.is_terminal(s)

    def utility(self, s, p):
        """Defines the final numeric value to player p when the game ends in terminal state s."""
        raise NotImplementedError

def alpha_beta_minimax(game, state):
    player = game.to_move(state)
    value, move = max_value_ab(game, state, player, -np.Inf, np.Inf, 0)
    return move

def max_value_ab(game, state, player, alpha, beta, depth):
    if game.is_cutoff(state, depth):
        return game.utility(state, player), None

    value, move = -np.Inf, None
    for a in game.actions(state):
        v, _ = min_value_ab(game, game.result(state, a), player, alpha, beta, depth + 1)
        if v > value:
            value, move = v, a
            alpha = max(v, alpha)
        if v >= beta:
            return value, move
    return value, move

def min_value_ab(game, state, player, alpha, beta, depth):
    if game.is_cutoff(state, depth):
        return game.utility(state, player), None

    value, move = np.Inf, None
    for a in game.actions(state):
        v, _ = max_value_ab(game, game.result(state, a), player, alpha, beta, depth + 1)
        if v < value:
            value, move = v, a
            alpha = min(v, alpha)
        if v <= alpha:
            return value, move
    return value, move


def minimax(game, state):
    player = game.to_move(state)
    value, move = max_value(game, state, player, 0)
    return move

def max_value(game, state, player, depth):
    if game.is_cutoff(state, depth):
        return game.utility(state, player), None

    value, move = -np.Inf, None
    for a in game.actions(state):
        v, _ = min_value(game, game.result(state, a), player, depth + 1)
        if v > value:
            value, move = v, a

    return value, move

def min_value(game, state, player, depth):
    if game.is_cutoff(state, depth):
        return game.utility(state, player), None

    value, move = np.Inf, None
    for a in game.actions(state):
        v, _ = max_value(game, game.result(state, a), player, depth + 1)
        if v < value:
            value, move = v, a

    return value, move