
import numpy as np
import time
import sys


"""
finds routes and their cost between "src", and "dst" with recursion

"""
def findRoutesAndCosts(src, dst):
    
    # stores visited nodes to control a node visited or not
    # in the begining all of them are not visited
    visited = {}
    for i in nodes:
        visited[i] = False
    
    path = [] # stores any path between "src" and "dst"
    routes = [] # stores all "path"
    
    costs = [] # stores cost of any path between "src" and "dst"
    cost = 0 #
    
    """
    recursive function to find routes and cost
    """
    def findPath(node, dst, path, cost):
        
        visited[node] = True # node is visited so don't visit it again.
        path.append(node) #node is added to path
        
        # if node becomes destiniton node, path which is from "src" to "dst" is added to "routes"
        # and calculated total cost is added to "costs"
        if node==dst:
            routes.append(list(path))
            costs.append(cost)
        else:
            for i in neighbors[node]: # visits all neighbors of the "node"
                if visited[i] == False: # if visited, pass it
                    costCalculated = calcCost(node, i) # calcultes cost between them
                    cost+=costCalculated #adds it to total cost which is up to that point
                    findPath(i, dst, path, cost) # recursion for visiting all nodes
                    cost-=costCalculated # it subtracts, because returning back so we must subtract previous costCalculated
        
        path.pop() # last node is removed, because a path from "src" to "dst" is found and now finds another way
        visited[node] = False
        
    findPath(src, dst, path, cost)
    
    return routes, costs

"""
calculates cost between "node1" and "node2"
"""
def calcCost(node1, node2):
    iX = nodes[node1][0][0]
    iY = nodes[node1][0][1]
    uX = nodes[node2][0][0]
    uY = nodes[node2][0][1]
    dist = np.sqrt(np.square(iX-uX)+np.square(iY-uY))
    batteryLvl = nodes[node2][3]
    return round(dist/batteryLvl, 4)


"""
prints path given for example:
    A -> B -> C -> D
"""
def printAPath(path):
    print("\t",end="")
    for i in range(len(path)-1):
        print(path[i],"-> ", end="")
    print(path[-1],end="")

"""
prints all routes from a node to another node and prints the cost. For example:
    4 ROUTE(S) FOUND:
    ROUTE 1: A -> B -> C -> D -> E -> F     COST: 5.3453
    ROUTE 2: A -> C -> G -> H -> K -> F     COST: 1.4567
    ROUTE 3: A -> D -> G -> C -> B -> F     COST: 2.5678
    ROUTE 4: A -> C -> H -> I -> F     COST: 0.5332
"""
def printPaths(routes, costs):
    c = 1
    print("\t"+str(len(routes)),"ROUTE(S) FOUND:")
    for path in routes:
        print("\tROUTE " + str(c) + ": ",end="")
        printAPath(path)
        print("\tCOST: ", costs[c-1])
        c+=1


"""
prints nodes and their nodes. For example:
    NODES & THEIR NEIGHBORS: A -> B, E, G, I, | B -> A, E, G, I, | D -> | E -> A, B, D, F, G, H, I, | F -> A, B, D, E, G, I, | G -> A, E, I, | H -> | I -> A, D, E, | 
    
"""
def printNeighbors():
    print("\tNODES & THEIR NEIGHBORS: ",end="")
    for i in nodes:
        print(i,"-> ",end="")
        for j in range(len(neighbors[i])-1):
            print(neighbors[i][j]+", ",end="")
        
        if len(neighbors[i])!=0:
            print(neighbors[i][-1],end="")
                
        print(" | ",end="")
    print("")

"""
create neighbors of all nodes in the "nodes" dictionary
    for example:
    neighbors ={A:[B,C,D],
                B:[E,F]}
"""
def createNeighbors():
    neighbors = {}
    for i in nodes:
        neighbors[i] = []
    for node1 in nodes.keys():
        for node2 in nodes.keys():
            if node1 == node2:
                continue
            if isInRange(node2,node1): #check if node2 is in range of node1
                neighbors[node1].append(node2)
    return neighbors

