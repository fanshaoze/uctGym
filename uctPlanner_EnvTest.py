import sys
import math
import copy
import random
from uct_EnvTest import State, SimAction, Simulator
#from Env.EnvWrapper import EnvWrapper
import numpy as np
from GymWrapper import EnvWrapper
import datetime
import uct_EnvTest


class ToyState(State):
	def __init__(self, _state):
		self.state_ = _state

	def equal(self, state):
		#TODO __dict__ may not be effective
		if isinstance(state, ToyState):
			#return self.state_.__dict__ == state.__dict__
			#print(type(state.state_))
			state_equal = np.array_equal(self.state_, state.state_)
			#print(state_equal)
			return state_equal
		else:
			print("wrong state type")
			return False

	def duplicate(self):
		other = ToyState(self.state_)
		return other

	def print(self):  # print x,y,and food
		print(self.state_, end='')


class ToyAction(SimAction):
	def __init__(self, _action):
		self.action_ = _action

	def duplicate(self):
		other = ToyAction(self.action_)
		return other

	def print(self):
		print(self.action_, end='')

	def equal(self, other):
		#TODO possible that the isinstance is wrong
		# assert (isinstance(other, ToyAction))
		if isinstance(other, ToyAction):
			return other.action_ == self.action_
		else:
			print("wrong action type")
			return False


# Toy simulator
class ToySimulator(Simulator):

#TODO when init this, we need to start with wrapper
	def __init__(self, _env_params):
		# init the simulator,start from(0,2)
		self.done = False
		self.reward = 0
		self.actVect = []
		self.env_params_ = _env_params
		self.wrapped_env = EnvWrapper(**_env_params)
		self.action_n_ = self.wrapped_env.get_action_n()
		for i in range(self.action_n_):
			self.actVect.append(ToyAction(i))
		init_state = self.wrapped_env.reset()
		self.current = ToyState(init_state)

	def __del__(self):
		self.actVect.clear()
		del self.current
		pass

	def setState(self, _state, _done):  # Done
		if isinstance(_state, ToyState):
			self.current = copy.deepcopy(_state)
			checkpoint = self.wrapped_env.checkpoint_with_state(_state.state_)
			self.wrapped_env.restore(checkpoint)
			self.done = _done
		else:
			print("wrong state type")
			return

	def getState(self):  # Done
		return self.current

	def act(self, action):
		assert (not self.isTerminal())
		if not isinstance(action, ToyAction):
			print("wrong action type")
			return 0
		_action = action.action_
		next_state, reward, done = self.wrapped_env.step(_action)
		self.current.state_ = next_state
		self.done = done
		self.reward = reward
		return reward

	# get all the actions taked
	def getActions(self):  # Done
		return self.actVect

	# there is a food on the right bound of the range
	def isTerminal(self):  # Done
		return self.done

	# the place of the food is random
	def reset(self):  # Done
		self.done = False
		self.reward = 0
		init_state = self.wrapped_env.reset()
		self.current = ToyState(init_state)

# env_name = "AlienNoFrameskip-v0"
# max_episode_length = 10
# _env_params = {
#         "env_name": env_name,
#         "max_episode_length": max_episode_length
#     }
#
# wrapped_env = EnvWrapper(**_env_params)
# state = wrapped_env.env.reset()
# print(wrapped_env.env.action_space)
# print(state)
# wrapped_env.checkpoint()

# action_n = wrapped_env.get_action_n()
# print(action_n)
# toy_state = ToyState(state)
# sim = ToySimulator(_env_params)
# toy_state = sim.getState()
# print(toy_state.state_)
# action = wrapped_env.env.action_space.sample()
# sim.act(ToyAction(action))
# print(sim.getState().state_,sim.done,sim.reward)
# action = wrapped_env.env.action_space.sample()
# next_state, reward, done = wrapped_env.step(action)
# sim.setState(ToyState(next_state), done)
# sim.getActions()









env_name = "Breakout-v4"
max_episode_length = 100000
_env_params = {
        "env_name": env_name,
        "max_episode_length": max_episode_length
    }

depthList = [5]
trajectory = [5000]
initPositionList = [(2,3,1)]
numGames = 1
outFilename = "multitestpro-out.txt"
starttime = datetime.datetime.now()
fo = open(outFilename, "w")
fo.write("maxdepth,num_Runs,avgstep\n")
sim = ToySimulator(_env_params)
sim2 = ToySimulator(_env_params)
avgsteps = 0
avgstep_list = []
initNums = len(initPositionList)
initNums = 1
initsize = 0
ransize = 0
initstate = ToyState(sim.getState())
avg_cumulate_reward = 0
#(self, _sim, _maxDepth, _numRuns, _ucbScalar, _gamma, _leafValue, _endEpisodeValue):
for max_depth in depthList:
    for num_Runs in trajectory:
        print(max_depth,",",num_Runs)
        avgsteps = 0
        uctTree = uct_EnvTest.UCTPlanner(sim2, max_depth, num_Runs, 1, 0.95, 0, 0)
        #uctTree = uct.UCTPlanner(sim2, 30, 110, 1, 0.95, 0, 0)
        print (numGames,initNums)
        for j in range (0,initNums):
            for i in range(0, int(numGames/initNums)):
                #sim.setState(initstate, False)
                steps = 0
                r = 0
                #sim.getState().print()
                print(sim.isTerminal())
                while not sim.isTerminal():
                    steps += 1
                    uctTree.setRootNode(sim.getState(), sim.getActions(), r, sim.isTerminal())
                    #print()
                    uctTree.plan()
                    #print()
                    #return the action with the highest reward
                    action = uctTree.getAction()
                    print("-action:", end='')
                    action.print()
                    sim.wrapped_env.render()
                    #print("->", end='')
                    #uctTree.testTreeStructure()
                    # 先序遍历，测试所有节点
                    #uctTree.testDeterministicProperty()
                    r = sim.act(action)
                    avg_cumulate_reward += r
                    #sim.getState().print()
                    print(" reward:",uctTree.root_.reward_,end='')
                    print("")
                    #sim.getState().print()
                sim.reset()
                print("#####################Game:", i, "  steps: ", steps, "  average cumulate reward: ", avg_cumulate_reward)
                avgsteps += steps
        avgsteps = avgsteps/numGames
        fo.write(str(max_depth)+","+str(num_Runs)+","+str(avgsteps)+"\n")
        print(max_depth,",",num_Runs,":",avgsteps)

        avgstep_list.append(avgsteps)
endtime = datetime.datetime.now()
print("execute time: ",(endtime - starttime).seconds)
#avgtimes+=(endtime - starttime).seconds
fo.close()
#print("avgtimes:",avgtimes/20)
