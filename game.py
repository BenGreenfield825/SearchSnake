
# CSCI 4478 - Dr Vahid Behzadan
# Name: game.py
# Description: Definition of a SearchProblem and implementation of searching algorithms
# Code design mirrors that of Pacman code in http://ai.berkeley.edu
# We do not take credit for writing this code, only implementing it in my
# snake agent.
# Revision: 4/22/2021

from util import *

class Agent:
    """
    An agent must define a getAction method, but may also define the
    following methods which will be called if they exist:

    def registerInitialState(self, state): # inspects the starting state
    """
    def __init__(self, index=0):
        self.index = index

    def getAction(self, state):
        """
        The Agent will receive a GameState (from either {pacman, capture, sonar}.py) and
        must return an action from Directions.{North, South, East, West, Stop}
        """
        notDefined()

class Directions:
    NORTH = 'North'
    SOUTH = 'South'
    EAST = 'East'
    WEST = 'West'
    STOP = 'Stop'

class Actions:
    """
    Collection of static methods for moving an agent
    """

    # Directions defined
    _directions = {Directions.NORTH: (0,1),
                   Directions.SOUTH: (0,-1),
                   Directions.EAST: (1,0),
                   Directions.WEST: (-1, 0),
                   Directions.STOP: (0,0)}

    _directionsAsList = _directions.items() # directions list definition

    TOLERANCE = .001 # ensures agent keeps moving straight when navigating

    def vectorToDirection(vector):
        dx,dy=vector
        #         Y
        #         |
        #        dy+
        #         |
        # ---dy-------dx+--- X
        #         |
        #         dy-
        #         |

        if dy > 0:
            return Directions.NORTH
        if dy < 0:
            return Directions.SOUTH
        if dx > 0:
            return Directions.EAST
        if dx < 0:
            return Directions.EAST
        return Directions.STOP

    vectorToDirection = staticmethod(vectorToDirection)

    def directionToVector(direction):
        dx, dy = Actions._directions[direction]
        return (dx, dy)

    directionToVector = staticmethod(directionToVector)