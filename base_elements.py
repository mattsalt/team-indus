import sys
import random
import copy

# Define Steps
N = (-1, 0)
E = (0, 1)
S = (1, 0)
W = (0, -1)

# Utility copy of clean visited array
cleanVisited = [  # (y,x)
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
]

# Enumerate possible moves, rover moves like a knight in chess
possibleMoves = {"NNE": [N, N, E], "NNW": [N, N, W], "NEE": [N, E, E], "NWW": [N, W, W],
                 "ENN": [E, N, N], "ESS": [E, S, S], "EEN": [E, E, N], "EES": [E, E, S],
                 "SEE": [S, E, E], "SWW": [S, W, W], "SSE": [S, S, E], "SSW": [S, S, W],
                 "WSS": [W, S, S], "WNN": [W, N, N], "WWS": [W, W, S], "WWN": [W, W, N]}

possibleFullMoves = {"NNE": (-2, 1), "NNW": (-2, -1), "NEE": (-1, 2), "NWW": (-1, -2),
                     "ENN": (-2, 1), "ESS": (2, 1),   "EEN": (-1, 2), "EES": (1, 2),
                     "SEE": (1, 2),  "SWW": (1, -2),  "SSE": (2, 1),  "SSW": (2, -1),
                     "WSS": (2, -1), "WNN": (-2, -1), "WWS": (1, -2), "WWN": (-1, -2)}

landingArea = [  # (y,x)
    ['X', 1 , 2 ,-1 , 4 , 1 , 4 , 2 ,-2],
    [-2 , 4 , 1 , 0 ,-2 ,-1 , 0 , 1 , 2],
    [ 1 , 2 ,-1 , 1 ,'X', 4 , 2 ,-1 , 1],
    [ 0,  2,  0, -2,  2,  1, 'X', 2 ,-1],
    [-2,  1,  4,  1, 'S',-1 , 4,  1 ,-2],
    [-1, 'X', 1, -1,  0,  1,  2, -2 , 0],
    [ 2,  4, -2,  1,  0,  2, -1, 'X', 2],
    [ 1,  0,  2,  4, -1, -2,  1,  0 , 1],
    [ 0, -2, -1,  1, 'X', 1,  2, -1 , 4]
]


# Pretty print methods
def print_grid(grid):
    for i in range(len(grid)):
        print(grid[i])


def print_path(path):
    for move in path:
        i = 0
        for step in move:
            if (i == 2):
                # Use sys.stdout to avoid new lines on print without imported future
                sys.stdout.write(step)
                sys.stdout.write("|")
            else:
                sys.stdout.write(step + ",")
            i += 1
    sys.stdout.write("\n")
    sys.stdout.flush()


def take_step(position, step):
    return (position[0] + step[0], position[1] + step[1])


def make_move(position, move_key):
    move = possibleFullMoves[move_key]
    new_position = (position[0] + move[0], position[1] + move[1])
    return new_position


# Return random move from a list of moves, all moves equally likely
def get_random_move(moves):
    random_move = random.randrange(0, len(moves))
    return moves[random_move]


# Return a random move with a positive score. Moves with negative scores are ignored.
def get_random_positive_move(moves):
    r = random.randrange(0, len(moves))
    r_key = moves.keys()[r]
    move_score = moves[r_key]
    while move_score < 0:
        r = random.randrange(0, len(moves))
        r_key = moves.keys()[r]
        move_score = moves[r_key]
    return r_key


# Finds valid moves on a given grid from the current position assuming you can only land on a square once.
# Grid doesn't loop. Can't land on any squares with 'X'.
def find_valid_moves(grid, current_pos, visited):
    valid_moves = {}
    for key, move in possibleMoves.iteritems():
        score = 0
        xy = current_pos
        valid = True
        i = 0
        for step in move:
            xy = take_step(xy, step)
            if xy[0] >= len(grid) or xy[1] >= len(grid) or xy[0] < 0 or xy[1] < 0:
                valid = False
                break
            elif grid[xy[0]][xy[1]] == 'X':
                valid = False
                break
            elif i == 2 and visited[xy[0]][xy[1]] == 1:
                valid = False
                break
            else:
                value = landingArea[xy[0]][xy[1]]
                if value != 'S':
                    score += value
            i = i + 1
        if valid:
            valid_moves[key] = score
    return valid_moves


def calculate_all_valid_moves_for_square():
    valid_moves = copy.deepcopy(cleanVisited)
    for columnIndex, column in enumerate(landingArea):
        for rowIndex, row in enumerate(column):
            if not landingArea[columnIndex][rowIndex] == 'X':
                valid_moves[columnIndex][rowIndex] = find_valid_moves(landingArea, (columnIndex, rowIndex),
                                                                      cleanVisited)
            else:
                valid_moves[columnIndex][rowIndex] = []

    return valid_moves
