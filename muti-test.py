import _thread
import threading
import time
import sys
import math
import random
import uct
import uctPlanner
import datetime
from multiprocessing import Process
import cProfile
from multiprocessing import Pool


def depth_tradactary_Test(depthList, trajectory, initPositionList, numGames, outFilename):
    starttime = datetime.datetime.now()
    fo = open(outFilename, "w")
    fo.write("maxdepth,num_Runs,avgstep\n")
    sim = uctPlanner.ToySimulator()
    sim2 = uctPlanner.ToySimulator()
    avgsteps = 0
    avgstep_list = []
    initNums = len(initPositionList)
    initsize = 0
    ransize = 0
    #(self, _sim, _maxDepth, _numRuns, _ucbScalar, _gamma, _leafValue, _endEpisodeValue):
    for max_depth in depthList:
        for num_Runs in trajectory:
            print(max_depth,",",num_Runs)
            avgsteps = 0
            uctTree = uct.UCTPlanner(sim2, max_depth, num_Runs, 1, 0.95, 0, 0)
            #uctTree = uct.UCTPlanner(sim2, 30, 110, 1, 0.95, 0, 0)
            print (numGames,initNums)
            for j in range (0,initNums):
                initstate = uctPlanner.ToyState(initPositionList[j][0],initPositionList[j][1],initPositionList[j][2])
                for i in range(0, int(numGames/initNums)):
                    sim.setState(initstate)
                    steps = 0
                    r = 0
                    #sim.getState().print()
                    while not sim.isTerminal():
                        steps += 1
                        uctTree.setRootNode(sim.getState(), sim.getActions(), r, sim.isTerminal())
                        #print()
                        uctTree.plan()
                        #return the action with the highest reward
                        action = uctTree.getAction()
                        #print("-action:", end='')
                        #action.print()
                        #print("->", end='')
                        #uctTree.testTreeStructure()
                        # 先序遍历，测试所有节点
                        #uctTree.testDeterministicProperty()
                        r = sim.act(action)
                        #sim.getState().print()
                        #print("reward:",uctTree.root_.reward_,end='')
                        #print("")
                        #sim.getState().print()
                    #sim = sim.reset()
                    #print("#####################Game:", i, "  steps: ", steps, "  r: ", r)
                    avgsteps += steps
            avgsteps = avgsteps/numGames
            fo.write(str(max_depth)+","+str(num_Runs)+","+str(avgsteps)+"\n")
            print(max_depth,",",num_Runs,":",avgsteps)

            avgstep_list.append(avgsteps)
    endtime = datetime.datetime.now()
    print("execute time: ",(endtime - starttime).seconds)
    fo.close()
    return avgstep_list

    # varstep = 0
    # print(avgstep_list)
    # for v in range(0,len(avgstep_list)):
    #     varstep += avgstep_list[v]
    # varstep = varstep/len(avgstep_list)
    # print(varstep)
    # varresult = 0
    # for v in range(0,len(avgstep_list)):
    #     varresult += (avgstep_list[v]-varstep)*(avgstep_list[v]-varstep)
    # print("var:",varresult)





def initPosition(PostionNumber):
    initPostionX = []
    initPostionY = []
    initFood = []
    initNums = PostionNumber

    initsize = 0
    ransize = 0
    while (True):
        initflag = 0
        tmpx = random.randint(0,4)
        tmpy = random.randint(0,4)
        tmpFood = random.randint(0,4)
        print(tmpx,tmpy,tmpFood)
        ransize+=1
        for initindex in range(0,len(initPostionX)):
            if (initPostionX[initindex] == tmpx and initPostionY[initindex] == tmpy) \
                    or tmpy == tmpFood:
                initflag = 1
                break
        if initflag == 1:
            continue
        else:
            initPostionX.append(tmpx)
            initPostionY.append(tmpy)
            initFood.append(tmpFood)
            initsize += 1
            if initsize == initNums:
                break
    #(self, _sim, _maxDepth, _numRuns, _ucbScalar, _gamma, _leafValue, _endEpisodeValue):
    PositionList = []
    for i in range(0,initsize):
        PositionList.append((initPostionX[i],initPostionY[i],initFood[i]))
    return PositionList

