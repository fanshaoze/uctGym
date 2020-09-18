import os
import random
import uct
import collections
import networkx as nx
import matplotlib.pyplot as plt
import uctViz
from copy import deepcopy


def union(x, y, parent):
	f_x = find(x, parent)
	f_y = find(y, parent)
	if f_x == f_y:
		return False
	parent[f_x] = f_y
	return True


def find(x, parent):
	if parent[x] != x:
		parent[x] = find(parent[x], parent)
	return parent[x]


def convert_graph(graph, comp2port_mapping, parent, same_device_mapping, port_pool):
	list_of_node = set()
	list_of_edge = set()
	has_short_cut = False

	for node in comp2port_mapping:
		if len(comp2port_mapping[node]) == 2:
			list_of_node.add(port_pool[comp2port_mapping[node][0]])
			list_of_node.add(port_pool[comp2port_mapping[node][1]])
			list_of_edge.add((port_pool[comp2port_mapping[node][1]], port_pool[comp2port_mapping[node][0]]))

	for node in graph:
		root_node = find(node, parent)
		list_of_node.add(port_pool[node])
		list_of_node.add(port_pool[root_node])

		if node in same_device_mapping:
			cur_node_the_other_port = same_device_mapping[node]
			cur_node_the_other_port_root = find(cur_node_the_other_port, parent)
			if cur_node_the_other_port_root == root_node:
				has_short_cut = True

		if root_node != node:
			list_of_edge.add((port_pool[node], port_pool[root_node]))

		for nei in graph[node]:
			list_of_node.add(port_pool[nei])
			if nei != root_node:
				list_of_edge.add((port_pool[nei], port_pool[root_node]))

	return list(list_of_node), list(list_of_edge), has_short_cut


def convert_to_netlist(component_pool, port_pool, parent, comp2port_mapping):
	# for one component, find the two port
	# if one port is GND/VIN/VOUT, leave it don't need to find the root
	# if one port is normal port, then find the root, if the port equal to root then leave it, if the port is not same as root, change the port to root
	list_of_node = set()
	list_of_edge = set()

	for idx, comp in enumerate(component_pool):
		list_of_node.add(comp)
		for port in comp2port_mapping[idx]:
			port_root = find(port, parent)
			if port_root in [0, 1, 2]:
				list_of_node.add(port_pool[port_root])
				list_of_node.add(port_root)
				list_of_edge.add((comp, port_root))
				list_of_edge.add((port_pool[port_root], port_root))
			else:
				list_of_node.add(port_root)
				list_of_edge.add((comp, port_root))

	return list(list_of_node), list(list_of_edge)


#
class TopoGenState(uct.State):
	def __init__(self, init=False):
		if init:
			self.num_component = 0
			self.component_pool = ['VIN', 'VOUT', "GND"]
			self.port_pool = ['VIN', 'VOUT', "GND"]
			self.count_map = {"FET-A": 0, "FET-B": 0, "capacitor": 0, "inductor": 0}
			self.comp2port_mapping = {0: [0], 1: [1],
									  2: [2]}  # key is the idx in component pool, value is idx in port pool
			self.port2comp_mapping = {0: 0, 1: 1, 2: 2}

			self.port_2_idx = {'VIN': 0, 'VOUT': 1, "GND": 2}
			self.idx_2_port = {0: 'VIN', 1: 'VOUT', 2: "GND"}
			self.same_device_mapping = {}
			self.graph = collections.defaultdict(set)
			self.parent = None
			self.step = 0
		# self.actVect = []

	def init_disjoint_set(self):
		print('called', 'init_disjoint_set')
		self.parent = list(range(len(self.port_pool)))
		print('after init', self.parent)

	def equal(self, state):
		if isinstance(state, TopoGenState):
			return self.component_pool == state.component_pool and \
				   self.port_pool == state.port_pool and \
				   self.num_component == state.num_component and \
				   self.count_map == state.count_map and \
				   self.comp2port_mapping == state.comp2port_mapping and \
				   self.port2comp_mapping == state.port2comp_mapping and \
				   self.port_2_idx == state.port_2_idx and \
				   self.idx_2_port == state.idx_2_port and \
				   self.same_device_mapping == state.same_device_mapping and \
				   self.graph == state.graph and \
				   self.step == state.step and \
				   self.parent == state.parent
		# self.actVect == state.actVect
		return False

	def get_edges(self):
		edges = []
		for key, vals in self.graph.items():
			for v in vals:
				edges.append((self.idx_2_port[key], self.idx_2_port[v]))
		return edges

	def duplicate(self):
		return deepcopy(self)

	def print(self):
		print('component_pool: {} \nport_pool: {}\nstep: {}'.format(self.component_pool, self.port_pool, self.step))

	def get_node_num(self):
		return len(self.component_pool) - 3

	def get_edge_num(self):
		edge_num = 0
		for key, val in self.graph.items():
			edge_num += len(val)
		return edge_num / 2

	def visualize(self, steps, title=None):
		list_of_node, list_of_edge, has_short_cut = convert_graph(self.graph, self.comp2port_mapping, self.parent,
																  self.same_device_mapping, self.port_pool)
		# G = nx.Graph()
		# G.add_nodes_from((list_of_node))
		# G.add_edges_from(list_of_edge)
		list_of_node, list_of_edge = convert_to_netlist(self.component_pool, self.port_pool, self.parent,
														self.comp2port_mapping)
		T = nx.Graph()
		T.add_nodes_from((list_of_node))
		T.add_edges_from(list_of_edge)
		if bool(title):
			print('title', title)
			plt.title(title)
		nx.draw(T, with_labels=True)

		plt.savefig("./plots/step" + str(steps) + '-plot.jpg')
		plt.close()

	# plt.show()


