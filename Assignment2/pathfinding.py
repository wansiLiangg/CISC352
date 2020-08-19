'''
Description: This program shows the path to find a goal.

Member:
Christina Hu 	
Jie Niu 	    
Wansi Liang 	
Gary Wang 	    
Derek Huang 	
'''

## import part
import numpy as np
import os
from heapq import *
from copy import copy, deepcopy


## a class to define a point in the maze above. The location, cost and origin they come from of it is stored
class Point:
    def __init__(self, x, y, came_from=None, cost_so_far=float('inf')):
        self.x = x
        self.y = y
        self.came_from = came_from
        self.cost_so_far = cost_so_far

    ## a function to break ties in the priority queue, but it actually does not matter which point comes earlier.
    def __lt__(self, other):
        return True

## a function to read a text input file and saves them as 2D arrays
def readFile(filename):
    boards = []
    with open(filename) as f:
        file = f.readlines()
    board = []
    for r in file:
        if r == '\n':
            boards.append(board)
            board = []
        else:
            board.append(list(r.rstrip('\n')))
    boards.append(board)
    return boards

## output our solutions.
def outputFile(greedyAnswer, AAnswer, filename):
    with open(filename,'w') as out:
        for i in range(len(greedyAnswer)):
            out.write('Greedy\n')
            for r in greedyAnswer[i]:
                line = ''.join(r)+"\n"
                out.write(line)
            out.write('A*\n')
            for r in AAnswer[i]:
                line = ''.join(r)+"\n"
                out.write(line)
            out.write("\n")

## solve the graphs without allowing to move diagonally
def solveXY():
    grids = readFile('pathfinding_a.txt')
    greedyAnswer = []
    AAnswer = []
    for g in grids:
        maze = Graph(g)
        greedyAnswer.append(maze.greedySearchAlgorithm(diagonal=False))
        AAnswer.append(maze.AStarSearchAlgorithm(diagonal=False))
    outputFile(greedyAnswer, AAnswer, 'pathfinding_a_out.txt')

## solve the graphs with allowing to move diagonally.
def solveDiag():
    '''
        Solves the graphs, allowing diagonal movement as well as vertical/horizontal
    '''
    grids = readFile('pathfinding_b.txt')
    greedyAnswer = []
    AAnswer = []
    for g in grids:
        maze = Graph(g)
        greedyAnswer.append(maze.greedySearchAlgorithm(diagonal=True))
        AAnswer.append(maze.AStarSearchAlgorithm(diagonal=True))
    outputFile(greedyAnswer, AAnswer, 'pathfinding_b_out.txt')

class Graph:
    ## A maze is defined and stored as a 2d array.
    def __init__(self, grid):
        self.grid = grid
        self.start = self.pointfinder('S')
        self.goal = self.pointfinder('G')

    ## a function to find the location of the start of the goal.
    def pointfinder(self, target):
        for r in range(len(self.grid)):
            for c in range(len(self.grid[0])):
                if self.grid[r][c] == target:
                    return Point(c, r)

    ## Grveedy algorithm to sole this maze. (allow/not allow to move diagonally)
    def greedySearchAlgorithm(self, diagonal = False):
        frontier = []
        visited = [[False for i in range(len(self.grid[0]))] for j in range(len(self.grid))]
        start = self.start
        goal = self.goal
        heappush(frontier, (0, start))
        visited[start.y][start.x] = True
        while not len(frontier)==0:
            current = heappop(frontier)[1]
            x = current.x
            y = current.y
            if self.grid[y][x] == 'G':
                break
            neighbours = self.getXYNeighbours(current) \
                + (self.getDiagNeighbours(current) if diagonal else [])
            for next in neighbours:
                if not visited[next.y][next.x]:
                    heuristic = self.chebyshev(goal, next) if diagonal else self.manhattan(goal, next)
                    heappush(frontier, (heuristic, next))
                    next.came_from = current
                    visited[next.y][next.x] = True
        solution = deepcopy(self.grid)
        current = current.came_from
        while current.came_from != None:
            solution[current.y][current.x] = 'P'
            current = current.came_from
        return solution

    ## A* algorithm to solve this maze. (allow/not allow to move diagonally)
    def AStarSearchAlgorithm(self, diagonal=False):
        frontier = []
        start = self.start
        start.cost_so_far = 0
        goal = self.goal
        heappush(frontier, (0, start))
        while not len(frontier)==0:
            current = heappop(frontier)[1]
            x = current.x
            y = current.y
            if self.grid[y][x] == 'G':
                break
            neighbours = self.getXYNeighbours(current) \
                + (self.getDiagNeighbours(current) if diagonal else [])
            for next in neighbours:
                new_cost = current.cost_so_far + 1
                if new_cost < next.cost_so_far:
                    next.cost_so_far = new_cost
                    heuristic = self.chebyshev(goal, next) if diagonal else self.manhattan(goal, next)
                    priority = new_cost + heuristic
                    heappush(frontier, (priority, next))
                    next.came_from = current
        solution = deepcopy(self.grid)
        current = current.came_from
        while current.came_from != None:
            solution[current.y][current.x] = 'P'
            current = current.came_from
        return solution

    ## a function to find the neighbours of a point horizontally and vertically
    def getXYNeighbours(self, p):
        neighbours = []
        x = p.x
        y = p.y
        grid = self.grid
        if x > 0 and grid[y][x-1] != 'X':
            neighbours.append(Point(x-1, y, came_from=p))
        if x < len(grid[0])-1 and grid[y][x+1] != 'X':
            neighbours.append(Point(x+1, y, came_from=p))
        if y > 0 and grid[y-1][x] != 'X':
            neighbours.append(Point(x, y-1, came_from=p))
        if y < len(grid)-1 and grid[y+1][x] != 'X':
            neighbours.append(Point(x, y+1, came_from=p))
        return neighbours

    ## a function to find the neighbours of a point diagonally
    def getDiagNeighbours(self, p):
        neighbours = []
        grid = self.grid
        x = p.x
        y = p.y
        if x>0 and y>0 and grid[y-1][x-1] != 'X': # up-left
            neighbours.append(Point(x-1, y-1, came_from=p))
        if x>0 and y<len(grid)-1 and grid[y+1][x-1] != 'X': # down-left
            neighbours.append(Point(x-1, y+1, came_from=p))
        if x<len(grid[0])-1 and y>0 and grid[y-1][x+1] != 'X': # up-right
            neighbours.append(Point(x+1, y-1, came_from=p))
        if x<len(grid[0])-1 and y<len(grid)-1 and grid[y+1][x+1] != 'X': #down-right
            neighbours.append(Point(x+1, y+1, came_from=p))
        return neighbours

    ## to find the chebyshev distance from a to b
    def chebyshev(self, a, b):
        return max(abs(b.x-a.x), abs(b.y-a.y))

    ## to find the Manhattan distance from a to b
    def manhattan(self, a, b):
        return abs(b.x-a.x) + abs(b.y-a.y)

solveXY()
solveDiag()
