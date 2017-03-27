import BaseElements
import time

landingArea = BaseElements.landingArea
startPosition = (4, 4)

validMoves = BaseElements.calculateAllValidMovesForSquare()

bestScore = 0
def getPaths(position,move, path, visited, cumScore, score):
    global bestScore
    path.append(move)
    cumScore += score
    visited[position[0]][position[1]] = 1
    if position == (4, 4) and len(path) >= 2:
        if cumScore > bestScore:
            bestScore = cumScore
            BaseElements.printPath(path)
            print(cumScore)
    else:
        dict = validMoves[position[0]][position[1]]
        sortedMoves = sorted(dict, key=lambda x: dict[x], reverse=True)
        for move in sortedMoves:
            newScore = dict[move]
            newPosition = BaseElements.makeMove(position,move)
            if visited[newPosition[0]][newPosition[1]] == 0:
                getPaths(newPosition, move, path, visited, cumScore, newScore)
    path.pop()
    cumScore -= score
    visited[position[0]][position[1]] = 0



startTime = time.time()
getPaths((5, 6),'SEE', [], BaseElements.cleanVisited, 0,3)
print "DURATION:" + str(time.time() - startTime)
