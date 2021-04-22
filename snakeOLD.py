
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

    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

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

        # for index, position in enumerate(self.walls):
        #     print("Walls:", position.pos)

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)

    def isGoalState(self, current_pos):
        # todo: Current pos is being looked at after the food has already been eaten, so the food is in a different spot, hence if statement is never true
        # print("current:", current_pos)
        # print("food:", food.pos)
        if current_pos == food.pos:
            print("Goal state!")
            return True
        else:
            return False

    def getSuccessors(self, current_pos):    # more like surrounding grid positions
        """returns a tuple of states, actions, costs"""

        '''Theoretically the max # of successors that can be generated at once should be 3: in front of the head,
        and the two sides of the head (if we have not eaten food yet we can have 4 successors). We will also make it so
        that the snake can not wrap around the screen.'''

        # todo: Currently body right behind the head is being added to successors (I assume other walls will be too).
        successors = []  # tuple of states, actions, cost (grid pos, direction to get there, cost to get there)
        x, y = current_pos
        possible_moves = [-1, 1] # x or y can either stay, increase or decrease position by 1
        # either x or y can move, but not both at a time
        # print("Current pos:", current_pos)
        for movesX in possible_moves:
            nextX = x + movesX   # x will move, y will stay the same
            nextY = y
            if nextX < 0 or nextX > 19: # make sure we don't go out of bounds
                continue
            nextState = nextX, nextY
            print("Current pos2:", current_pos, "next:", nextState)
            for fuck, noU in enumerate(self.walls):
                print("walls:", noU.pos)
            if nextState in self.walls:
                print("FFFFFFFFFFFFFFFFF")
                break
            for index, wallX in enumerate(self.walls):
                # print("wall.pos:", wall.pos)
                # print("next:", nextState)
                if wallX.pos != nextState:   # if nextState we generated is not a wall
                    if nextState != current_pos:
                        if nextState not in successors:
                            successors.append(nextState)

        for moves in possible_moves:
            nextX = x
            nextY = y + moves # y will move, x will stay the same
            if nextY < 0 or nextY > 19: # make sure we don't go out of bounds
                continue
            nextState = nextX, nextY
            if nextState in self.walls:
                print("FFFFFFFFFFFFFFFFF")
                break
            for index, wallY in enumerate(self.walls):
                # print("wally:", wallY.pos)
                # print("next:", nextState)
                if wallY.pos != nextState:   # if nextState we generated is not a wall
                    if nextState != current_pos:
                        if nextState not in successors:
                            successors.append(nextState)

        print("Successors:", successors)
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


def redrawWindow(surface):
    global rows, width, s, snack
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


def getSnack(yumyum):
    pass


# global food
food = []


def main():
    global width, rows, s, snack
    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))
    s = snake((255, 0, 0), (10, 10))
    snack = cube(randomSnack(rows, s), color=(0, 255, 0))
    global food
    food = snack
    flag = True

    clock = pygame.time.Clock()

    while flag:
        # for index, position in enumerate(s.walls):  # we can use this to see current walls (basically our body)
        #     print("Walls:", position.pos)
        pygame.time.delay(50)
        clock.tick(10)
        s.move()
        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = cube(randomSnack(rows, s), color=(0, 255, 0))
            food = snack

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z: z.pos, s.body[x + 1:])):
                # print(\'Score: \', len(s.body))
                # message_box(\'You Lost!\', \'Play again...\')
                s.reset((10, 10))
                break

        redrawWindow(win)

        # test line
        s.getSuccessors(s.head.pos) # the head's position works as our current position
        s.isGoalState(s.head.pos)




main()