"""
node1 is in range of node2 or not?
"""
def isInRange(node1, node2):
    rangex = nodes[node2][1]
    rangey = nodes[node2][2]
    
    node2X = float(nodes[node2][0][0])
    node2Y = float(nodes[node2][0][1])
        
    node1X = float(nodes[node1][0][0])
    node1Y = float(nodes[node1][0][1])
    
    if node1X<=rangex[0]+node2X and node1X>=node2X-rangex[1] and node1Y<=rangey[0]+node2Y and node1Y>=node2Y-rangey[1]:
        return True
    return False

"""
changes the battery level of a "node" to "newBttry"
"""
def changeBattery(node, newBttry):
    nodes[node][3] = int(newBttry)

"""
moves a "node" to "newCoor"
"""
def move(node, newCoor):
    newCoor = newCoor.split(";")
    x = float(newCoor[0])
    y = float(newCoor[1])
    nodes[node][0] = (x,y)
    
"""
create a new node with that format:
    
    nodes[node] = [location, rangex, rangey, battery_level]
    
also adds the label of new node to the neighbors dictionary
    
"""
def createNode(command):
    local = command[3].split(";")
    x=float(local[0])
    y=float(local[1])
    rnge = command[4].split(";")
    x1=float(rnge[0])
    x2=float(rnge[1])
    y1=float(rnge[2])
    y2=float(rnge[3])
    battery=float(command[5])
    
    label = command[2]
    local = (x,y)
    rangex = (x1,x2)
    rangey = (y1,y2)
    
    nodes[label] = [local,rangex,rangey,battery]
    neighbors[label] = []
    print("\tCOMMAND *CRNODE*: New node",label,"is created")


"""
    prints general information in format below:
    neighbors
    all routes
    optimal route
"""
def printGeneralInfo(routes, costs):
    printNeighbors()
    if len(routes)==0:
        return    
    printPaths(routes,costs)
    i = np.argmin(costs)
    path = routes[i]
    print("\tSELECTED ROUTE ("+str(i+1)+"): ", end="")
    printAPath(path)
    print("")


nodes = {}
neighbors = {}

packetSize = float(sys.argv[1])

packetNum = 1

isSendStarted=False

t = 0 # time

totalByte = 1 #total byte to be sent. it is assigned to 1 to enter while loop, it is changed with command later.

file = open("commands","r")
commands = file.readlines()
file.close()

print("********************************\n"+
       "AD-HOC NETWORK SIMULATOR - BEGIN\n"+
       "********************************\n")

while(totalByte>0):
    print("SIMULATION TIME: ", time.strftime('%H:%M:%S', time.gmtime(t)))
    for cmd in commands:
        splt = cmd.split("\t")
        
        if t==int(splt[0]):
            if splt[1]=="CRNODE":
                createNode(splt)
            
            elif splt[1]=="MOVE":
                move(splt[2],splt[3])
                print("\tCOMMAND *MOVE*: The location of node",splt[2],"is changed")
            
            elif splt[1]=="SEND":
                totalByte = float(splt[4])
                src = splt[2]
                dst = splt[3]
                print("\tCOMMAND *SEND*: Data is ready to send from", src, " to",dst)
                isSendStarted=True
            elif splt[1]=="CHBTTRY":
                changeBattery(splt[2],splt[3])
                print("\tCOMMAND *CHBTTRY*: Battery level of node", splt[2] ,"is changed to", int(splt[3]))
                
            elif splt[1]=="RMNODE":
                n = splt[2].split("\n")[0]
                print("\tCOMMAND *RMNODE*: Node", n ,"is removed")
                neighbors.pop(n)
                nodes.pop(n)
                
            #if sending is started
            if isSendStarted:
                neighbors = createNeighbors()
                routes, costs = findRoutesAndCosts(src,dst)
                printGeneralInfo(routes,costs)
            
    if len(routes)==0:
        print("\tNO ROUTE FROM", src, "TO", dst, "FOUND.")
        break
    t+=1
    if isSendStarted:
        print("\tPACKET", packetNum, "HAS BEEN SENT")
        totalByte-=packetSize
        if totalByte<=0:
            totalByte=0
        print("\tREMAINING DATA SIZE:", totalByte, "BYTE")
        packetNum+=1
  

print("******************************\n"+
        "AD-HOC NETWORK SIMULATOR - END\n"+
        "******************************\n")