class TopoGenAction(uct.SimAction):
	def __init__(self, type, value):
		self.type = type
		self.value = value

	def duplicate(self):
		other = TopoGenAction(self.type, self.value)
		return other

	def print(self):
		print(' ({}, {})'.format(self.type, self.value))

	def equal(self, other):
		if isinstance(other, TopoGenAction):
			return other.type == self.type and self.value == self.value
		return False


class TopoGenSimulator(uct.Simulator):
	def __init__(self, target):
		self.target = target
		self.target_edges = None
		if target:
			self.target_edges = target.get_edges()

		self.node_reward = 1.0
		self.node_penalty = -1
		self.edge_reward = 1.0
		self.edge_penalty = -1
		self.basic_components = ["FET-A", "FET-B", "capacitor", "inductor"]
		self.reward = -100
		self.current = TopoGenState(init=True)

		# move to state
		# self.step = 0
		self.actVect = []

		self.update_action_set()

	def setState(self, state):
		self.current = state.duplicate()
		self.update_action_set()

	def getState(self):
		return self.current

	def finish_node_set(self):
		self.current.init_disjoint_set()

	# tested
	def add_node(self, node_id):
		# if self.current.num_component >= self.target.num_component:
		#     print('Error: Node action should not be able.')
		count = str(self.current.count_map[self.basic_components[node_id]])
		self.current.count_map[self.basic_components[node_id]] += 1
		component = self.basic_components[node_id] + '-' + count
		self.current.component_pool.append(component)
		idx_component_in_pool = len(self.current.component_pool) - 1
		self.current.port_pool.append(component + '-left')
		self.current.port_pool.append(component + '-right')
		self.current.port_2_idx[component + '-left'] = len(self.current.port_2_idx)
		self.current.port_2_idx[component + '-right'] = len(self.current.port_2_idx)
		self.current.comp2port_mapping[idx_component_in_pool] = [self.current.port_2_idx[component + '-left'],
																 self.current.port_2_idx[component + '-right']]
		self.current.port2comp_mapping[self.current.port_2_idx[component + '-left']] = idx_component_in_pool
		self.current.port2comp_mapping[self.current.port_2_idx[component + '-right']] = idx_component_in_pool
		self.current.idx_2_port[len(self.current.idx_2_port)] = component + '-left'
		self.current.idx_2_port[len(self.current.idx_2_port)] = component + '-right'
		self.current.same_device_mapping[self.current.port_2_idx[component + '-left']] = self.current.port_2_idx[
			component + '-right']
		self.current.same_device_mapping[self.current.port_2_idx[component + '-right']] = self.current.port_2_idx[
			component + '-left']
		self.current.num_component += 1

	# tested
	def add_edge(self, edge):
		if edge[0] < 0:
			return
		print('edge', edge)
		self.current.graph[edge[0]].add(edge[1])
		self.current.graph[edge[1]].add(edge[0])
		print('parent value', self.current.parent)
		union(edge[0], edge[1], self.current.parent)
		return

	#
	def reward_on_edge(self, edge):
		self.reward = 0
		if edge[0] < 0:
			return

		edge_name = (self.current.idx_2_port[edge[0]], self.current.idx_2_port[edge[1]])
		if edge_name in self.target_edges:
			self.reward = self.edge_reward
		else:
			self.reward = self.edge_penalty
		return

	# compare to target to compute rewards and next actions
	def reward_on_node(self, node_id):
		node_name = self.basic_components[node_id]
		self.reward = 0
		if self.current.count_map[node_name] <= self.target.count_map[node_name]:
			self.reward = self.node_reward
		else:
			self.reward = self.node_penalty
		return

	#
	def update_action_set(self):
		if not self.target:
			return
		if len(self.current.component_pool) < len(self.target.component_pool):
			self.actVect = [TopoGenAction('node', i) for i in range(len(self.basic_components))]
		else:
			# print('edge branch', self.current.step)
			# print('current.component_pool', self.current.component_pool)
			# print('target.component_pool', self.target.component_pool)
			self.actVect.clear()
			e1 = self.current.step - (len(self.current.component_pool) - 3)
			e1 %= len(self.current.port_pool)
			# if e1 >= len(self.current.port_pool):
			#     return
			# all the available edge set with e1 as a node
			e2_pool = list(range(len(self.current.port_pool)))
			random.shuffle(e2_pool)

			for e2 in e2_pool:
				# the same port
				if e1 == e2:
					continue
				# from the same device
				if e2 in self.current.same_device_mapping and \
						e1 == self.current.same_device_mapping[e2]:
					continue
				# existing edges
				if (e1 in self.current.graph and e2 in self.current.graph[e1]) or \
						(e2 in self.current.graph and e1 in self.current.graph[e2]):
					continue
				# disjoint set
				e1_root = find(e1, self.current.parent)
				e2_root = find(e2, self.current.parent)
				vin_root = find(0, self.current.parent)
				vout_root = find(1, self.current.parent)
				gnd_root = find(2, self.current.parent)
				special_roots = [vin_root, vout_root, gnd_root]
				if e1_root in special_roots and e2_root in special_roots:
					continue
				self.actVect.append(TopoGenAction('edge', [e1, e2]))
			if len(self.actVect) > 0:
				if e1 in self.current.graph and len(self.current.graph[e1]) > 0:
					self.actVect.append(TopoGenAction('edge', [-1, -1]))
		return

	def act(self, action):
		if action.type == 'node':
			self.add_node(action.value)
			self.reward_on_node(action.value)
		elif action.type == 'edge':
			print('before edge action')
			self.current.print()
			self.add_edge(action.value)
			self.reward_on_edge(action.value)
		else:
			print('Error: Unsupported Action Type!')

		if len(self.current.component_pool) == len(self.target.component_pool) and \
				not bool(self.current.parent):
			self.finish_node_set()

		self.current.step += 1
		self.update_action_set()

		return self.reward

	def getActions(self):
		return self.actVect

	def isTerminal(self):
		# check equals to the target or all nodes are visited
		if self.current.step - (len(self.current.component_pool) - 3) >= len(self.current.port_pool) or \
				len(self.actVect) == 0:
			return True
		return set(self.current.component_pool) == set(self.target.component_pool) and \
			   set(self.current.port_pool) == set(self.target.port_pool) and \
			   set(self.current.get_edges()) == set(self.target.get_edges())


