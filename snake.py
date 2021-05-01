# CSCI 4478 - Dr Vahid Behzadan
# Name: game.py
# Description: Classes to run a game of snake
# Reference: https://www.youtube.com/watch?v=CD4qAhfFuLo&t=1734s
# Reference: https://pastebin.com/embed_js/jB6k06hG
# Revision: 4/22/2021

import math
import random

import pygame
import tkinter as tk
from tkinter import messagebox

# Graphing
import pandas as pd
import matplotlib.pyplot as plot
import numpy as np
from datetime import datetime

file = "results.txt"


# ------------------------------------------------- Code setting up the basics of the snake game

class cube(object):
    rows = 20
    w = 500

    def __init__(self, start, dirnx=1, dirny=0, color=(255, 0, 0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))
        if eyes:
            centre = dis // 2
            radius = 3
            circleMiddle = (i * dis + centre - radius, j * dis + 8)
            circleMiddle2 = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)


class snake(object):
    body = []
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1

        self.walls = []
        self.walls.append(self.head)
        self.score = 0

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            for key in keys:
                # print("Head position:", self.head.pos) # lets us see grid pos for head
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                if c.dirnx == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows - 1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows - 1:
                    c.pos = (0, c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows - 1:
                    c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows - 1)
                else:
                    c.move(c.dirnx, c.dirny)

    def moveAuto(self, key):  # use this move method when directions are generated by successor method
        # todo: feed only actions into moveAuto - successors will have state, action, cost
        # print(key)

        if key == "LEFT":
            self.dirnx = -1
            self.dirny = 0
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        elif key == "RIGHT":
            self.dirnx = 1
            self.dirny = 0
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        elif key == "UP":
            self.dirnx = 0
            self.dirny = -1
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        elif key == "DOWN":
            self.dirnx = 0
            self.dirny = 1
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                if c.dirnx == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows - 1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows - 1:
                    c.pos = (0, c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows - 1:
                    c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows - 1)
                else:
                    c.move(c.dirnx, c.dirny)
        # exit()

    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

        self.walls = self.body
        self.score = 0

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0] - 1, tail.pos[1])))
            self.walls = self.body
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0] + 1, tail.pos[1])))
            self.walls = self.body
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1] - 1)))
            self.walls = self.body
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1] + 1)))
            self.walls = self.body

        global allWalls
        allWalls = self.body

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)

    def isGoalState(self, current_pos):
        if current_pos == tempFood.pos:
            # print("Goal state!")
            return True
        else:
            return False

    def getStartState(self):
        return self.head.pos

    def getSuccessors(self, current_pos):  # more like surrounding grid positions
        """returns a tuple of states, actions, costs"""

        '''Theoretically the max # of successors that can be generated at once should be 3: in front of the head,
        and the two sides of the head (if we have not eaten food yet we can have 4 successors). We will also make it so
        that the snake can not wrap around the screen.'''

        cost = 0
        wallPositions = []
        for x, wall in enumerate(self.walls):
            wallPositions.append(wall.pos)
        successors = []  # tuple of states, actions, cost (grid pos, direction to get there, cost to get there)
        x, y = current_pos
        possible_moves = [-1, 1]  # x or y can either stay, increase or decrease position by 1
        # print("Current pos (successor function):", current_pos)

        # look at successors for y axis
        for movesX in possible_moves:
            nextX = x + movesX  # x will move, y will stay the same
            nextY = y
            if nextX < 0 or nextX > 19:  # make sure we don't go out of bounds
                continue
            nextState = nextX, nextY
            if nextState not in wallPositions:
                if nextState != current_pos:
                    if nextState not in successors:
                        directionX = ""
                        if movesX == 1:
                            directionX = "RIGHT"
                            cost = (euclideanCost(current_pos, tempFood.pos) / 2) # prioritize left and right actions
                        elif movesX == -1:
                            directionX = "LEFT"
                            cost = (euclideanCost(current_pos, tempFood.pos) / 2)
                        successors.append((nextState, directionX, cost))

        # look at successors for y axis
        for moves in possible_moves:
            nextX = x
            nextY = y + moves  # y will move, x will stay the same
            if nextY < 0 or nextY > 19:  # make sure we don't go out of bounds
                continue
            nextState = nextX, nextY
            if nextState not in wallPositions:
                if nextState != current_pos:
                    if nextState not in successors:
                        directionY = ""
                        if moves == 1:
                            directionY = "DOWN"
                            cost = euclideanCost(current_pos, tempFood.pos)
                        elif moves == -1:
                            directionY = "UP"
                            cost = euclideanCost(current_pos, tempFood.pos)
                        successors.append((nextState, directionY, cost))

        # todo: toggle to see successors
        # print("Successors:", successors)
        return successors


