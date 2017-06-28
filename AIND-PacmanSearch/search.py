# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
  """
  This class outlines the structure of a search problem, but doesn't implement
  any of the methods (in object-oriented terminology: an abstract class).

  You do not need to change anything in this class, ever.
  """

  def getStartState(self):
     """
     Returns the start state for the search problem
     """
     util.raiseNotDefined()

  def isGoalState(self, state):
     """
       state: Search state

     Returns True if and only if the state is a valid goal state
     """
     util.raiseNotDefined()

  def getSuccessors(self, state):
     """
       state: Search state

     For a given state, this should return a list of triples,
     (successor, action, stepCost), where 'successor' is a
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental
     cost of expanding to that successor
     """
     util.raiseNotDefined()

  def getCostOfActions(self, actions):
     """
      actions: A list of actions to take

     This method returns the total cost of a particular sequence of actions.  The sequence must
     be composed of legal moves
     """
     util.raiseNotDefined()


def tinyMazeSearch(problem):
  """
  Returns a sequence of moves that solves tinyMaze.  For any other
  maze, the sequence of moves will be incorrect, so only use this for tinyMaze
  """
  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
  """
  Search the deepest nodes in the search tree first
  [2nd Edition: p 75, 3rd Edition: p 87]

  Your search algorithm needs to return a list of actions that reaches
  the goal.  Make sure to implement a graph search algorithm
  [2nd Edition: Fig. 3.18, 3rd Edition: Fig 3.7].

  To get started, you might want to try some of these simple commands to
  understand the search problem that is being passed in:

  print "Start:", problem.getStartState()
  print "Is the start a goal?", problem.isGoalState(problem.getStartState())
  print "Start's successors:", problem.getSuccessors(problem.getStartState())
  """

  # Use stack (LIFO) to keep track of nodes to search
  searchNodes = util.Stack()
  start = problem.getStartState()
  visited = set()
  predecessors = {}

  # Push initial state to stack and keep track of visited
  searchNodes.push((start, visited))

  # Search successors
  while not searchNodes.isEmpty():
      (s, v) = searchNodes.pop()

      # If this is goal state
      if problem.isGoalState(s):
          return buildPathFromPredecessors(predecessors, start, s)

      # Set this node as visited
      if s not in v:
          v.add(s)

          # Push unvisited successors to stack
          for state, action, cost in problem.getSuccessors(s):
              if state not in v:
                  predecessors[state] = (s, action)
                  searchNodes.push((state, v))

  return False

def buildPathFromPredecessors(predecessors, start, goal):
  """
  Builds an array of actions given a predecessors dict, start state, and goal
  state
  """
  path = []
  state = goal

  # Start from the goal and build path backwards
  while state != start:
      (prevState, action) = predecessors[state]
      path.append(action)
      state = prevState

  # Return reverse
  return path[::-1]

def breadthFirstSearch(problem):
  """
  Search the shallowest nodes in the search tree first.
  [2nd Edition: p 73, 3rd Edition: p 82]
  """

  # Use queue (FIFO) to keep track of nodes to search
  searchNodes = util.Queue()
  start = problem.getStartState()
  visited = set()
  predecessors = {}

  # Push initial state to queue and keep track of visited
  searchNodes.push((start, visited))

  # Search successors
  while not searchNodes.isEmpty():
      (s, v) = searchNodes.pop()

      # If this is goal state
      if problem.isGoalState(s):
          return buildPathFromPredecessors(predecessors, start, s)

      # Set this node as visited
      if s not in v:
          v.add(s)

          # Push unvisited successors to queue
          for state, action, cost in problem.getSuccessors(s):
              if state not in v:
                  predecessors[state] = (s, action)
                  searchNodes.push((state, v))

  return False

def uniformCostSearch(problem):
  "Search the node of least total cost first. "

  # Use Priority Queue using cost to keep track of nodes to search
  searchNodes = util.PriorityQueue()
  start = problem.getStartState()
  visited = set()
  predecessors = {}

  # Push initial state to PQ and keep track of visited
  searchNodes.push((start, visited, 0), 0)

  # Search successors
  while not searchNodes.isEmpty():
      # Pop a node from PQ and get state, visited, cost
      (s, v, c) = searchNodes.pop()

      # If this is goal state
      if problem.isGoalState(s):
          return buildPathFromPredecessors(predecessors, start, s)

      # Set this node as visited
      if s not in v:
          v.add(s)

          # Push unvisited successors to queue
          for state, action, cost in problem.getSuccessors(s):
              if state not in v:
                  predecessors[state] = (s, action)
                  searchNodes.push((state, v, c + cost), c + cost)

  return False

def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."

  # Similar to uniformCostSearch except we combine cost and heuristic
  # Use Priority Queue using cost to keep track of nodes to search
  searchNodes = util.PriorityQueue()
  start = problem.getStartState()
  visited = set()
  predecessors = {}

  # Push initial state to PQ and keep track of visited
  priority = 0 + heuristic(start, problem)
  searchNodes.push((start, visited, 0), priority)

  # Search successors
  while not searchNodes.isEmpty():
      # Pop a node from PQ and get state, visited, cost
      (s, v, c) = searchNodes.pop()

      # If this is goal state
      if problem.isGoalState(s):
          return buildPathFromPredecessors(predecessors, start, s)

      # Set this node as visited
      if s not in v:
          v.add(s)

          # Push unvisited successors to queue
          for state, action, cost in problem.getSuccessors(s):
              if state not in v:
                  predecessors[state] = (s, action)
                  priority = c + cost + heuristic(state, problem)
                  searchNodes.push((state, v, c + cost), priority)

  return False

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
