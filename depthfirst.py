import time
import base_elements

validMoves = base_elements.calculate_all_valid_moves_for_square()
bestScore = 0


def can_get_home(current_pos, visited):
    home_squares = [(2, 3), (2, 5), (3, 2), (5, 2), (5, 6), (6, 3), (6, 5)]
    for square in home_squares:
        if visited[square[0]][square[1]] == 0:
            return True
    if (current_pos in home_squares):
        return True
    return False


def get_paths(position, move, path, visited, cumulative_score, score):
    global bestScore
    path.append(move)
    cumulative_score += score
    visited[position[0]][position[1]] = 1
    if position == (4, 4) and len(path) >= 2:
        if cumulative_score > bestScore:
            bestScore = cumulative_score
            print(cumulative_score)
            base_elements.print_path(path)
    elif can_get_home(position, visited):
        dict = validMoves[position[0]][position[1]]
        # sorted_moves = sorted(dict, key=lambda x: dict[x], reverse=True)
        sorted_moves = dict.keys()
        for move in sorted_moves:
            new_score = dict[move]
            new_position = base_elements.make_move(position, move)
            if visited[new_position[0]][new_position[1]] == 0:
                get_paths(new_position, move, path, visited, cumulative_score, new_score)
    path.pop()
    cumulative_score -= score
    visited[position[0]][position[1]] = 0


startTime = time.time()
get_paths((4, 4), '', [], base_elements.clean_visited, 0, 0)
print "DURATION:" + str(time.time() - startTime)
