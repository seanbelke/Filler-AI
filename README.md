# Filler-AI

## Background

*Filler* is a 2-player game on the GamePigeon platform for iOS devices.  The game consists of a grid of colored tiles (red, green, blue, black, yellow, and purple), which are initially scrambled in such a way that no two adjacent tiles are the same color.

![Initial Filler Board](images/filler-initial.png)

At the start of the game, each player has a single tile that belongs to their "region".  From each player's perspective, this tile is on the bottom left corner of their screen, because the game is mirrored when presented to each player.  However, for the purposes of designing this AI, and within this README, I'll refer to the filler board as if there is a Player "A" whose region starts at the bottom left of the grid, and a player "B" whose region starts at the top right corner of the grid.  In the example initial configuration shown above, you can see that Player A has a single black tile as its region, and Player B has a single green tile as its region.  

Each player takes turns selecting a new color for their region.  The player can select any of the 6 colors other than its own color, or its opponent's color.  Upon selecting a new color, all tiles of that color that were adjacent to the player's region previously are now absorbed into that player's region, *and* the player's entire region will change to that color.  The game will display a score for each player as the game progresses.  Each player's score is the number of tiles in that player's region.

Formally, the game ends when every tile on the grid is part of one of the two player's regions, but it's worth noting that once either player has a score of 29 or more, they are guaranteed to win the game because there are exactly 56 (28 times 2) tiles on the board, and there is no way for either player's region to get smaller as the game progresses.

Here is an example of what the grid may look like in the middle of the game.  Player A's region is green, and Player B's region is blue.

![Partial Game](images/filler-partial.jpg)

## AI Design

The algorithm used to play the game is a depth-limited minimax with alpha-beta pruning for improved efficiency.  The depth limit can be chosen by the user.  Each turn taken by either player represents an additional layer of depth, so for example if you want the AI to be able to see 4 rounds ahead, you'll need to set the depth limit to 8 (which is the current setting).  

The AI considers any game states in which a player has a guaranteed win (a score of 29 or more, as described above) to be a terminal state, and will end its search at that point.  Note that this means the AI is not useful for maximizing a player's score once that threshold has been passed, because it will consider every state to be terminal at that point.

## Usage Instructions

If you want the AI to suggest a move to you while playing a human opponent on GamePigeon, you'll have to change the code to reflect your initial board configuration.  The given initial configuration represents the image of the initial board shown above, as an example of how to input the starting configuration.  It also is set to let player 'A' go first, which is controlled by the AI.  On GamePigeon, whoever sends the game goes *second*, and sometimes the board shown is not accurate until the other person has taken his/her first turn.  So, in this case you should wait to input the initial board configuration until the other player has taken a turn.

There are various other ways to use this program.  With simple modifications to `play_game` in `filler.py`, you can make the AI play itself, if you would like to see how that works out.

Make sure you have the latest version of python 3 installed.  You may need to install packages if you get errors when trying to run this program.  

Run the program in your terminal with the command `py filler.py`

## Other notes, references, etc.

The game search algorithms were implemented using the pseudocode given in the book *Artificial Intelligence: A Modern Approach, Fourth Edition* by Peter Norvig and Stuart Russell, although the algorithms are common in AI and were not invented by the authors.

I left the implementation of standard (depth-limited) minimax in gamesearch.py even though it is not used, for my own reference and educational purposes.