def euclideanCost(position, goal): # use a euclidean measurement to use as a cost
    xy1 = position
    xy2 = goal
    return ( (xy1[0] - xy2[0]) ** 2 + (xy1[1] - xy2[1]) ** 2 ) ** 0.5


def drawGrid(w, rows, surface):
    sizeBtwn = w // rows

    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn

        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))


def redrawWindow(surface, s):
    global rows, width, snack
    surface.fill((0, 0, 0))
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width, rows, surface)
    pygame.display.update()
    # print("yum:", food.pos)


def randomSnack(rows, item):
    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break

    return (x, y)


def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


# global food
tempFood = []
startState = 0


# ------------------------------------------------- End of code setting up the basics of the snake game


# --------------------------------------------------------------------- Running the game normally
def main():
    global width, rows, s, snack, startState
    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))
    startState = (10, 10)
    # s = snake((255, 0, 0), (10, 10))
    s = snake((255, 0, 0), startState)
    snack = cube(randomSnack(rows, s), color=(0, 255, 0))
    global food, tempFood
    food = snack
    tempFood = snack
    flag = True

    clock = pygame.time.Clock()

    keyPresses = ["UP", "LEFT", "UP", "LEFT", "UP", "LEFT"]

    while flag:
        # for index, position in enumerate(s.walls):  # we can use this to see current walls (basically our body)
        #     print("Walls:", position.pos)
        pygame.time.delay(50)
        clock.tick(10)
        s.move()
        # s.moveAuto(keyPresses)
        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = cube(randomSnack(rows, s), color=(0, 255, 0))
            tempFood = food  # use this as testing to try to get food value before it changes
            food = snack  # update food to new value

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z: z.pos, s.body[x + 1:])):
                print('Score:', len(s.body))
                # message_box('You Lost!\''', \'Play again...\'')
                message_box("u die'd", "dead")
                s.reset((10, 10))
                break

        redrawWindow(win, s)

        # test line
        s.getSuccessors(s.head.pos)  # the head's position works as our current position
        s.isGoalState(s.head.pos)


# --------------------------------------------------------------------- End of running the game normally


# --------------------------------------------------------------------- Feeding snake game hardcoded directions
def feedDirections(s):
    """feedDirections demonstrates how we can input a list of directions to feed into the game"""
    global width, rows, snack
    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))
    s = snake((255, 0, 0), (10, 10))
    snack = cube(randomSnack(rows, s), color=(0, 255, 0))
    clock = pygame.time.Clock()
    flag = True

    directions = ["RIGHT", "UP", "RIGHT", "UP", "RIGHT", "UP", "LEFT", "LEFT"]

    for direction in directions:
        pygame.time.delay(50)
        clock.tick(10)
        s.moveAuto(direction)
        redrawWindow(win, s)


# --------------------------------------------------------------------- End of feeding snake game hardcoded directions

# DEFINE CONSTANTS

START_POS = (0, 0)
FOOD_POS = []
def foodPos():
    global FOOD_POS
    FOOD_POS= []
    for j in range(0, 399):  # 400 grid positions, i.e. max num of food positions can be 400
        foodX = random.randrange(19)
        foodY = random.randrange(19)
        food = foodX, foodY
        # print(food)
        FOOD_POS.append(food)
# FOOD_POS = [(10, 0), (0, 10), (10, 0), (0, 10), (10, 0)]

