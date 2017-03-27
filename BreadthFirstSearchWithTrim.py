import BaseElements
import time
import copy
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
landingArea = BaseElements.landingArea
startPosition = (4, 4)

validMoves = BaseElements.calculateAllValidMovesForSquare()

def canGetHome(currentPos, visited):
    homeSquares = [(2, 3), (2, 5), (3, 2), (5, 2), (5, 6), (6, 3), (6, 5)]
    for square in homeSquares:
        if visited[square[0]][square[1]] == 0:
            return True
    if(currentPos in homeSquares):
        return True
    return False



def calculateNextSteps(currentPosition,currentScore,currentPath, visited):
    newElements = []
    for move, score in validMoves[currentPosition[0]][currentPosition[1]].iteritems():
        newPosition = BaseElements.makeMove(currentPosition,move)
        newVisited = copy.deepcopy(visited)
        newPath = copy.copy(currentPath)
        newPath.append(move)
        newVisited[newPosition[0]][newPosition[1]] = 1
        pathFinished = newPosition == (4,4)
        if pathFinished:
            finishedPaths.append((newPosition,newPath,currentScore + score, pathFinished, newVisited))
        else:
            newElements.append((newPosition,newPath,currentScore + score, pathFinished, newVisited))
    return newElements


def getNPlus1Paths(steps):
    newSteps = []
    for a in steps:
        if not a[3]:
            newSteps.extend(calculateNextSteps(a[0], a[2], a[1], a[4]))
    return newSteps

def clean(paths):
    #Don't trim aggressively near the end
    if len(paths) < 75000:
        return paths, True

    sortedPaths = sorted(paths, key = lambda path: path[2], reverse=True)

    for path in list(sortedPaths):
        visited = path[4]
        currentPos = path[0]
        if not canGetHome(currentPos, visited):
            sortedPaths.remove(path)
    if len(paths) < 100000:
        trimmedList = sortedPaths[:10000]
    else:
        trimmedList = sortedPaths[:1000]
    print("Cleaning from " + str(len(sortedPaths)) + " to " + str(len(trimmedList)))
    return trimmedList, False


def createNextPaths():
    global finishedPaths
    nPaths = calculateNextSteps((4,4),0,[],BaseElements.cleanVisited)
    cleanNext = False
    for i in range(70):
        startTime = time.time()
        nPlus1Paths = getNPlus1Paths(nPaths)
        print(str(i + 2) + " - " + str(time.time() - startTime) + "  " + str(len(nPaths)) + " " + str(len(nPlus1Paths)))
        if (i > 1 and (i % 2 == 0)) or cleanNext:
            nPaths, cleanNext = clean(nPlus1Paths)
        else:
            nPaths = nPlus1Paths

    sortedPaths = sorted(nPaths, key=lambda path: path[2], reverse=True)
    if len(sortedPaths) == 0:
        maxFP = sorted(finishedPaths, key=lambda path: path[2], reverse=True)[0]
        print(maxFP)
        print(len(maxFP[1]))
    else:
        print("done " + str(len(nPaths)) + " maxScore:" + str(sortedPaths[0][2]))

finishedPaths = []
startTime = time.time()
createNextPaths()
sortedPaths = sorted(finishedPaths, key=lambda path: path[2], reverse=True)

print("MAX FINISHED PATH SCORE:" + str(sortedPaths[0][2]))
print time.time() - startTime
