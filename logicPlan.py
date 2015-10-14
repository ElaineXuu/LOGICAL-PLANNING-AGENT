# logicPlan.py
# ------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In logicPlan.py, you will implement logic planning methods which are called by
Pacman agents (in logicAgents.py).
"""

import util
import sys
import logic
import game


pacman_str = 'P'
ghost_pos_str = 'G'
ghost_east_str = 'GE'
pacman_alive_str = 'PA'

class PlanningProblem:
    """
    This class outlines the structure of a planning problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the planning problem.
        """
        util.raiseNotDefined()

    def getGhostStartStates(self):
        """
        Returns a list containing the start state for each ghost.
        Only used in problems that use ghosts (FoodGhostPlanningProblem)
        """
        util.raiseNotDefined()
        
    def getGoalState(self):
        """
        Returns goal state for problem. Note only defined for problems that have
        a unique goal state such as PositionPlanningProblem
        """
        util.raiseNotDefined()

def tinyMazePlan(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def sentence1():
    """Returns a logic.Expr instance that encodes that the following expressions are all true.
    
    A or B
    (not A) if and only if ((not B) or C)
    (not A) or (not B) or C
    """
    A = logic.Expr('A')
    B = logic.Expr('B')
    C = logic.Expr('C')
    aaa = logic.disjoin(A,B)
    a_or_b = ~A % (~B | C)
    not_a = logic.disjoin(~A,~B,C)
    return logic.conjoin(aaa,a_or_b,not_a)




def sentence2():
    """Returns a logic.Expr instance that encodes that the following expressions are all true.
    
    C if and only if (B or D)
    A implies ((not B) and (not D))
    (not (B and (not C))) implies A
    (not D) implies C
    """
    A = logic.Expr('A')
    B = logic.Expr('B')
    C = logic.Expr('C')
    D = logic.Expr('D')
    aaa = C % (B | D)
    a_or_b = A >> (~B & ~D)
    not_a = ~(B & ~C) >> A
    not_d = ~D >> C
    return logic.conjoin(aaa,a_or_b,not_a,not_d)


def sentence3():
    """Using the symbols WumpusAlive[1], WumpusAlive[0], WumpusBorn[0], and WumpusKilled[0],
    created using the logic.PropSymbolExpr constructor, return a logic.PropSymbolExpr
    instance that encodes the following English sentences (in this order):

    The Wumpus is alive at time 1 if and only if the Wumpus was alive at time 0 and it was
    not killed at time 0 or it was not alive and time 0 and it was born at time 0.

    The Wumpus cannot both be alive at time 0 and be born at time 0.

    The Wumpus is born at time 0.
    """
    a = logic.PropSymbolExpr("WumpusAlive[1]")
    b = logic.PropSymbolExpr("WumpusAlive[0]")
    c = logic.PropSymbolExpr("WumpusBorn[0]")
    d = logic.PropSymbolExpr("WumpusKilled[0]")
    alive = a % ((b & ~d) | (~b & c))
    cant = ~(b & c)
    born = c
    return logic.conjoin(alive,cant,born) 



def findModel(sentence):
    """Given a propositional logic sentence (i.e. a logic.Expr instance), returns a satisfying
    model if one exists. Otherwise, returns False.
    """
    a = logic.to_cnf(sentence)
    b = logic.pycoSAT(a)
    return b

def atLeastOne(literals) :
    """
    Given a list of logic.Expr literals (i.e. in the form A or ~A), return a single 
    logic.Expr instance in CNF (conjunctive normal form) that represents the logic 
    that at least one of the literals in the list is true.
    >>> A = logic.PropSymbolExpr('A');
    >>> B = logic.PropSymbolExpr('B');
    >>> symbols = [A, B]
    >>> atleast1 = atLeastOne(symbols)
    >>> model1 = {A:False, B:False}
    >>> print logic.pl_true(atleast1,model1)
    False
    >>> model2 = {A:False, B:True}
    >>> print logic.pl_true(atleast1,model2)
    True
    >>> model3 = {A:True, B:True}
    >>> print logic.pl_true(atleast1,model2)
    True
    """
    return logic.disjoin(literals)


def atMostOne(literals) :
    """
    Given a list of logic.Expr literals, return a single logic.Expr instance in 
    CNF (conjunctive normal form) that represents the logic that at most one of 
    the expressions in the list is true.
    """
    conjunctions = []
    for literal in literals:
        not_literal = ~literal

        # Disjoin literal with NOT(literal) for every other element besides this literal
        # and add it to the list to be conjoined
        for inner_literal in literals:
            if literal != inner_literal:
                not_inner_literal = ~inner_literal
                disjunction = logic.disjoin(not_literal, not_inner_literal)
                conjunctions.append(disjunction)

    return logic.conjoin(conjunctions)


def exactlyOne(literals) :
    """
    Given a list of logic.Expr literals, return a single logic.Expr instance in 
    CNF (conjunctive normal form)that represents the logic that exactly one of 
    the expressions in the list is true.
    """
    conjunctions = []
    one_must_be_true_list = []
    for literal in literals:
        not_literal = ~literal
        one_must_be_true_list.append(literal)

        # Disjoin literal with NOT(literal) for every other element besides this literal
        # and add it to the list to be conjoined
        for inner_literal in literals:
            if literal != inner_literal:
                not_inner_literal = ~inner_literal
                disjunction = logic.disjoin(not_literal, not_inner_literal)
                conjunctions.append(disjunction)

    # Add the expression that states at least one of the literals must be true
    one_must_be_true = logic.disjoin(one_must_be_true_list)
    conjunctions.append(one_must_be_true)

    return logic.conjoin(conjunctions)


def extractActionSequence(model, actions):
    """
    Convert a model in to an ordered list of actions.
    model: Propositional logic model stored as a dictionary with keys being
    the symbol strings and values being Boolean: True or False
    Example:
    >>> model = {"North[3]":True, "P[3,4,1]":True, "P[3,3,1]":False, "West[1]":True, "GhostScary":True, "West[3]":False, "South[2]":True, "East[1]":False}
    >>> actions = ['North', 'South', 'East', 'West']
    >>> plan = extractActionSequence(model, actions)
    >>> print plan
    ['West', 'South', 'North']
    """
    models = []
    final = []
    for i in model.keys():
        if model[i]:
            a = logic.PropSymbolExpr.parseExpr(i)
            if a[0] in actions:
                models.append(a)
    p = sorted(models, key=lambda mod: int(mod[1]))
    for m in p:
        final.append(m[0])
    return final

def pacmanSuccessorStateAxioms(x, y, t, walls_grid):
    """
    Successor state axiom for state (x,y,t) (from t-1), given the board (as a 
    grid representing the wall locations).
    Current <==> (previous position at time t-1) & (took action to move to x, y)
    """
    current = logic.PropSymbolExpr(pacman_str, x, y, t)

    neighbors = []

    if walls_grid[x-1][y] == False:
        prev_position = logic.PropSymbolExpr(pacman_str, x-1, y, t-1)
        action = logic.PropSymbolExpr('East', t-1)
        state = logic.conjoin(prev_position, action)
        neighbors.append(state)

    if walls_grid[x+1][y] == False:
        prev_position = logic.PropSymbolExpr(pacman_str, x+1, y, t-1)
        action = logic.PropSymbolExpr('West', t-1)
        state = logic.conjoin(prev_position, action)
        neighbors.append(state)

    if walls_grid[x][y-1] == False:
        prev_position = logic.PropSymbolExpr(pacman_str, x, y-1, t-1)
        action = logic.PropSymbolExpr('North', t-1)
        state = logic.conjoin(prev_position, action)
        neighbors.append(state)

    if walls_grid[x][y+1] == False:
        prev_position = logic.PropSymbolExpr(pacman_str, x, y+1, t-1)
        action = logic.PropSymbolExpr('South', t-1)
        state = logic.conjoin(prev_position, action)
        neighbors.append(state)

    prev_states = atLeastOne(neighbors)
    final_axiom = current % prev_states
    return final_axiom 


def positionLogicPlan(problem):
    manhattanDistance = util.manhattanDistance(problem.getStartState(), problem.getGoalState())
    for time in range(manhattanDistance, 3000):
        exprs = []

        start=problem.getStartState()
        goal=problem.getGoalState()
        exprs.append(logic.PropSymbolExpr("P",start[0],start[1],0))
        exprs.append(logic.PropSymbolExpr("P",goal[0],goal[1],time))

        positions = []
        for x in range(1,problem.getWidth()+1):
            for y in range(1,problem.getHeight()+1):
                if not problem.isWall((x,y)) and (x,y)!=problem.getStartState():
                    positionSymbol = logic.Expr('~',logic.PropSymbolExpr("P",x,y,0))
                    exprs.append(positionSymbol)

        for t in range(0,time):
            northSymbol = logic.PropSymbolExpr("North", t)
            southSymbol = logic.PropSymbolExpr("South", t)
            westSymbol = logic.PropSymbolExpr("West", t)
            eastSymbol = logic.PropSymbolExpr("East", t)
            exactlyOneAction = exactlyOne([northSymbol, southSymbol, westSymbol, eastSymbol])
            appendToExprs(exprs, exactlyOneAction)

        for t in range(1, time+1):
            for x in range(1,problem.getWidth()+1):
                for y in range(1,problem.getHeight()+1):
                    if not problem.isWall((x,y)):
                        actions = problem.actions((x,y))
                        prevExprs = []
                        for action in actions:
                            currentStatePropSymbolExpr = logic.PropSymbolExpr("P", x, y, t)
                            prevState = ()
                            if action == 'North':
                                action = 'South'
                                prevState = (x,y+1)
                            elif action == 'South':
                                action = 'North'
                                prevState = (x,y-1)
                            elif action == 'West':
                                action = 'East'
                                prevState = (x-1,y)
                            elif action == 'East':
                                action = 'West'
                                prevState = (x+1,y)
                            actionPropSymbolExpr = logic.PropSymbolExpr(action, t-1)
                            prevStatePropSymbolExpr = logic.PropSymbolExpr("P", prevState[0], prevState[1], t-1)
                            prevExprs.append(logic.Expr("&", actionPropSymbolExpr, prevStatePropSymbolExpr))
                        prevExprsOrred = logic.Expr("|", *prevExprs)
                        iff = logic.Expr("<=>", prevExprsOrred, currentStatePropSymbolExpr)
                        appendToExprs(exprs, iff)
        result = logic.pycoSAT(exprs)
        if result:
            return true


def foodLogicPlan(problem):
    """
    Given an instance of a FoodPlanningProblem, return a list of actions that help Pacman
    eat all of the food.
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    walls = problem.walls
    width, height = problem.getWidth(), problem.getHeight()

    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def ghostPositionSuccessorStateAxioms(x, y, t, ghost_num, walls_grid):
    """
    Successor state axiom for patrolling ghost state (x,y,t) (from t-1).
    Current <==> (causes to stay) | (causes of current)
    GE is going east, ~GE is going west 
    """
    pos_str = ghost_pos_str+str(ghost_num)
    east_str = ghost_east_str+str(ghost_num)

    "*** YOUR CODE HERE ***"
    return logic.Expr('A') # Replace this with your expression