actionsList = [[], [], [], []]
scoreList = [0, 0, 0, 0]

# all calculated score, maintain over multiple runs
allCalcCosts = [[],[],[],[]]

# all average score, calculated once
averageCalcCosts = [[],[],[],[]]


# --------------------------------------------------------------------- DFS

# s: snake object
# i : iterator to keep track of where food will be
# slow: True go slow False go fast
def dfs_search(s, i, slow):
    from util import Stack
    global width, rows, snack, tempFood, startState, food

    def performActions(dirs, slow):
        for action in dirs:
            if slow:
                pygame.time.delay(50)
                clock.tick(10)
            s.moveAuto(action)
            redrawWindow(win, s)

    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))
    startState = START_POS
    snack = cube(FOOD_POS[i], color=(0, 255, 0))
    tempFood = snack
    clock = pygame.time.Clock()
    flag = True

    dfs_stack = Stack()  # fringe
    visited = set()
    dfs_stack.push((s.getStartState(), []))

    dead = False
    while 1:
        if dfs_stack.isEmpty():
            break
        current, directions = dfs_stack.pop()
        # print("Current pos:", current)
        if current not in visited:
            visited.add(current)
            if s.isGoalState(current):
                s.score += 1
                s.addCube()
                performActions(directions, slow)
                # print("DFS number of actions:", len(directions))
                actionsList[0].append(len(directions))
                # print("DFS score:", len(s.body))
                scoreList[0] = len(s.body)
                # scoreList[0] = s.score
            for childNode, direction, cost in s.getSuccessors(current):
                if childNode not in dfs_stack.list:
                    if childNode in visited:
                        continue
                    dfs_stack.push((childNode, directions + [direction]))


# --------------------------------------------------------------------- End DFS


# --------------------------------------------------------------------- BFS

# s: snake object
# i : iterator to keep track of where food will be
# slow: True go slow False go fast
def bfs_search(s, i, slow):
    from util import Queue
    global width, rows, snack, tempFood, startState, food

    def performActions(dirs, slow):
        for action in dirs:
            if slow:
                pygame.time.delay(50)
                clock.tick(10)
            s.moveAuto(action)
            redrawWindow(win, s)

    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))
    startState = START_POS
    snack = cube(FOOD_POS[i], color=(0, 255, 0))
    tempFood = snack
    clock = pygame.time.Clock()
    flag = True

    bfs_queue = Queue()  # fringe
    visited = set()
    bfs_queue.push((s.getStartState(), []))

    while 1:
        if bfs_queue.isEmpty():
            break
        current, directions = bfs_queue.pop()
        # print("Current pos:", current)
        if current not in visited:
            visited.add(current)
            if s.isGoalState(current):
                s.score += 1
                s.addCube()
                performActions(directions, slow)
                # print("BFS number of actions:", len(directions))
                actionsList[1].append(len(directions))
                # print("BFS score:", len(s.body))
                scoreList[1] = len(s.body)
                # scoreList[1] = s.score
            for childNode, direction, cost in s.getSuccessors(current):
                if childNode not in bfs_queue.list:
                    if childNode in visited:
                        continue
                    bfs_queue.push((childNode, directions + [direction]))


# --------------------------------------------------------------------- DFS


# --------------------------------------------------------------------- A Star