def construct_target_v1():
	simulator = TopoGenSimulator(None)
	# ["FET-A", "FET-B", "capacitor", "inductor"]
	simulator.add_node(0)
	simulator.add_node(1)
	simulator.add_node(3)
	simulator.current.init_disjoint_set()
	# edges:
	edges = [['VIN', 'FET-A-0-left'], ['FET-A-0-right', 'FET-B-0-left'], ['FET-B-0-right', 'GND'],
			 ['inductor-0-left', 'FET-A-0-right'], ['inductor-0-right', 'VOUT']]
	for edge in edges:
		p1, p2 = simulator.current.port_2_idx[edge[0]], simulator.current.port_2_idx[edge[1]]
		simulator.add_edge([p1, p2])
	return simulator.getState()


def construct_target_v2():
	simulator = TopoGenSimulator(None)
	# ["FET-A", "FET-B", "capacitor", "inductor"]
	simulator.add_node(0)
	simulator.add_node(1)
	simulator.add_node(3)
	simulator.current.init_disjoint_set()
	# edges:
	edges = [['VIN', 'FET-A-0-left'], ['FET-A-0-right', 'FET-B-0-left'], ['FET-B-0-right', 'GND'],
			 ['inductor-0-left', 'FET-A-0-right'], ['inductor-0-right', 'VOUT']]
	for edge in edges:
		p1, p2 = simulator.current.port_2_idx[edge[0]], simulator.current.port_2_idx[edge[1]]
		simulator.add_edge([p1, p2])
	return simulator.getState()


