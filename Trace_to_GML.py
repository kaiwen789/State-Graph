import sys
import re

class Node:
	def __init__(self,ID):
		self.descendant = []
		self.ID = ID
	def add_descendant(self,dsc):
		if dsc not in self.descendant:
			self.descendant.append(dsc)
	def get_ID(self):
		return self.ID
	def get_descendant(self):
		return self.descendant

class Graph:
	def __init__(self):
		self.NodeList = {}
	def add_node(self,ID):
		if ID not in self.NodeList:
			new_node = Node(ID)
			self.NodeList[ID] = new_node
	def add_edge(self,ID_ASC,ID_DSC):
		if len(ID_ASC) != 0:
			self.NodeList[ID_ASC].add_descendant(self.NodeList[ID_DSC])
	def get_node_list(self):
		return self.NodeList


if len(sys.argv)!=4:
	print('\nUsage: python Trace_to_GML.py [trace file] [element list] [output name]')
	print('  [Trace file] should be the same format as the input of model checker (mode 2)')
	print('  [Element list] is a list of elements of interest, each of them seperate by space')
	print('  [Output name] should include .gml\n')
	sys.exit(0)

TraceFile = open(sys.argv[1],'r')
ElementFile = open(sys.argv[2],'r')

# Declare Important Variables
ElementList = []
ElementListID = []
state_graph = Graph()
prev_node_ID = ''

# Extract the elements of interest
line = ElementFile.readline()
line = line.strip()
line = ' '.join(line.split())
ElementList = re.split(' ',line)
ElementFile.close()

# Extract the position of the elements of interest
for line in TraceFile:
	if line.find('# time') != -1:
		line = line[line.find('time')+1:]
		line = line[line.find(' ')+1:]
		line = line.strip()
		TotalList = re.split(' ',line)

		ElementListID = [TotalList.index(element) for element in ElementList]
		break

# Record the dependency of the graph
for line in TraceFile:
	line = line.strip()
	line = ' '.join(line.split())
	SnapShot = re.split(' ',line)

	time = SnapShot[0]
	if time == str(0):
		prev_node_ID = ''
	SnapShot = SnapShot[1:]
	SnapShot = [SnapShot[ID] for ID in ElementListID]
	SnapShot = ''.join(SnapShot)
	
	state_graph.add_node(SnapShot)
	state_graph.add_edge(prev_node_ID,SnapShot)

	prev_node_ID = SnapShot

# Test Script
# l = state_graph.get_node_list()
# for node_key in l:
# 	print(l[node_key].get_ID())
# 	ll = [dsc.get_ID() for dsc in l[node_key].get_descendant()]
# 	print(ll)

TraceFile.close()

# Generate GML file
# graph [
# directed 1
# node [ id 1100110110 label "1100110110" graphics [ fill	"#FF3300" w 40 h 30 x 94 y 57 type "ellipse" ]]
# edge [ source 1100110110 target 1010110010  graphics [ fill	"#000000" targetArrow "delta" ]]
# ]

gmlFile = open(sys.argv[3],'w')
gmlFile.write('graph [\ndirected 1\n')

# Draw nodes
for node_key in state_graph.get_node_list():
	ID = state_graph.get_node_list()[node_key].get_ID()
	gmlFile.write('node [ id ' + ID + ' label \"' + ID + '\" graphics [ fill	"#FF3300" w 80 h 30 x 0 y 0 type "ellipse" ]]\n')

# Draw Edges
for node_key in state_graph.get_node_list():
	for target in state_graph.get_node_list()[node_key].get_descendant():
		ID = state_graph.get_node_list()[node_key].get_ID()
		gmlFile.write('edge [ source ' + ID + ' target ' + target.get_ID() + '  graphics [ fill	"#000000" targetArrow "delta" ]]\n')

gmlFile.write(']')
gmlFile.close()