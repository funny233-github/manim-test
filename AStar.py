UPArror = "↑"
DOWNArror = "↓"
LEFTArror = "←"
RIGHTArror = "→"
ANSI_BLACK = '\033[30m'  
ANSI_RED = '\033[31m'  
ANSI_GREEN = '\033[32m'  
ANSI_YELLOW = '\033[33m'  
ANSI_BLUE = '\033[34m'  
ANSI_PURPLE = '\033[35m'  
ANSI_CYAN = '\033[36m'  
ANSI_WHITE = '\033[37m'  
ANSI_NORMAL = '\033[0m'

class AstarMapNode:
    def __init__(self,isPath:bool,location:list[int]):
        if len(location) != 2:
            raise Exception("location is a two demension list")
        self.isPath = isPath
        self.nexts:list[AstarMapNode] = []
        self.pathDirection:None|str = None
        self.location = location
        self.cost = 0
        self.estimate = 0
        self.isRecommendPath = False
    def __repr__(self):
        if not self.isPath:
            return "#"

        if self.isRecommendPath and not self.pathDirection is None:
            return ANSI_GREEN+self.pathDirection+ANSI_NORMAL

        # if not self.pathDirection is None:
            # return self.pathDirection
        return" "
    def addNext(self,node):
        self.nexts.append(node)

class AstarMapStartAndEndNode(AstarMapNode):
    def __init__(self,isStart:bool,location:list[int]):
        super().__init__(True,location)
        self.isStart = isStart
    def __repr__(self):
        if self.isStart:
            return "S"
        return "E"


class AstarMap:

    def __init__(self,mapdata:str):
        if isinstance(mapdata,str):
            self.verifyStrMap(mapdata)
            self.gridMapBasedOnStr(mapdata)
        else:
            raise Exception("excepted map type, just support string")
    def __repr__(self):
        res = ""
        for rows in self.grid:
            for i in rows:
                res += str(i)
            res += "\n"
        return res

    def verifyStrMap(self,mapdata:str):
        fmapdata = mapdata[1:-1].split("\n")
        for i in range(len(fmapdata)):
            if len(fmapdata[i]) != len(fmapdata[i-1]):
                raise Exception("It's not a regular map which shape does not a rectangle")
    def initNodes(self,fmapdata:list[str]):
        ROW = len(fmapdata)
        COL = len(fmapdata[0])
        self.grid = [[AstarMapNode(False,[row,col]) for col in range(COL)] for row in range(ROW)]
        for row in range(ROW):
            for col in range(COL):
                if fmapdata[row][col] == "-":
                    self.grid[row][col].isPath = True
                elif fmapdata[row][col] == "S":
                    self.grid[row][col] = AstarMapStartAndEndNode(True,[row,col])
                    self.start = self.grid[row][col]
                elif fmapdata[row][col] == "E":
                    self.grid[row][col] = AstarMapStartAndEndNode(False,[row,col])
                    self.end = self.grid[row][col]

    def linkNodes(self):
        ROW = len(self.grid)
        COL = len(self.grid[0])
        for row in range(ROW):
            for col in range(COL):

                if not self.grid[row][col].isPath:
                    continue

                if row != 0 and self.grid[row-1][col].isPath == True:
                    self.grid[row][col].addNext(self.grid[row-1][col])

                if row != ROW-1 and self.grid[row+1][col].isPath == True:
                    self.grid[row][col].addNext(self.grid[row+1][col])

                if col != 0 and self.grid[row][col-1].isPath == True:
                    self.grid[row][col].addNext(self.grid[row][col-1])

                if col != COL-1 and self.grid[row][col+1].isPath == True:
                    self.grid[row][col].addNext(self.grid[row][col+1])

    def gridMapBasedOnStr(self,mapdata:str):
        fmapdata = mapdata[1:-1].split("\n")
        self.initNodes(fmapdata)
        self.linkNodes()

    def where(self,node:AstarMapNode):
        res = ""
        for rows in self.grid:
            for i in rows:
                if node is i:
                    res += "T"
                else:
                    res += str(i)
            res += "\n"
        print(res)

#location[row][col]
def calcCost(currentNode:AstarMapNode,targetNode:AstarMapNode):
    return abs(currentNode.location[0]-targetNode.location[0]) + abs(currentNode.location[1]-targetNode.location[1])

def calcPath(node:AstarMapNode,scene:AstarMap):
    for next in node.nexts:
        if not next.pathDirection is None:
            continue
        if next.location[1] > node.location[1]:
            next.pathDirection = LEFTArror
        if next.location[1] < node.location[1]:
            next.pathDirection = RIGHTArror
        if next.location[0] > node.location[0]:
            next.pathDirection = UPArror
        if next.location[0] < node.location[0]:
            next.pathDirection = DOWNArror

        next.cost = node.cost + 1
        next.estimate = calcCost(next,scene.start)
def astarCalc(scene:AstarMap):
    scene.start.cost = calcCost(scene.start,scene.end)
    frontiers = set([scene.start])
    reached = set([scene.start])

    while not scene.end in frontiers:
        minValue = min([frontier.cost+frontier.estimate for frontier in frontiers])

        for frontier in frontiers:
            if frontier.cost+frontier.estimate == minValue: 
                calcPath(frontier,scene)
                reached = reached | set([frontier])
                frontiers = frontiers - set([frontier])
                for x in frontier.nexts:
                    if x not in reached:
                        frontiers = frontiers | set([x])
                break
def getPath(scene:AstarMap):
    astarCalc(scene)
    pos = scene.end
    while not pos is scene.start:
        direction = pos.pathDirection
        for next in pos.nexts:
            pos.isRecommendPath = True
            if direction == LEFTArror and next.location[1] < pos.location[1]:
                pos = next
                break
            if direction == RIGHTArror and next.location[1] > pos.location[1]:
                pos = next
                break
            if direction == UPArror and next.location[0] < pos.location[0]:
                pos = next
                break
            if direction == DOWNArror and next.location[0] > pos.location[0]:
                pos = next
                break
