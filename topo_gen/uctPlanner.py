import sys
import math
import random
import uct
import datetime


class ToyState(uct.State):
    def __init__(self, _x, _y, _food):
        self.x = _x
        self.y = _y
        self.food = _food

    def equal(self, state):
        if isinstance(state, ToyState):
            if state.x != self.x or state.y != self.y or state.food != self.food:
                return False
            else:
                return True
        else:
            return False

    def duplicate(self):
        other = ToyState(self.x, self.y, self.food)
        return other

    def print(self):#print x,y,and food
        print("(", self.x, ",", self.y, ",", self.food, ")",end='')


class ToyAction(uct.SimAction):
    def __init__(self, _id):
        self.id = _id

    def duplicate(self):
        other = ToyAction(self.id)
        return other

    def print(self):
        print(self.id,end='')

    def equal(self, other):
        if isinstance(other, ToyAction):
            return other.id == self.id
        else:
            return False

class ToySimulator(uct.Simulator):

    def __init__(self):#Done
        #init the simulator,start from(0,2)
        self.reward = 0
        self.actVect = []
        self.actVect.append(ToyAction(0))
        self.actVect.append(ToyAction(1))
        self.actVect.append(ToyAction(2))
        self.actVect.append(ToyAction(3))
        self.current = ToyState(0,2,0)

    def __del__(self):
        # del self.actVect[0]
        # del self.actVect[1]
        # del self.actVect[2]
        # del self.actVect[3]
        # del self.current
        pass

    def setState(self, state):
        if isinstance(state, ToyState):
            self.current.x = state.x
            self.current.y = state.y
            self.current.food = state.food
        else:
            return

    def getState(self):
        return self.current

    def act(self, action):
        assert (not self.isTerminal())
        if not isinstance(action, ToyAction):
            return 0
        aid = action.id
        if random.random() < 0.1:
            aid = int(random.random()*4)
            # print("random happen!")
        if aid == 0:
            if (self.current.x == 0) and (self.current.y > 0):
                self.current.y -= 1
        elif aid == 1:
            if (self.current.x == 0) and (self.current.y < 4):
                self.current.y += 1
        elif aid == 2:
            if self.current.x > 0:
                self.current.x -= 1
        elif aid == 3:
            if self.current.x < 4:
                self.current.x += 1
        if (self.current.x == 4) and (self.current.y == self.current.food):
            return 10
        else:
            return 0
    def getActions(self):#Done
        return self.actVect
#there is a food on the right bound of the range
    def isTerminal(self):#Done
        if self.current.x == 4 and self.current.y == self.current.food:
            return True
        return False
# the place of the food is random
    def reset(self):#Done
        self.current.x = 0
        self.current.y = 2
        self.current.food = int(random.random()*5)
        return self
    def setfood(self):#Done
        self.current.food = int(random.random()*5)
        return self









































#
# depthList = [-1]
# trajectory = [100]
# initPositionList = [(2,3,1)]
# numGames = 1
# outFilename = "singleTest.txt"
# starttime = datetime.datetime.now()
# fo = open(outFilename, "w")
# fo.write("maxdepth,num_Runs,avgstep\n")
# sim = ToySimulator()
# sim2 = ToySimulator()
# avgsteps = 0
# avgstep_list = []
# initNums = len(initPositionList)
# initsize = 0
# ransize = 0
# #(self, _sim, _maxDepth, _numRuns, _ucbScalar, _gamma, _leafValue, _endEpisodeValue):
# for max_depth in depthList:
#     for num_Runs in trajectory:
#         print(max_depth,",",num_Runs)
#         avgsteps = 0
#         uctTree = uct.UCTPlanner(sim2, max_depth, num_Runs, 1, 0.95, 0, 0)
#         print (numGames,initNums)
#         for j in range (0,initNums):
#             initstate = ToyState(initPositionList[j][0],initPositionList[j][1],initPositionList[j][2])
#             for i in range(0, int(numGames/initNums)):
#                 sim.setState(initstate)
#                 steps = 0
#                 r = 0
#                 sim.getState().print()
#                 while not sim.isTerminal():
#                     steps += 1
#                     uctTree.setRootNode(sim.getState(), sim.getActions(), r, sim.isTerminal())
#                     print()
#                     uctTree.plan()
#                     #return the action with the highest reward
#                     action = uctTree.getAction()
#                     print("-action:", end='')
#                     action.print()
#                     print("->", end='')
#                     #test
#                     '''
#                     uctTree.testTreeStructure()
#                     # Preorder traversal, test all the nodes
#                     #uctTree.testDeterministicProperty()
#                     '''
#                     r = sim.act(action)
#                     sim.getState().print()
#                     print("reward:",uctTree.root_.reward_,end='')
#                     print("")
#                 #sim = sim.reset()
#                 print("Game:", i, "  steps: ", steps, "  final reward: ", r)
#                 avgsteps += steps
#         avgsteps = avgsteps/numGames
#         fo.write(str(max_depth)+","+str(num_Runs)+","+str(avgsteps)+"\n")
#
#         #print("max_depth",max_depth,",",num_Runs,":",avgsteps)
#
#         avgstep_list.append(avgsteps)
# endtime = datetime.datetime.now()
# print("execute time: ",(endtime - starttime).seconds,"s")
# #avgtimes+=(endtime - starttime).seconds
# fo.close()
# #print("avgtimes:",avgtimes/20)






