import os
import sys
import math
import random
import shutil

import graphviz
from graphviz import Digraph
import uct
import datetime
import uctPlanner


def delAllFiles(rootdir):
	filelist = []
	filelist = os.listdir(rootdir)  # list all the files
	for f in filelist:
		filepath = os.path.join(rootdir, f)  # path-absolute path
		if os.path.isfile(filepath):  # is file?
			os.remove(filepath)  # delete file
		elif os.path.isdir(filepath):
			shutil.rmtree(filepath, True)  # is dir


class TreeGraph(object):

	def __init__(self, nodeList_):
		self.grap_g = Digraph("G", format="png")
		self.sub_g0 = Digraph(comment="process1", graph_attr={"style": 'filled'})

		self.nodeIndex = -1
		self.nodeList = nodeList_
		self.destLeafIndex = 3
		# self.destLeafIndex = len(self.nodeList)-1
		self.pathIndex = []

	def GenerateLabel(self, Index, state):
		# need modified for circulate
		#return "(" + str(state.x) + "," + str(state.y) + "," + str(state.food) + ") #" + str(Index)
		#return str(Index)
		tmplabel = '{}\n'.format(state.component_pool)
		label = ""
		for i in range(0,len(tmplabel),12):
			label+=tmplabel[i:i+12]+"\n"
		label = label[0:len(label)-1]
		return label

	# uctTree is the Tree,
	def GenerateActionLabel(self, action):
		if action.type == 'node':
			return "N"+"|"+str(action.value)
		else:
			return "E"+"|"+str(action.value)

	def getNodeIndex(self, stateNode):
		for i in range(0, len(self.nodeList)):
			if stateNode == self.nodeList[i]:
				return i
		return -1

	def pathSearch(self, StateNode):
		pathIndex = []
		pathIndex.append(self.getNodeIndex(StateNode))
		while StateNode.parentAct_ is not None:
			parentAct = StateNode.parentAct_
			StateNode = parentAct.parentState_
			pathIndex.append(self.getNodeIndex(StateNode))
		return pathIndex

	def drawAll(self, uctTree, folder):
		for i in range(0, len(self.nodeList)):
			self.grap_g = None
			self.sub_g0 = None
			self.grap_g = Digraph("G", format="png")
			self.sub_g0 = Digraph(comment="process1", graph_attr={"style": 'filled'})
			fileName = folder + "/test-table" + str(i)
			self.drawSearch(uctTree, i, fileName)

	def drawSearch(self, uctTree, _destLeafIndex, fileName):
		self.destLeafIndex = _destLeafIndex
		self.pathIndex = self.pathSearch(self.nodeList[self.destLeafIndex])
		# print(self.pathIndex)
		self.nodeIndex += 1
		rootIndex = self.nodeIndex
		rootIndex = self.getNodeIndex(uctTree.root_)
		self.sub_g0.node(str(rootIndex), self.GenerateLabel(rootIndex, uctTree.root_.state_),
						 _attributes={"style": "filled", "color": "grey"})
		self.drawTree(rootIndex, uctTree.root_, None, None, None)
		self.grap_g.subgraph(self.sub_g0)
		self.grap_g.render(fileName, view=False)

	# def getLineLable(self, parentState, aid):
	# 	if aid == 0:
	# 		if (parentState.state_.x == 0) and (parentState.state_.y > 0):
	# 			return "down"
	# 	elif aid == 1:
	# 		if (parentState.state_.x == 0) and (parentState.state_.y < 4):
	# 			return "up"
	# 	elif aid == 2:
	# 		if parentState.state_.x > 0:
	# 			return "left"
	# 	elif aid == 3:
	# 		if parentState.state_.x < 4:
	# 			return "right"
	# 	return "stay"
	def getLineLable(self, parentState, actionLable):
		return actionLable

	def drawTree(self, currentIndex, v_stateNode, parentsIndex, parentState, actionLabel):
		actVisitCounter = 0
		actSize = len(v_stateNode.nodeVect_)
		# print("1##",self.GenerateLabel(currentIndex,v_stateNode.state_))
		if parentState is not None:
			# print("2##",self.GenerateLabel(parentsIndex,parentState.state_))
			lineLable = self.getLineLable(parentState, actionLabel)
			if currentIndex > self.destLeafIndex:
				self.grap_g.edge(str(parentsIndex), str(currentIndex), lineLable, color="white", fontcolor="white")
			elif currentIndex in self.pathIndex:
				self.grap_g.edge(str(parentsIndex), str(currentIndex), lineLable)
			else:
				self.grap_g.edge(str(parentsIndex), str(currentIndex))

		for i in range(0, actSize):
			actionLabel = self.GenerateActionLabel(v_stateNode.actVect_[i])
			# print (actionId)
			v_actionNode = v_stateNode.nodeVect_[i]
			stateSize = len(v_actionNode.stateVect_)
			for j in range(0, stateSize):
				v_childStateNode = v_actionNode.stateVect_[j]
				# print("3##",self.GenerateLabel(actionId,v_childStateNode.state_))
				self.nodeIndex += 1
				childIndex = self.nodeIndex
				childIndex = self.getNodeIndex(v_childStateNode)
				if childIndex in self.pathIndex:
					self.sub_g0.node(str(childIndex), self.GenerateLabel(childIndex, v_childStateNode.state_) \
									 , _attributes={"style": "filled", "color": "grey"})
				elif childIndex < self.destLeafIndex:
					self.sub_g0.node(str(childIndex), self.GenerateLabel(childIndex, v_childStateNode.state_))
				else:
					self.sub_g0.node(str(childIndex), self.GenerateLabel(childIndex, v_childStateNode.state_) \
									 , _attributes={"style": "filled", "color": "white"}, fontcolor="white")

				# print("4##",self.GenerateLabel(childIndex,v_childStateNode.state_))
				# print("5##",self.GenerateLabel(currentIndex,v_stateNode.state_))
				self.drawTree(childIndex, v_childStateNode, currentIndex, v_stateNode, actionLabel)

	def drawExpend(self, sim):
		pass


