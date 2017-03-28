import sys
import base_elements


def check_solution(start_position, solution):
    score = 0
    move_count = 0
    visited = base_elements.clean_visited
    moves = solution.split("|")
    current_position = start_position
    for move in moves:
        move_count += 1
        for step in move.split(","):
            if step == 'N':
                current_position = (current_position[0] - 1, current_position[1])
            elif step == 'E':
                current_position = (current_position[0], current_position[1] + 1)
            elif step == 'S':
                current_position = (current_position[0] + 1, current_position[1])
            elif step == 'W':
                current_position = (current_position[0], current_position[1] - 1)

            if current_position[0] > 8 or current_position[1] > 8 or current_position[0] < 0 or current_position[1] < 0:
                print('YOU CRASHED INTO THE MOUNTAINS')
                sys.exit(0)
            elif base_elements.landing_aread[current_position[0]][current_position[1]] == 'X':
                print('YOU TUMBLED INTO A CREVICE AT MOVE ' + str(move_count) + " - " + move)
                sys.exit(0)
            else:
                value = base_elements.landing_aread[current_position[0]][current_position[1]]
                if value == 'S':
                    value = 0
                score += value
        if visited[current_position[0]][current_position[1]] == 1:
            print('YOU RETURNED TO THE SAME PLACE TWICE ON MOVE ' + str(move_count) + " - " + move)
            sys.exit(0)
        else:
            visited[current_position[0]][current_position[1]] = 1

    if not current_position[0] == 4 and not current_position[1] == 4:
        print("YOU DIDN'T MAKE IT BACK TO THE START!")
        sys.exit(0)
    print("You scored " + str(score) + " in " + str(move_count) + " moves.")
    print(solution)


solution = "W,W,N|W,N,N|S,S,W|E,E,S|E,E,N|E,N,N|N,E,E|W,S,S|N,N,W|E,E,S|S,W,W|E,N,N|W,W,S|N,W,W|W,S,S|N,E,E|W,W,N|S,S,W|E,S,S|E,E,S|S,S,W|E,E,N|W,S,S|N,W,W|E,E,N|S,S,W|N,E,E|W,W,N|N,N,E|W,N,N|N,W,W|E,S,S|N,N,E|N,E,E|E,E,S|W,S,S|N,E,E|S,S,W|S,W,W|N,N,W|W,S,S|N,W,W|S,S,E|S,E,E|N,E,E|E,S,S|E,E,N|N,N,W|N,W,W|E,E,N|S,S,E|S,S,W|S,W,W|E,N,N|N,N,E|W,W,S|E,S,S|E,E,N|S,S,W|W,W,N|N,N,E|N,W,W"
check_solution((4, 4), solution)
