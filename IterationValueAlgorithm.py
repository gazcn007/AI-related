import numpy
import copy

def reachBoundary(grid, state):
    rows = len(grid)
    cols = len(grid[0])
    x = state[0]
    y = state[1]
    if x < 0 or x > rows-1:
        return False
    if y < 0 or y > cols-1:
        return False
    return True

def getNextStates():
    nextStates = {'down': (1,0),'left': (0,-1),'right': (0,1),'up':(-1,0)} #for 2c
    #nextStates = {'left': (0,-1)} #for 2b
    return nextStates

def MaxValueFromBellmanEquation(rewardMatrix,gridWorld, gamma, state):
    nextStates = getNextStates()
    immediateReward = rewardMatrix[state[0]][state[1]]
    immediateValue = gridWorld[state[0]][state[1]]
    maxValue = -10000
    for action in nextStates.keys():
         #for 0.8 probability of move success 
        coordinates =  tuple(sum(pair) for pair in zip (nextStates[action],state))
        valueList = list()
        stateLegal = reachBoundary(gridWorld, coordinates)
        if not stateLegal: # bounce back to same state's value and reward
            valueList.append(immediateValue)
        else: # take value from the nex state
            valueList.append(gridWorld[coordinates[0]][coordinates[1]])
        #for 0.2 probability of move failure, which agent stays at same place
        coordinates=state;
        stateLegal = reachBoundary(gridWorld, coordinates)
        if not stateLegal: # bounce back to same state's value and reward
            valueList.append(immediateValue)
        else: # take value from the nex state
            valueList.append(gridWorld[coordinates[0]][coordinates[1]]);
        value = immediateReward + gamma * (valueList[0]*0.8+valueList[1]*0.2);
        maxValue = max(value, maxValue)
    return maxValue

def converged(previous, current):
    mat1 = numpy.matrix(previous)
    mat2 = numpy.matrix(current)
    if numpy.allclose(mat2, mat1):
        return True
    else:
        return False

def printQValues(gridWorld):
    for row in gridWorld:
        for item in row:
            print "|" ,(item),"\t",
        print "|"

def valueIteration():
    gamma = 0.95
    gridWorld = [[0,0,0],[0,0,0]];
    previous = copy.deepcopy(gridWorld)
    RewardMatrx = [[0,0,200],[100,0,-100]];
    count=0
    while(True):    
        for row in range(len(gridWorld)):
            for column in range(len(gridWorld[0])):
                if RewardMatrx[row][column] != -10000:
                    gridWorld[row][column] = MaxValueFromBellmanEquation(RewardMatrx,gridWorld, gamma, (row, column))                    
        
        if(converged(previous, gridWorld)):
            break
        else:
            previous = copy.deepcopy(gridWorld)
        count += 1

    printQValues(gridWorld)
        
valueIteration()

