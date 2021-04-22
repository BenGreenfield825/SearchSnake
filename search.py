
# CSCI 4478 - Dr Vahid Behzadan
# Name: search.py
# Description: Definition of a SearchProblem and implementation of searching algorithms
# Code design mirrors that of Pacman code in http://ai.berkeley.edu
# Revision: 4/22/2021

import util

class SearchProblem:

    def getStartState(self):
        return 0
    def isGoalState(self,state):
        return 0
    def getSuccessors(self, state):
        return 0
    def getCostOfActions(self,actions):
        return 0

# 4. todo: do any type of search on a snake map with constant given directions
def tinyMazeSearch(problem):
    """
    Objective: Instructs the snake to move in a sequence of directions
    Note: It has the snake move as defined in this function with no changes
    """

    # Top level of program, we want snake to move south six times
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s,s,s,s,s,s]

# -------------------------------------- Gonna need to change things sorry buddy
# def main():
#     # main can call the different search functions (ideally we should set up command line args but idk how to do that so)
#     # depthFirstSearch()
#     return
#
#
# def depthFirstSearch():
#     print("Starting depth first search algorithm...")
#     return
#
#
# def breadthFirstSearch():
#     print("Starting breadth first search algorithm...")
#     return
#
#
# # ideally the only line of code outside of a function should just be a call to main so we can focus on just the functions
# main()