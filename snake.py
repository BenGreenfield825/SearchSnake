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
            print("Goal state!")
            return True
        else:
            return False

    def getStartState(self):
        # return startState
        # i am such a huge idiot and i hate myself
        return self.head.pos

    def getSuccessors(self, current_pos):  # more like surrounding grid positions
        """returns a tuple of states, actions, costs"""

        '''Theoretically the max # of successors that can be generated at once should be 3: in front of the head,
        and the two sides of the head (if we have not eaten food yet we can have 4 successors). We will also make it so
        that the snake can not wrap around the screen.'''

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
                        elif movesX == -1:
                            directionX = "LEFT"
                        successors.append((nextState, directionX, 0))

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
                        elif moves == -1:
                            directionY = "UP"
                        successors.append((nextState, directionY, 0))

        # todo: toggle to see successors
        # print("Successors:", successors)
        return successors


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
food = []
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

actionsList = [0, 0, 0]


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
FOOD_POS = [(10, 0), (0, 10), (10, 0), (0, 10), (10, 0)]
# FOOD_POS = [(10, 0), (0, 10), (10, 10), (12, 10), (5, 5)] # did this for some other test values


# --------------------------------------------------------------------- DFS


def dfs_search(s, i):
    from util import Stack
    global width, rows, snack, tempFood, startState, food

    def performActions(dirs):
        for action in dirs:
            pygame.time.delay(50)
            clock.tick(10)
            s.moveAuto(action)
            redrawWindow(win, s)

    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))
    """food position can be hard coded to test results/performance"""
    startState = START_POS
    # s = snake((255, 0, 0), startState)
    # s.reset(startState)
    snack = cube(FOOD_POS[i], color=(0, 255, 0))
    # snack = cube((12, 10), color=(0, 255, 0))
    food = snack
    tempFood = snack
    print("food pos:", tempFood.pos)
    clock = pygame.time.Clock()
    flag = True

    dfs_stack = Stack()  # fringe
    visited = set()
    dfs_stack.push((s.getStartState(), []))

    while 1:
        if dfs_stack.isEmpty():
            print("Failure")
            s.addCube()
            break
        current, directions = dfs_stack.pop()
        print("Current pos:", current)
        if current not in visited:
            visited.add(current)
            if s.isGoalState(current):
                performActions(directions)
                print("Number of actions:", len(directions))
                print("Score:", len(s.body))
                # message_box("Goal", ("Number of actions:", len(directions), "Score:", len(s.body)))
                break
                # s.addCube()
                # snack = cube(randomSnack(rows, s), color=(0, 255, 0))
                # tempFood = food  # use this as testing to try to get food value before it changes
                # food = snack  # update food to new value
                # print("next food:", tempFood.pos)
                # continue
            for childNode, direction, cost in s.getSuccessors(current):
                # print("childNode:", childNode, "direction:", direction)
                if childNode not in dfs_stack.list:
                    if childNode in visited:
                        continue
                    dfs_stack.push((childNode, directions + [direction]))

    actionsList[0] = len(directions)


# --------------------------------------------------------------------- End DFS


def bfs_searchTEST():
    from util import Queue
    global width, rows, snack, tempFood, startState, food

    def performActions(dirs, sObj):
        # pass
        for action in dirs:
            # print(action)
            # print(sObj.head.pos)
            pygame.time.delay(50)
            clock.tick(10)
            sObj.moveAuto(action)
            for x in range(len(sObj.body)):
                if sObj.body[x].pos in list(map(lambda z: z.pos, sObj.body[x + 1:])):
                    print('Score:', len(sObj.body))
                    # message_box('You Lost!\''', \'Play again...\'')
                    message_box("u die'd", "dead")
                    sObj.reset((10, 10))
                    break
            redrawWindow(win, sObj)

    def search(sObj):
        global snack, food, tempFood
        bfs_queue = Queue()  # fringe
        visited = set()
        snack = cube(randomSnack(rows, sObj), color=(0, 255, 0))
        food = snack
        tempFood = snack
        print("food pos:", food.pos)
        bfs_queue.push((sObj.getStartState(), []))
        while 1:
            if bfs_queue.isEmpty():
                print("Failure")
                break
            current, directions = bfs_queue.pop()
            # print("Current pos:", current)
            if current not in visited:
                visited.add(current)
                if sObj.isGoalState(current):
                    # todo: food pos and current pos line up - so it might be an error with drawing on the screen
                    print(directions)
                    performActions(directions, sObj)
                    print("Number of actions:", len(directions))
                    print('Score:', len(sObj.body))
                    # message_box("Goal", ("Number of actions:", len(directions)))
                    sObj.addCube()
                    search(sObj)
                    # bfs_searchTEST(sObj)
                for childNode, direction, cost in sObj.getSuccessors(current):
                    if childNode not in bfs_queue.list:
                        if childNode in visited:
                            continue
                        bfs_queue.push((childNode, directions + [direction]))

    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))
    """food position can be hard coded to test results/performance"""
    startState = (10, 10)
    ns = snake((255, 0, 0), startState)
    ns.reset(startState)
    # snack = cube(randomSnack(rows, s), color=(0, 255, 0))
    # snack = cube((12, 10), color=(0, 255, 0))

    # print("food pos:", tempFood.pos)
    clock = pygame.time.Clock()
    flag = True

    search(ns)

    # actionsList[1] = len(directions)