def ghostDirectionSuccessorStateAxioms(t, ghost_num, blocked_west_positions, blocked_east_positions):
    """
    Successor state axiom for patrolling ghost direction state (t) (from t-1).
    west or east walls.
    Current <==> (causes to stay) | (causes of current)
    """
    pos_str = ghost_pos_str+str(ghost_num)
    east_str = ghost_east_str+str(ghost_num)

    "*** YOUR CODE HERE ***"
    return logic.Expr('A') # Replace this with your expression


def pacmanAliveSuccessorStateAxioms(x, y, t, num_ghosts):
    """
    Successor state axiom for patrolling ghost state (x,y,t) (from t-1).
    Current <==> (causes to stay) | (causes of current)
    """
    ghost_strs = [ghost_pos_str+str(ghost_num) for ghost_num in xrange(num_ghosts)]

    "*** YOUR CODE HERE ***"
    return logic.Expr('A') # Replace this with your expression

def foodGhostLogicPlan(problem):
    """
    Given an instance of a FoodGhostPlanningProblem, return a list of actions that help Pacman
    eat all of the food and avoid patrolling ghosts.
    Ghosts only move east and west. They always start by moving East, unless they start next to
    and eastern wall. 
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    walls = problem.walls
    width, height = problem.getWidth(), problem.getHeight()

    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviations
plp = positionLogicPlan
flp = foodLogicPlan
fglp = foodGhostLogicPlan

# Some for the logic module uses pretty deep recursion on long expressions
sys.setrecursionlimit(100000)
    