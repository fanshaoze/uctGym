import sys
import math
import copy
import random
from uct_EnvTest import State, SimAction, Simulator
from GymWrapper import EnvWrapper
import datetime
import uct_EnvTest
import numpy as np
from util import mkdir
import time


class ToyState(State):
	def __init__(self, _state, _done=False):
		# TODO add done attribute
		self.state_ = copy.deepcopy(_state)
		self.done_ = _done
		#print(type(self.state_))

	def equal(self, _state):
		# TODO __dict__ may not be effective
		if isinstance(_state, ToyState):
			return np.array_equal(self.state_[0], _state.state_[0])
		else:
			print("wrong state type")
			return False

	def duplicate(self):
		other = ToyState(self.state_, self.done_)
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
		if isinstance(other, ToyAction):
			return other.action_ == self.action_
		else:
			print("wrong action type")
			return False


# Toy simulator
class ToySimulator(Simulator):

	# TODO when init this, we need to start with wrapper
	def __init__(self, _env_params):
		self.reward = 0
		self.actVect = []
		self.env_params_ = _env_params
		self.wrapped_env = EnvWrapper(**_env_params)
		self.action_n_ = self.wrapped_env.get_action_n()
		for i in range(self.action_n_):
			self.actVect.append(ToyAction(i))
		self.wrapped_env.reset()
		self.current = ToyState(self.wrapped_env.get_cloned_state(), False)

	def __del__(self):
		# self.actVect.clear()
		# del self.current
		pass

	def setState(self, _state):  # Done
		if isinstance(_state, ToyState):
			self.wrapped_env.restore_with_state(_state.state_)
			self.current.state_ = self.wrapped_env.get_cloned_state()
			self.current.done_ = _state.done_
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
		#self.wrapped_env.render()
		self.current.state_ = self.wrapped_env.get_cloned_state()
		self.current.done_ = done
		#self.reward = reward
		return reward

	# get all the actions taked
	def getActions(self):  # Done
		return self.actVect

	# there is a food on the right bound of the range
	def isTerminal(self):  # Done
		return self.current.done_

	# the place of the food is random
	def reset(self):  # Done
		init_state = self.wrapped_env.reset()
		self.current.state_ = self.wrapped_env.get_cloned_state()
		self.current.done_ = False


env_name = "BreakoutNoFrameskip-v4"
max_episode_length = 1000000000
_env_params = {
	"env_name": env_name,
	"max_episode_length": max_episode_length
}
dt = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
mkdir(dt)
depthList = [100]
trajectory = [100]
numGames = 1
outFilename = "multitestpro-out.txt"
starttime = datetime.datetime.now()
fo = open(outFilename, "w")
fo.write("maxdepth,num_Runs,avgstep\n")
sim = ToySimulator(_env_params)

sim2 = ToySimulator(_env_params)
avgsteps = 0
avgstep_list = []
initNums = 1
initsize = 0
ransize = 0
initstate = copy.deepcopy(sim.getState())

sim.setState(initstate)
state_init = sim.wrapped_env.get_cloned_state()
actions = []
for i in range(5):
	actions.append(sim.wrapped_env.env.action_space.sample())
for i in range(5):
	sim.act(ToyAction(actions[i]))
state0 = sim.wrapped_env.get_cloned_state()
print(type(state0[0]),type(sim.current.state_[0]))
print("sim state is equal to cloned state? ",np.array_equal(state0[0],sim.current.state_[0]))
sim.setState(initstate)
state_next_init = sim.wrapped_env.get_cloned_state()
print(type(state_init[0]),type(state_next_init[0]))
print("reset state successfully? ", np.array_equal(state_init[0], state_next_init[0]))
for i in range(5):
	sim.act(ToyAction(actions[i]))
state1 = sim.wrapped_env.get_cloned_state()
print(type(state0[0]))
print("second act state equal? ", np.array_equal(state0[0], state1[0]))
sys.exit()

avg_cumulate_reward = 0
# (self, _sim, _maxDepth, _numRuns, _ucbScalar, _gamma, _leafValue, _endEpisodeValue):
for max_depth in depthList:
	for num_Runs in trajectory:
		print(max_depth, ",", num_Runs)
		avgsteps = 0
		uctTree = uct_EnvTest.UCTPlanner(sim2, max_depth, num_Runs, 1, 1, 0, 0, True)
		print(numGames, initNums)
		for j in range(0, initNums):
			for i in range(0, int(numGames / initNums)):
				sim.setState(initstate)
				steps = 0
				r = 0
				# sim.getState().print()

				while not sim.isTerminal():
					steps += 1
					uctTree.setRootNode(sim.getState(), sim.getActions(), r, sim.isTerminal())
					origin_state = sim.wrapped_env.get_cloned_state()
					origin_done = sim.isTerminal()
					'''test equal
					print(uctTree.root_.state_.equal(ToyState(origin_state,origin_done)))
					sim.wrapped_env.render()
					'''
					tree_size = uctTree.plan()
					# print()
					action = uctTree.getAction()

					#reset the sim state as the root
					sim.setState(ToyState(origin_state,origin_done))

					print("-action:", end='')
					action.print()
					# print("->", end='')
					print("")
					# uctTree.testTreeStructure()
					# uctTree.testDeterministicProperty()

					r = sim.act(action)

					image_dir = dt+"/"+str(steps)+".png"
					sim.wrapped_env.env.ale.saveScreenPNG(image_dir)

					sim.wrapped_env.render()
					avg_cumulate_reward += r
					''' Test 
					simstate = sim.wrapped_env.get_cloned_state()
					print("after the act, state different with before? ", np.array_equal(simstate[0], uctTree.root_.state_.state_[0]))
					'''
					# sim.getState().print()
					print(" reward:", uctTree.root_.reward_, end='')
					print("")
					# sim.getState().print()
				print("#####################Game:", i, "  steps: ", steps, "  average cumulate reward: ",
					  avg_cumulate_reward)
				avgsteps += steps
		avgsteps = avgsteps / numGames
		fo.write(str(max_depth) + "," + str(num_Runs) + "," + str(avgsteps) + "\n")
		print(max_depth, ",", num_Runs, ":", avgsteps)

		avgstep_list.append(avgsteps)
endtime = datetime.datetime.now()
print("execute time: ", (endtime - starttime).seconds)
# avgtimes+=(endtime - starttime).seconds
fo.close()
# print("avgtimes:",avgtimes/20)