if __name__ == '__main__':
	# simple_topo_demo()
	target = construct_target_v1()
	print('-------------target--------------------')
	target.print()
	print('-------------target--------------------')
	# creat folder or clear the previous plots
	folder = "./plots"
	isExists = os.path.exists(folder)
	if not isExists:
		os.makedirs(folder)
	else:
		uctViz.delAllFiles(folder)
	# finish clearance
	target.visualize('target topology')
	target_edges = target.get_edges()

	depthList = [2]
	trajectory = [10]
	numGames = 1
	Vizstep = [1]  # the list of the steps which we want to see the tree structure


	def print_missing_edges(cur_edges, target_edges):
		more = [edge for edge in cur_edges if edge not in target_edges]
		less = [edge for edge in target_edges if edge not in cur_edges]
		print('no need edges: ', more)
		print('missing edges: ', less)
		return


	# (self, _sim, _maxDepth, _numRuns, _ucbScalar, _gamma, _leafValue, _endEpisodeValue):
	for max_depth in depthList:
		for num_Runs in trajectory:
			print(max_depth, ",", num_Runs)
			avgsteps = 0

			for j in range(0, numGames):
				sim = TopoGenSimulator(target)
				uct_simulator = TopoGenSimulator(target)
				uctTree = uct.UCTPlanner(uct_simulator, max_depth, num_Runs, 1, 0.95, 0, 0)
				r = 0
				sim.getState().print()
				step = 0
				while not sim.isTerminal():
					uctTree.setRootNode(sim.getState(), sim.getActions(), r, sim.isTerminal())
					nodeList = uctTree.plan()
					print("step ", str(step), ":nodeList len:", len(nodeList))
					# viz start
					if step in Vizstep:
						folder = "./viz" + str(step)
						isExists = os.path.exists(folder)
						if not isExists:
							os.makedirs(folder)
						else:
							uctViz.delAllFiles(folder)
						treeviz = uctViz.TreeGraph(nodeList)
						treeviz.drawAll(uctTree, folder)
					# viz finished
					# return the action with the highest reward
					action = uctTree.getAction()
					print("{}-action:".format(step), end='')
					action.print()
					print("{}-state:".format(step), end='')
					r = sim.act(action)
					sim.getState().print()
					cur_edges = sim.getState().get_edges()
					print_missing_edges(cur_edges, target_edges)

					if sim.getState().parent:
						if action.type == 'node':
							act_str = 'adding node {}'.format(sim.current.component_pool[action.value])
						else:
							if action.value[1] < 0 or action.value[0] < 0:
								act_str = 'skip connecting'
							else:
								act_str = 'connecting {} and {}'.format(sim.current.idx_2_port[action.value[0]],
																		sim.current.idx_2_port[action.value[1]])
						# add step for output different file name
						sim.getState().visualize(step, act_str)
					print("{}-reward:".format(step), r)
					step += 1

			avgsteps = avgsteps / numGames
			print(str(max_depth) + "," + str(num_Runs) + "," + str(avgsteps) + "\n")

		# print("max_depth",max_depth,",",num_Runs,":",avgsteps)

		# avgstep_list.append(avgsteps)
# endtime = datetime.datetime.now()
# print("execute time: ", (endtime - starttime).seconds, "s")
# # avgtimes+=(endtime - starttime).seconds
# fo.close()
# print("avgtimes:",avgtimes/20)