# s: snake object
# i : iterator to keep track of where food will be
# slow: True go slow False go fast
def aStar_search(s, i, slow):
    from util import Queue
    global width, rows, snack, tempFood, startState, food

    def nullHeuristic(state, problem=None):
        # trivial heuristic
        return 0

    def manhattanHeuristic(position):
        # uses distance as a score for heuristic
        xy1 = position
        xy2 = tempFood.pos
        return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])

    def performActions(dirs, slow):
        # perform actions in the game window so we can see the results
        for action in dirs:
            if slow:
                pygame.time.delay(50)
                clock.tick(10)
            s.moveAuto(action)
            redrawWindow(win, s)

    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))
    startState = START_POS
    snack = cube(FOOD_POS[i], color=(0, 255, 0))
    tempFood = snack
    clock = pygame.time.Clock()
    flag = True

    from util import PriorityQueue
    aStar_priorityqueue = PriorityQueue()  # fringe
    visited = set()
    aStar_priorityqueue.push((s.getStartState(), [], 0), 0)

    while 1:
        if aStar_priorityqueue.isEmpty():
            break

        current, directions, costs = aStar_priorityqueue.pop()  # add costs for ucs
        # print("Current:", current)
        if current not in visited:
            visited.add(current)
            if s.isGoalState(current):
                s.score += 1
                s.addCube()
                performActions(directions, slow)
                # print("A_Star number of actions:", len(directions))
                actionsList[2].append(len(directions))
                # print("A_Star score:", len(s.body))
                scoreList[2] = len(s.body)
                # scoreList[2] = s.score
            for childNode, direction, cost in s.getSuccessors(current):
                if childNode not in aStar_priorityqueue.heap:
                    if childNode in visited:  # make sure child is not in visited so we don't go backwards
                        continue
                    hCost = costs + cost + manhattanHeuristic(childNode)
                    aStar_priorityqueue.push((childNode, directions + [direction], costs + cost), hCost)


# --------------------------------------------------------------------- End of A Star


# --------------------------------------------------------------------- UCS

# s: snake object
# i : iterator to keep track of where food will be
# slow: True go slow False go fast
def ucs_search(s, i, slow):
    from util import Queue
    global width, rows, snack, tempFood, startState, food

    def performActions(dirs, slow):
        # perform actions in the game window so we can see the results
        for action in dirs:
            if slow:
                pygame.time.delay(50)
                clock.tick(10)
            s.moveAuto(action)
            redrawWindow(win, s)

    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))
    startState = START_POS
    snack = cube(FOOD_POS[i], color=(0, 255, 0))
    tempFood = snack
    clock = pygame.time.Clock()
    flag = True

    from util import PriorityQueue
    ucs_priorityqueue = PriorityQueue()  # fringe
    visited = set()
    ucs_priorityqueue.push((s.getStartState(), [], 0), 0)

    while 1:
        if ucs_priorityqueue.isEmpty():
            break

        current, directions, costs = ucs_priorityqueue.pop()  # add costs for ucs
        # print("Current:", current)
        if current not in visited:
            visited.add(current)
            if s.isGoalState(current):
                s.score += 1
                s.addCube()
                performActions(directions, slow)
                # print("A_Star number of actions:", len(directions))
                actionsList[3].append(len(directions))
                # print("A_Star score:", len(s.body))
                scoreList[3] = len(s.body)
                # scoreList[2] = s.score
            for childNode, direction, cost in s.getSuccessors(current):
                if childNode not in ucs_priorityqueue.heap:
                    if childNode in visited:  # make sure child is not in visited so we don't go backwards
                        continue
                    ucs_priorityqueue.push((childNode, directions + [direction], costs + cost), costs + cost)

