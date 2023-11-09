import AStar as AS
MAP = """
S--#-----#-----#--E
---#--#--#-----#---
---#--#--#-#---#-##
---#-----#-#---#---
---#--#----#---#---
---#--#--###---###-
---#--####-----#---
---#-----#--#--#---
---------#--#------
---#-----#-----#---
"""

test = AS.AstarMap(MAP)
print(test)
AS.getPath(test)
print(test)
costs = []
for i in test.grid:
    for j in i:
        costs.append(j.cost)
print(costs)
