## import part
import numpy as np

'''
Description: This program demonstrates the Conway’s Game of Life problem.

Member:
Christina Hu 	
Jie Niu 	    
Wansi Liang 	
Gary Wang 	    
Derek Huang 	
'''

'''
The followings are height and width defined in the program 
'''
# height x width gridBoard of 0’s and 1’s, where 4<=height<=100 and 4<=width<=100
# random gridBoard size,
height = 100  # height is the height of gridBoard
width = 100  # width is the width of gridBoard

'''
The followings are variables defined in the program 
'''
# LIVE and DEAD represent the states of cell
LIVE = 1  # 1 means cell is live
DEAD = 0  # 0 means cell is dead
board = None
gridBoard = []
outputArray = []


'''
The following part is responsible for opening the file and reading the input from './inLife.txt'
'''
file = open('./inLife.txt', 'r')
for countStarter, line in enumerate(file.readlines()):
    line = line.strip('\n')
    if countStarter == 0:
        firstLine = line.strip()
        numberOfGenerations = int(firstLine)
    else:
        gridBoard.append([LIVE if int(currentState) == 1 else DEAD for index, currentState in enumerate(line)])
board = np.array(gridBoard)
height, width = board.shape
outputArray.append(board) # Appending the board info into outputArray array


'''
This part here is responsible for generating neighbors and producing next generations.
'''
for i in range(numberOfGenerations):
    newBoard = board.copy()  # I make a copy of the board
    for row in range(height):
        for column in range(width):
            numberOfAliveNeighbors = (board[(row + 1) % height, column] +
                                      board[(row - 1) % height, column] +
                                      board[row, (column - 1) % width] +
                                      board[row, (column + 1) % width] +
                                      board[(row - 1) % height, (column - 1) % width] +
                                      board[(row + 1) % height, (column - 1) % width] +
                                      board[(row - 1) % height, (column + 1) % width] +
                                      board[(row + 1) % height, (column + 1) % width])
            if board[row, column] != LIVE:
                if numberOfAliveNeighbors == 3:
                    newBoard[row, column] = LIVE
            else:
                if numberOfAliveNeighbors > 3:
                    newBoard[row, column] = DEAD
                elif numberOfAliveNeighbors < 2:
                    newBoard[row, column] = DEAD
    outputArray.append(newBoard) # Appending the newBoard info into outputArray array
    board = newBoard


'''
The final part here is responsible for writing into the output file './outLife.txt'
'''
file = open('./outLife.txt', 'w')
for index, a in enumerate(outputArray):
    file.write("Generation " + str(index) + "\n")
    for q in range(outputArray[index].shape[0]):
        for p in range(outputArray[index].shape[1]):
            file.write(str(outputArray[index][q,p]))
        file.write("\n")