# --------------------------------------------------------------------- BFS

def bfs_search(s, i):
    from util import Queue
    global width, rows, snack, tempFood, startState, food

    def performActions(dirs):
        for action in dirs:
            pygame.time.delay(50)
            clock.tick(10)
            s.moveAuto(action)
            redrawWindow(win, s)

    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))
    """food position can be hard coded to test results/performance"""
    startState = START_POS
    # s = snake((255, 0, 0), startState)
    # s.reset(startState)
    # snack = cube(FOOD_POS, color=(0, 255, 0))
    # snack = cube((12, 10), color=(0, 255, 0))
    snack = cube(FOOD_POS[i], color=(0, 255, 0))
    food = snack
    tempFood = snack
    print("food pos:", tempFood.pos)
    clock = pygame.time.Clock()
    flag = True

    bfs_queue = Queue()  # fringe
    visited = set()
    bfs_queue.push((s.getStartState(), []))

    while 1:
        if bfs_queue.isEmpty():
            print("Failure")
            s.addCube()
            break
        current, directions = bfs_queue.pop()
        print("Current pos:", current)
        if current not in visited:
            visited.add(current)
            if s.isGoalState(current):
                performActions(directions)
                print("Number of actions:", len(directions))
                print("Score:", len(s.body))
                # message_box("Goal", ("Number of actions:", len(directions), "Score:", len(s.body)))
                # break
                # s.addCube()
                # snack = cube(randomSnack(rows, s), color=(0, 255, 0))
                # tempFood = food  # use this as testing to try to get food value before it changes
                # food = snack  # update food to new value
                # print("next food:", tempFood.pos)
                # continue
            for childNode, direction, cost in s.getSuccessors(current):
                # print("childNode:", childNode, "direction:", direction)
                if childNode not in bfs_queue.list:
                    if childNode in visited:
                        continue
                    bfs_queue.push((childNode, directions + [direction]))

    actionsList[1] = len(directions)


# --------------------------------------------------------------------- DFS


# --------------------------------------------------------------------- A Star


def aStar_search(s, i):
    from util import Queue
    global width, rows, snack, tempFood, startState, food

    def nullHeuristic(state, problem=None):
        # trivial heuristic
        return 0

    def manhattanHeuristic(position):
        # uses distance as a score for heuristic
        xy1 = position
        # xy2 = problem.goal
        xy2 = food.pos
        return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])

    def performActions(dirs):
        # perform actions in the game window so we can see the results
        print(dirs)
        for action in dirs:
            pygame.time.delay(50)
            clock.tick(10)
            s.moveAuto(action)
            # print(action)
            print("current pos (perform actions):", s.head.pos)
            # print("food pos:", food.pos)
            redrawWindow(win, s)

    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))
    """food position can be hard coded to test results/performance"""
    startState = START_POS

    snack = cube(FOOD_POS[i], color=(0, 255, 0))
    # snack = cube((12, 10), color=(0, 255, 0))
    food = snack
    tempFood = snack
    print("food pos:", tempFood.pos)
    clock = pygame.time.Clock()
    flag = True

    from util import PriorityQueue  # A* also uses a priority queue to decide which nodes to go to based on heuristic
    aStar_priorityqueue = PriorityQueue()  # fringe
    visited = set()
    aStar_priorityqueue.push((s.getStartState(), [], 0), 0)

    while 1:
        if aStar_priorityqueue.isEmpty():
            # aStar_priorityqueue.push((s.getStartState(), [], 0), 0)
            s.addCube()
            # snack = cube(FOOD_POS[i], color=(0, 255, 0))

            break

        current, directions, costs = aStar_priorityqueue.pop()  # add costs for ucs
        # print("Current:", current)
        if current not in visited:
            visited.add(current)
            if s.isGoalState(current):
                performActions(directions)
                print("Number of actions:", len(directions))
                print("Score:", len(s.body))
                # message_box("Goal", ("Number of actions:", len(directions), "Score:", len(s.body)))

            for childNode, direction, cost in s.getSuccessors(current):
                if childNode not in aStar_priorityqueue.heap:
                    if childNode in visited:  # make sure child is not in visited so we don't go backwards
                        continue
                    '''instead of just doing costs + cost, we also add in heuristic() so we can see the cost
                    of the edges as well as the heuristic cost.'''
                    # hCost = costs + cost + nullHeuristic(childNode, s)
                    print("direction:", direction)
                    # print("childNode:", childNode)
                    print("current:", current)
                    hCost = costs + cost + manhattanHeuristic(childNode)
                    aStar_priorityqueue.push((childNode, directions + [direction], costs + cost), hCost)

    actionsList[2] = len(directions)


# --------------------------------------------------------------------- End of A Star


def runSearch():
    mySnake = snake((255, 0, 0), START_POS)
    # message_box("aStar", "Starting aStar Search...")
    for i in range(0, 5):
        aStar_search(mySnake, i)
    mySnake.reset(START_POS)
    for i in range(0, 5):
        bfs_search(mySnake, i)
    mySnake.reset(START_POS)
    for i in range(0, 5):
        dfs_search(mySnake, i)
    mySnake.reset(START_POS)


runSearch()

