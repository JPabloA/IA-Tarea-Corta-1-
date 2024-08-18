import time

"""
Author : Akshay Rajput
© Anyone must take permission form me and mention my social handles in 
the references/attributes before using this code in their work or project.
Linkedin: https://www.linkedin.com/in/akshay-189a48200/
Twitter: https://twitter.com/notifications
Medium: https://medium.com/@warriorak77
GitHub: https://github.com/webintellectual
Website: https://akshaysworklife.bio.link/
"""

class Node:
    def __init__(self,st=[[2,2,1,1,1,2,2],[2,2,1,1,1,2,2],[1,1,1,1,1,1,1],[1,1,1,0,1,1,1],[1,1,1,1,1,1,1],[2,2,1,1,1,2,2],[2,2,1,1,1,2,2]],prt=None,pCost=0):
        self.state = st
        self.parent = prt
        self.action = None
        self.pathCost = pCost # g

        self.h = 88 # I already calculated MD for initial state
        self.f = self.pathCost + self.h

    def __lt__(self, other):
        return self.f < other.f # min heap

goal = [[2,2,0,0,0,2,2],[2,2,0,0,0,2,2],[0,0,0,0,0,0,0],[0,0,0,1,0,0,0],[0,0,0,0,0,0,0],[2,2,0,0,0,2,2],[2,2,0,0,0,2,2]]
def goalTest(state):
    """ 
    Check if the state is goal state or not
    Args:
        state (matrix): Current state of the board
    Returns:
        bool: True if state is goal state else False
    """
    return state==goal

def MD(i,j):
    """Manhattan Distance
    Args:
        i (int): row
        j (int): column
    Returns:
        int: Manhatan distance of i,j from 3,3
    """
    return abs(3-i)+abs(3-j)

Total_nodes_expanded = 0
def getSuccessors(node):
    ans = []

    # Good order of directions # NSEW
    dx1 = [0,0,1,-1] # x1 is the peg to be jumped
    dy1 = [-1,1,0,0] # y1 is the peg to be jumped
    
    dx2 = [0,0,2,-2] # x2 is the empty cell where x1 will jump
    dy2 = [-2,2,0,0] # y2 is the empty cell where y1 will jump
    
    for i in range(7): #For each row of the board
        for j in range(7): #For each column of the board
            if node.state[i][j]==1: #If there is a peg at i,j
                for k in range(4): #For each direction
                    #c1i,c1j are the coordinates of the peg to be jumped
                    c1i = i+dy1[k]
                    c1j = j+dx1[k]
                    #c2i,c2j are the coordinates of the empty cell where the peg will jump
                    c2i = i+dy2[k]
                    c2j = j+dx2[k]

                    if(c2i<0 or c2i>=7 or c2j<0 or c2j>=7): #Out of bounds
                        continue
                    if(node.state[c1i][c1j]==0):#No peg to jump
                        continue
                    if(node.state[c2i][c2j]==0):#Empty cell is not empty
                        stateCpy = [obj.copy() for obj in node.state]#Deep copy of the state
                        child = Node(stateCpy,node,node.pathCost+1)
                        child.state[c2i][c2j]=1 #Jump the peg
                        child.state[c1i][c1j]=0 #Remove the jumped peg 
                        child.state[i][j]=0 #Remove the peg (the peg that jumped)
                        child.action = [[i,j],[c2i,c2j]]#Action taken to reach this state

                        chr = node.h
                        chr -= MD(i,j) #Remove the MD of the peg that jumped
                        chr -= MD(c1i,c1j) #Remove the MD of the jumped peg
                        chr += MD(c2i,c2j) #Add the MD of the empty cell where the peg jumped
                        child.h = chr
                        child.f = child.pathCost + child.h

                        ans.append(child)
                        global Total_nodes_expanded
                        Total_nodes_expanded +=1
    return ans


def displayBoard(state):
    """ Display the board

    Args:
        state (matrix): Current state of the board
    """
    for row in state:
        print(row)

def aStar():
    """ 
    A* search algorithm to solve the peg solitaire problem
    
    Returns:
        matrix: Final state of the board
    """
    start_node = Node() # initial state
    frontier = [] # keep nodes # we can use list directly as a heap in python. append() and pop() for push and pop
    explored = [] # keep states which are explored

    frontier.append(start_node)
    while True:
        if len(frontier)==0:
            return None
        curr = frontier.pop()

        displayBoard(curr.state)
        print("Path cost: ", curr.pathCost)
        print()

        if curr.state in explored:
            continue
        if goalTest(curr.state) == True:
            print("Search ended")
            print("Total nodes explored: ", len(explored)) 
            return curr
        children = getSuccessors(curr)
        for child in children:
            if (child.state in explored) == False:
                frontier.append(child)
        explored.append(curr.state)

def allActions(goalNode):
    ans = []
    while goalNode.parent != None:
        ans.append(goalNode.action)
        goalNode = goalNode.parent
    ans.reverse()
    return ans

print("Search started")
start_time = time.time()
ans = aStar()
end_time = time.time()
elapsed_time = end_time - start_time
print("Total nodes expanded: ",Total_nodes_expanded)
print("Time taken: ",elapsed_time)
print()
displayBoard(ans.state)

# print()
# print("Moves: ")
# moves = allActions(ans)
# for move in moves:
#     print(move)
