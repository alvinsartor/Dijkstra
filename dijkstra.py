import random
import sys

# --- NODE CLASS --- #
class Node:

	#initializing function
	def __init__(self, name):
		self.name = name
		self.edges = []
		self.isSource = False
		self.father = None
		self.stima = sys.maxint
		self.hasBeenChecked = False
	
	#return the edges of the node
	def getEdges(self): return self.edges			
	#used internally to create a return-connection
	def addBack(self,node, weight): self.edges.append(Edge(node, weight))
	#create a connection self-node and node-self (using addBack())
	def addEdge(self,node, weight): 
		self.edges.append(Edge(node, weight))
		node.addBack(self, weight)
	
	#return TRUE if it is connected to the node passed as argument
	def isConnectedTo(self, node):
		edg = self.edges
		for e in edg:
			if e.node.name == node.name:
				return True
		return False
	
	#return the father of the node. Used to find paths
	def getFather(self): return self.father
	#initialize the node so the RELAX() function can be performed on it
	def initialize(self):
		self.stima = sys.maxint
		self.hasBeenChecked = False
		self.isSource = False
		self.father = None
	
	#Execute a Relax on the adjacents units, changing their value if necessary
	def internalRelax(self, node, estimation):
		self.hasBeenChecked = True
		self.stima = estimation
		self.father = node
		for e in self.edges:
			if (e.node.hasBeenChecked == False or e.node.stima > self.stima + e.weight):
				e.node.internalRelax(self, self.stima + e.weight)			
	
	#Execute a Relax on the source. This will propagate it to the neighbours
	def relax(self):		
		self.hasBeenChecked = True
		self.isSource = True
		self.father = None
		self.stima = 0
		for e in self.edges:
			if (e.node.hasBeenChecked == False or e.node.stima > self.stima + e.weight):			
				e.node.internalRelax(self, self.stima + e.weight)		
	
	#return a string containing the specifications of the node
	def toString(self):
		conn = ''
		for e in self.edges:
			conn += e.toString()
		return 'Node: ' + self.name + '     ' + 'Connections: ' + conn

# --- EDGE CLASS --- #
class Edge:	

	#constructor of the Edge class
	def __init__(self, node, w):
		self.node = node
		self.weight = w
	
	#return a string containing the specifications of the edge
	def toString(self):
		return '[' + self.node.name + ':' + str(self.weight) + ']'


# --- GRAPH FUNCTIONS --- #

#create a graph randomly using the parameters passed as argument
def createRandomGraph(dim, connex, minW, maxW):
	graph = []
	for i in range(dim):
		graph.append(Node('n' + str(i)))
	
	k = 0
	while k < connex:
		n1 = graph[random.randint(0,dim - 1)]
		n2 = graph[random.randint(0,dim - 1)]
		if n1.name != n2.name and n1.isConnectedTo(n2) == False:
			n1.addEdge(n2, random.randint(minW, maxW))
			k += 1
	return graph

#print a graph
def printGraph(g):
	print('\n')
	for n in g: 
		print(n.toString())

#calls the initialize() function in all the nodes of the graph
def init_SS(g):
	for n in g:
		n.initialize()
		
#given a starting point (S), the function prints all the paths from the
#	other nodes to S
def pathFrom(g, s):
	init_SS(g)
	s.relax()
	for n in g:
		path = []
		k = n
		path.append(k)
		while k.getFather() != None:			
			k = k.getFather()
			path.append(k)
		parcialResult = ''
		for node in path:
			parcialResult += '->' + node.name
		print parcialResult

   


g = createRandomGraph(20, 20, 1, 99)
printGraph(g)
pathFrom(g, g[0])