def generatedepthList(start,end,steplen):
    max_depth = []
    for i in range(start,end,steplen):
        max_depth.append(i)
    return max_depth

def generatetrajList(start,end,steplen):
    traj = []
    for i in range(start,end,steplen):
        traj.append(i)
    return traj

# 为线程定义一个函数
def print_time( threadName, delay):
   count = 0
   while count < 5:
      time.sleep(delay)
      count += 1
      print ("%s: %s" % ( threadName, time.ctime(time.time()) ))

# 创建两个线程
#def depth_tradactary_Test(depthList, trajectory, initPositionList, numGames, outFilename):

#depth_tradactary_Test([4],[2000],[(2,3,1)],100,"multitestpro-out.txt")


def main():
    print("main program start")
    foconf = open("config", "r")
    foPosition = open("positions.txt", "w")

    text = foconf.readline()
    textlist = text.split("=")
    threadNum = int(textlist[1])

    text = foconf.readline()
    textlist = text.split("=")
    PositionNum = int(textlist[1])

    text = foconf.readline()
    textlist = text.split("=")
    numGame = int(textlist[1])

    text = foconf.readline()
    textlist = text.split("=")
    depstart = int(textlist[1])
    text = foconf.readline()
    textlist = text.split("=")
    depend = int(textlist[1])
    text = foconf.readline()
    textlist = text.split("=")
    depStepLen = int(textlist[1])

    text = foconf.readline()
    textlist = text.split("=")
    trajstart = int(textlist[1])
    text = foconf.readline()
    textlist = text.split("=")
    trajend = int(textlist[1])
    text = foconf.readline()
    textlist = text.split("=")
    trajStepLen = int(textlist[1])

    foconf.close()

    PositionSeed = initPosition(PositionNum)
    PositionList = []
    for i in range(0,threadNum):
        PositionList.append(PositionSeed[i:i+int(PositionNum/threadNum)])
        for j in range(i,i+int(PositionNum/threadNum)):
            foPosition.write(str(PositionSeed[i:i+int(PositionNum/threadNum)])+"\n")
    print(PositionList)
    foPosition.close()
    foPosition = open("positions.txt", "r")

    deplist = generatedepthList(depstart,depend,depStepLen)
    trajlist = generatetrajList(trajstart,trajend,trajStepLen)
    #fixed lists!
    # deplist = [4,5,7,10,14,19,25]
    # trajlist = [750,2000,4000,6000]
    # deplist = [4,5,7,10,14,16,18,19,20,22,24,25]
    # trajlist = [7000,9000,11000,13000,15000,17000,19000]
    deplist = [2,3]
    trajlist = [10,20]
    #fixed lists!
    fileList = []
    for j in range(0,threadNum):
        filename = "mutitest"+str(j)+".txt"
        fileList.append(filename)
    print(fileList)
    #def depth_tradactary_Test(depthList, trajectory, initPositionList, numGames, outFilename):
    threads = []
    for i in range(0, threadNum):
        t = Process(target=depth_tradactary_Test, args=(deplist, trajlist,PositionList[i],numGame/threadNum,fileList[i]))
        threads.append(t)
        t.start()
    # for i in range(0, threadNum):
    #     t = threading.Thread(target=depth_tradactary_Test, args=(deplist, trajlist,PositionList[i],numGame,fileList[i]))
    #     threads.append(t)
    #     t.start()

    print("main program running")

    #
    #     for i in range(0,threadNum):
    #         _thread.start_new_thread(depth_tradactary_Test, (deplist, trajlist,PositionList[i],numGame,fileList[i]))
    #
    #
    #
    #
    # try:
    #
    # except:
    #    print ("Error: 无法启动线程")
    #
    # while 1:
    #     print("123")
    #     pass

if __name__ == "__main__":
    main()