# run: run number of the routine
def runSearch(run):
    global actionsList
    actionsList= [[],[],[],[]]

    mySnake = snake((255, 0, 0), START_POS)

    goSlow = False

    # -------------------------------------------------------------- Run Search Algorithms
    mySnake.reset(START_POS)
    print("RUNNING DFS#", run)
    for i in range(0, len(FOOD_POS)):
        dfs_search(mySnake, i, goSlow)
    mySnake.reset(START_POS)
    print("RUNNING BFS#", run)
    for i in range(0, len(FOOD_POS)):
        bfs_search(mySnake, i, goSlow)
    mySnake.reset(START_POS)
    print("RUNNING ASTAR#", run)
    for i in range(0, len(FOOD_POS)):
        aStar_search(mySnake, i, goSlow)
    mySnake.reset(START_POS)
    print("RUNNING UCS#", run)
    for i in range(0, len(FOOD_POS)):
        ucs_search(mySnake, i, goSlow)
    mySnake.reset(START_POS)

    # -------------------------------------------------------------- Calculate new scores
    # print("ACTIONS [ DFS, BFS, ASTAR ]: ")
    # print(actionsList)
    DFS_actions = sum(actionsList[0])
    BFS_actions = sum(actionsList[1])
    AStar_actions = sum(actionsList[2])
    UCS_actions = sum(actionsList[3])
    print("Total DFS actions taken:", DFS_actions)
    print("Total BFS actions taken:", BFS_actions)
    print("Total A_Star actions taken:", AStar_actions)
    print("Total UCS actions taken:", UCS_actions)

    print("RAW SCORES [ DFS, BFS, ASTAR, UCS ]: ")
    print(scoreList)
    calcScores = [0, 0, 0, 0]
    calcScores[0] = (scoreList[0] / DFS_actions) * 100
    calcScores[1] = (scoreList[1] / BFS_actions) * 100
    calcScores[2] = (scoreList[2] / AStar_actions) * 100
    calcScores[3] = (scoreList[3] / UCS_actions) * 100
    print("DFS score:", calcScores[0])
    print("BFS score:", calcScores[1])
    print("A_Star score:", calcScores[2])
    print("UCS score:", calcScores[3])

    allCalcCosts[0].append(calcScores[0])
    allCalcCosts[1].append(calcScores[1])
    allCalcCosts[2].append(calcScores[2])
    allCalcCosts[3].append(calcScores[3])

    # -------------------------------------------------------------- Write to file

    my_file = open(file, "a")
    my_file.write("RUN NUMBER: " + str(run) + " DATE:" + str(datetime.now()) + "\n")
    my_file.write('{0:10}  {1:14}\n'.format("BFS ACTIONS:", BFS_actions))
    my_file.write('{0:10}  {1:14}\n'.format("DFS ACTIONS:", DFS_actions))
    my_file.write('{0:10}  {1:14}\n'.format("ASTAR ACTIONS:", AStar_actions))
    my_file.write('{0:10}  {1:14}\n\n'.format("UCS ACTIONS:", UCS_actions))

    my_file.write('{0:10}  {1:14}\n'.format("RAW BFS SCORE:", scoreList[0]))
    my_file.write('{0:10}  {1:14}\n'.format("RAW DFS SCORE:", scoreList[1]))
    my_file.write('{0:10}  {1:14}\n'.format("RAW ASTAR SCORE:", scoreList[2]))
    my_file.write('{0:10}  {1:14}\n\n'.format("RAW UCS SCORE:", scoreList[3]))

    my_file.write('{0:10}  {1:14}\n'.format("CALC BFS SCORE:", calcScores[0]))
    my_file.write('{0:10}  {1:14}\n'.format("CALC DFS SCORE:", calcScores[1]))
    my_file.write('{0:10}  {1:14}\n'.format("CALC ASTAR SCORE:", calcScores[2]))
    my_file.write('{0:10}  {1:14}\n\n'.format("CALC UCS SCORE:", calcScores[3]))
    my_file.close()

    # -------------------------------------------------------------- Bar Graph for Scores
    data = {"Algorithm": ["DFS", "BFS", "ASTAR", "UCS"],

            "Score": [round(x,2) for x in calcScores]

            }
    # Dictionary loaded into a DataFrame
    dataFrame = pd.DataFrame(data=data)
    # Draw a vertical bar chart
    ax = dataFrame.plot(kind='bar',x="Algorithm", y="Score", rot=70,
                       title="Scores of Snake Game Search Algorithms " + str(datetime.now()))

    for p in ax.patches:
        ax.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))

    plot.show(block=True)

    # -------------------------------------------------------------- Line Graph for Actions
    print(len(actionsList[0]))
    print(len(actionsList[1]))
    print(len(actionsList[2]))
    print(len(actionsList[3]))

    maxLen = max(len(actionsList[0]),len(actionsList[1]),len(actionsList[2]),len(actionsList[3]))
    # Using our actionsList lists we need to assign zeros where there are no slots
    for x in range(0,maxLen):
        if len(actionsList[0]) < maxLen+1:
            actionsList[0].append(0)
        if len(actionsList[1]) < maxLen+1:
            actionsList[1].append(0)
        if len(actionsList[2]) < maxLen+1:
            actionsList[2].append(0)
        if len(actionsList[3]) < maxLen+1:
            actionsList[3].append(0)


    scoreIdx = [x for x in range(0,maxLen+1)]

    # print("DFS",actionsList[0])
    # print("BFS",actionsList[1])
    # print("ASTAR",actionsList[2])
    # print("UCS",actionsList[3])


    # -------------------------------------------------------------- DFS Line Graph for Actions

    data = {"Score": scoreIdx,

            "DFS": actionsList[0]

            }
    # Dictionary loaded into a DataFrame
    dataFrame = pd.DataFrame(data=data)
    # Draw a vertical bar chart
    dataFrame.plot(kind='line',x="Score", y="DFS", rot=70,
                       title="Actions of Snake Game Search Algorithms " + str(run) + " " + str(datetime.now()))

    plot.show(line=True)
    # -------------------------------------------------------------- BFS Line Graph for Actions

    data = {"Score": scoreIdx,

            "BFS": actionsList[1]

            }
    # Dictionary loaded into a DataFrame
    dataFrame = pd.DataFrame(data=data)
    # Draw a vertical bar chart
    dataFrame.plot(kind='line',x="Score", y="BFS", rot=70,
                       title="Actions of Snake Game Search Algorithms " + str(run) + " " + str(datetime.now()))

    plot.show(line=True)

    # -------------------------------------------------------------- ASTAR Line Graph for Actions

    data = {"Score": scoreIdx,

            "ASTAR": actionsList[2]

            }
    # Dictionary loaded into a DataFrame
    dataFrame = pd.DataFrame(data=data)
    # Draw a vertical bar chart
    dataFrame.plot(kind='line',x="Score", y="ASTAR", rot=70,
                       title="Actions of Snake Game Search Algorithms " + str(run) + " " + str(datetime.now()))

    plot.show(line=True)

    # -------------------------------------------------------------- UCS Line Graph for Actions

    data = {"Score": scoreIdx,

            "UCS": actionsList[3]

            }
    # Dictionary loaded into a DataFrame
    dataFrame = pd.DataFrame(data=data)
    # Draw a vertical bar chart
    dataFrame.plot(kind='line',x="Score", y="UCS", rot=70,
                       title="Actions of Snake Game Search Algorithms " + str(run) + " " +str(datetime.now()))

    plot.show(line=True)

