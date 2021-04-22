
# CSCI 4478 - Dr Vahid Behzadan
# Name: searchAgents.py
# Description: Agents to test and figure out a snake's search AI
# Code design mirrors that of Pacman code in http://ai.berkeley.edu
# Revision: 4/22/2021

from game import Directions
from game import Agent
from game import Actions
import util
import time
import search

import math

# 3. todo: go west needs to work with snake
class GoWestAgent(Agent):
    "An agent that goes West until it can't."

    def getAction(self, state):
        "The agent receives a GameState (defined in pacman.py)."
        # 2. todo: look into STATE and getLegalSnakeActions
        if Directions.WEST in state.getLegalPacmanActions():
            return Directions.WEST
        else:
            return Directions.STOP