# depthList = [4]
# trajectory = [10]
# initPositionList = [(2, 3, 1)]
# numGames = 1
# outFilename = "multitestpro-out.txt"
# starttime = datetime.datetime.now()
# fo = open(outFilename, "w")
# fo.write("maxdepth,num_Runs,avgstep\n")
# sim = uctPlanner.ToySimulator()
# sim2 = uctPlanner.ToySimulator()
# avgsteps = 0
# avgstep_list = []
# initNums = len(initPositionList)
# initsize = 0
# ransize = 0
# # (self, _sim, _maxDepth, _numRuns, _ucbScalar, _gamma, _leafValue, _endEpisodeValue):
# for max_depth in depthList:
# 	for num_Runs in trajectory:
# 		print(max_depth, ",", num_Runs)
# 		avgsteps = 0
# 		uctTree = uct.UCTPlanner(sim2, max_depth, num_Runs, 1, 0.95, 0, 0)
# 		# uctTree = uct.UCTPlanner(sim2, 30, 110, 1, 0.95, 0, 0)
# 		print(numGames, initNums)
# 		for j in range(0, initNums):
# 			initstate = uctPlanner.ToyState(initPositionList[j][0], initPositionList[j][1], initPositionList[j][2])
# 			for i in range(0, int(numGames / initNums)):
# 				sim.setState(initstate)
# 				steps = 0
# 				r = 0
# 				# sim.getState().print()
# 				while not sim.isTerminal():
# 					steps += 1
# 					uctTree.setRootNode(sim.getState(), sim.getActions(), r, sim.isTerminal())
# 					# print()
# 					nodeList = uctTree.plan()
# 					# viz start
# 					folder = "./viz" + str(steps)
# 					isExists = os.path.exists(folder)
# 					if not isExists:
# 						os.makedirs(folder)
# 					else:
# 						delAllFiles(folder)
# 					treeviz = TreeGraph(nodeList)
# 					treeviz.drawAll(uctTree, folder)
#
# 					# viz finished
# 					# return the action with the highest reward
# 					action = uctTree.getAction()
# 					# print("-action:", end='')
# 					# action.print()
# 					# print("->", end='')
# 					# uctTree.testTreeStructure()
# 					# 先序遍历，测试所有节点
# 					# uctTree.testDeterministicProperty()
# 					r = sim.act(action)
# 					# sim.getState().print()
# 					# print("reward:",uctTree.root_.reward_,end='')
# 					# print("")
# 					# sim.getState().print()
# 					break
# 				# sim = sim.reset()
# 				print("#####################Game:", i, "  steps: ", steps, "  r: ", r)
# 				avgsteps += steps
# 		avgsteps = avgsteps / numGames
# 		fo.write(str(max_depth) + "," + str(num_Runs) + "," + str(avgsteps) + "\n")
# 		print(max_depth, ",", num_Runs, ":", avgsteps)
#
# 		avgstep_list.append(avgsteps)
# endtime = datetime.datetime.now()
# print("execute time: ", (endtime - starttime).seconds)
# # avgtimes+=(endtime - starttime).seconds
# fo.close()