# times: number of times we are running searches and data
def runMultiple(times):

    for x in range(0,times):
        foodPos()
        runSearch(x)

    averageCalcCosts[0] = sum(allCalcCosts[0])/times
    averageCalcCosts[1] = sum(allCalcCosts[1])/times
    averageCalcCosts[2] = sum(allCalcCosts[2])/times
    averageCalcCosts[3] = sum(allCalcCosts[3])/times

    # -------------------------------------------------------------- Bar Graph for Average Scores
    data = {"Algorithm": ["DFS", "BFS", "ASTAR", "UCS"],

            "AvgScore": [round(x, 2) for x in averageCalcCosts]

            }
    # Dictionary loaded into a DataFrame
    dataFrame = pd.DataFrame(data=data)
    # Draw a vertical bar chart
    ax = dataFrame.plot(kind='bar', x="Algorithm", y="AvgScore", rot=70,
                            title="Scores of Snake Game Search Algorithms Avg " + str(datetime.now()))

    for p in ax.patches:
        ax.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))

    plot.show(block=True)


def showExample():
    foodPos()
    mySnake = snake((255, 0, 0), START_POS)
    goSlow = True
    for i in range(0, 5):
        bfs_search(mySnake, i, goSlow)
    mySnake.reset(START_POS)
    for i in range(0, 5):
        aStar_search(mySnake, i, goSlow)
    mySnake.reset(START_POS)
    for i in range(0, 5):
        ucs_search(mySnake, i, goSlow)
    mySnake.reset(START_POS)
    for i in range(0, 5):
        dfs_search(mySnake, i, goSlow)
    mySnake.reset(START_POS)


# runMultiple(5)
# main()
showExample()
