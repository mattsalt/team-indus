import time
import copy
import base_elements

validMoves = base_elements.calculate_all_valid_moves_for_square()


def can_get_home(current_pos, visited):
    home_squares = [(2, 3), (2, 5), (3, 2), (5, 2), (5, 6), (6, 3), (6, 5)]
    for square in home_squares:
        if visited[square[0]][square[1]] == 0:
            return True
    if (current_pos in home_squares):
        return True
    return False


def calculate_next_steps(current_position, current_score, current_path, visited):
    new_elements = []
    for move, score in validMoves[current_position[0]][current_position[1]].iteritems():
        new_position = base_elements.make_move(current_position, move)
        new_visited = copy.deepcopy(visited)
        new_path = copy.copy(current_path)
        new_path.append(move)
        new_visited[new_position[0]][new_position[1]] = 1
        path_finished = new_position == (4, 4)
        if path_finished:
            finished_paths.append((new_position, new_path, current_score + score, path_finished, new_visited))
        else:
            new_elements.append((new_position, new_path, current_score + score, path_finished, new_visited))
    return new_elements


def get_n_plus_1_paths(steps):
    new_steps = []
    for a in steps:
        if not a[3]:
            new_steps.extend(calculate_next_steps(a[0], a[2], a[1], a[4]))
    return new_steps


def clean(paths):
    # Don't trim aggressively near the end
    if len(paths) < 75000:
        return paths, True

    sorted_paths = sorted(paths, key=lambda path: path[2], reverse=True)

    for path in list(sorted_paths):
        visited = path[4]
        current_pos = path[0]
        if not can_get_home(current_pos, visited):
            sorted_paths.remove(path)
    if len(paths) < 100000:
        trimmed_list = sorted_paths[:10000]
    else:
        trimmed_list = sorted_paths[:1000]
    print("Cleaning from " + str(len(sorted_paths)) + " to " + str(len(trimmed_list)))
    return trimmed_list, False


def create_next_paths():
    global finished_paths
    n_paths = calculate_next_steps((4, 4), 0, [], base_elements.clean_visited)
    clean_next = False
    for i in range(70):
        start_time = time.time()
        n_plus1_paths = get_n_plus_1_paths(n_paths)
        print(
        str(i + 2) + " - " + str(time.time() - start_time) + "  " + str(len(n_paths)) + " " + str(len(n_plus1_paths)))
        if (i > 1 and (i % 2 == 0)) or clean_next:
            n_paths, clean_next = clean(n_plus1_paths)
        else:
            n_paths = n_plus1_paths

    sorted_paths = sorted(n_paths, key=lambda path: path[2], reverse=True)
    if len(sorted_paths) == 0:
        max_f_p = sorted(finished_paths, key=lambda path: path[2], reverse=True)[0]
        print(max_f_p)
        print(len(max_f_p[1]))
    else:
        print("done " + str(len(n_paths)) + " maxScore:" + str(sorted_paths[0][2]))


finished_paths = []
start_time = time.time()
create_next_paths()
sorted_paths = sorted(finished_paths, key=lambda path: path[2], reverse=True)

print("MAX FINISHED PATH SCORE:" + str(sorted_paths[0][2]))
print time.time() - start_time
