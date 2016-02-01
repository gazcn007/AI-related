import json
from pprint import pprint
from byteify import byteify

with open('brussels_metro_v2.json') as data_file:    
    data = json.load(data_file)

#lets byteify our input json input so it gets rid of u's in front of all attributes
#the module for converting encoding is in byteify.py
data=byteify(data)

#modules for parsing a metro and apply blind search algorithm are:
#i. Breadth first search
#ii. Uniform cost search
#iii. Depth first search
#iv. Iterative deepening

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#Now because of that the cost of a transition operator along lines #1, #2 and #3 (the older lines) 
# is twice the cost of a transition operator along lines #4, #5, #6 (the new lines).
#   We need to improve our program a bit:
#      1. Fetch line info
#	   2. Record Costs
#      3. Find the cheapest way to travel so we have low costs 
# 			->(this can be greedily assumed the bigger the line number the node has, the cheaper it is to travel)
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

#Breath First Search 
def BFS(input_data,start,end):
	#breath search can be implemented by queues
	counter=0;
	array=[]
	#change the array is now of duples, 
	#[i][0] is node name, 
	#[i][1] is line that is cheapest to get to node
	#[i][2] is the parent that gets to the node by line [i][1]
	#initial the array with start node, and line that can
	array.append((start,-1,None))
	findstation=0;
	# ! add a cost counter
	cost=0;
	while (counter<len(array) and findstation==0):
		for station in input_data['stations']:
			if station['name']==array[counter][0]:
				for neighbour in station['neighbours']:
					if not any(neighbour['name'] in tuples for tuples in array) or neighbour['name']==array[-1][0]:
						if neighbour['name']==end and neighbour['name']!=array[-1][0]:
							#note since for the station 'Roi Baudouin', there is one line to get there from
							# its neighbors, so we don't have to compare costs
							array.append((neighbour['name'],neighbour['line'],station['name']))
							findstation=1
						elif neighbour['name']==end and neighbour['name']==array[-1][0]:
							#note since for the station 'Roi Baudouin', there is one line to get there from
							# its neighbors, so we don't have to compare costs
							if (neighbour['line']>array[-1][1]):
								array[-1]=(neighbour['name'],neighbour['line'],station['name'])
						else:
							if findstation==1:
								break
							elif neighbour['name']!=array[-1][0]:
								array.append((neighbour['name'],neighbour['line'],station['name']))
							else:
								if (neighbour['line']>array[-1][1]):
									array[-1]=(neighbour['name'],neighbour['line'],station['name'])
				break;
		counter+=1
	#cost count:
	cost=0
	for node in array:
		if node[1] in [1,2,3]:
			cost=cost+2
		elif node[1] in [4,5,6]:
			cost=cost+1
		else:
			cost=cost+0
	return array,cost

#Uniform Cost Search
def UCS(input_data,start,end):
	#UCS can be achieved by tuple array
	#1st attribute name of the station node 
	#2nd attribute for total cost of getting to the station node from starting point
	#3nd attribute for parent of the station node
	#records [i][0] is name of node, [i][1] is current sum cost, [i][2] records the parent of this node
	#with addition [i][3] is the line that is cheapest to get to the node from parent
	records=[]
	records.append((start,0,None,-1))
	#shortest nodes array collects nodes that are confirmed to have found shortest path to it
	shortest_nodes=[]
	#visited array collects nodes that are visited by the algorithm
	visited=[]
	visited.append(start)
	#we can sort a tuples array by sorted([('abc', 121),('abc', 231),('abc', 148), ('abc',221)], key=lambda x: x[1])
	findstation=0;
	while(findstation==0):
		shortest_nodes.append(records[0])
		#when we know we have got a cheapest path to travel to our destination, we stop
		if records[0][0]==end:
			break
		else:
			for station in input_data['stations']:
				if station['name']==records[0][0]:
					for neighbour in station['neighbours']:
						#check if our records and visited array have this station's neighbour or not
						#if so we are not adding it into our records and visited array
						if neighbour['name'] not in visited or neighbour['name']==visited[-1]:
							#since we just need to blind run algorithm until we find the node
							#we write an if statement here to stop the algorithm when we find the destination
							#usually it should not stop, because even if it has been find, we are not sure if it has the cheapest cost to travel there
							if neighbour['name']!=visited[-1]:
								records.append((neighbour['name'],records[0][1]+2,records[0][0],neighbour['line']))
								visited.append(neighbour['name'])
							#if we find a station that is the ending point
							#we can append it to visited[], return visited[], break the loop and we are done
							#by far, we just need to blindly find the destination, so we can stop here
							#if we are evaluating the shortest path, we will need to run more step until the node has a cheapest path.
							#(at head of the list after it is being sorted by cost sum)
							elif neighbour['line'] in [4,5,6]:
								records[-1]=((neighbour['name'],records[0][1]+2,records[0][0],neighbour['line']))
								visited.append(neighbour['name'])
					break;
		records.remove(records[0])
		records=sorted(records, key=lambda x: x[1])
	cost=0
	for node in shortest_nodes:
		if node[3] in [1,2,3]:
			cost=cost+2
		elif node[3] in [4,5,6]:
			cost=cost+1
		else:
			cost=cost+0
	return shortest_nodes,cost

#Depth First Search 
def DFS(input_data,start,end):
	visited=[]
	#DFS can be quickly achieved by stacks
	stack=[]
	stack.append((start,-1,None))
	findstation=0;
	while(len(stack)!=0 and findstation==0):
		currentStation=stack[-1];
		visited.append(currentStation)
		insertionPoint=len(stack)-1
		for station in input_data['stations']:
			if station['name']==currentStation[0]:
				for neighbour in station['neighbours']:
					if not any(neighbour['name'] in tuples for tuples in visited) and (not any(neighbour['name'] in tuples for tuples in stack) or neighbour['name']==stack[insertionPoint][0]):
						if neighbour['name']!=stack[insertionPoint][0]:
							#if we find the station, break the while loop, and return our visited path
							if neighbour['name']==end:
								visited.append((neighbour['name'],neighbour['line'],station['name']))
								stack.insert(insertionPoint,(neighbour['name'],neighbour['line'],station['name']))
								findstation=1
							else:
								#since the question asked us to do it clockwise from 12 o'clock, so we need to push into our stack in
								#the same order how json file is like
								stack.insert(insertionPoint,(neighbour['name'],neighbour['line'],station['name']))
						else:
							if neighbour['line'] in [4,5,6]:
								stack[insertionPoint]=((neighbour['name'],neighbour['line'],station['name']))
				break;
		stack.pop()
	cost=0
	for node in visited:
		if node[1] in [1,2,3]:
			cost=cost+2
		elif node[1] in [4,5,6]:
			cost=cost+1
		else:
			cost=cost+0
	return visited,cost

#Iterative Deepening Search
def IDS(input_data,start,end):
	#Iterative Deepening Search can be achieved by using 2D array [[]]
	visited=[]
	sameDepth=[] #this is a collection of station nodes that have teh same depth
	findstation=0
	sameDepth.append((start,-1,None))
	visited.append(sameDepth)
	visited_nodes=[]
	visited_nodes.append(start)
	counter=0
	while(counter<=len(visited) and findstation==0):

		sameDepth=[] 
		for node in visited[counter]:
			for station in input_data['stations']:
				if station['name']==node[0]:
					for neighbour in station['neighbours']:
						#note to myself : arranging conditions matters
						if neighbour['name'] not in visited_nodes or sameDepth==[] or neighbour['name'] == sameDepth[-1][0]:
							if sameDepth==[] or neighbour['name']!=sameDepth[-1][0]:
								#if we find the station, break the while loop, and return our visited path
								if neighbour['name']==end:
									sameDepth.append((neighbour['name'],neighbour['line'],station['name']))
									visited_nodes.append(neighbour['name'])
									findstation=1
								else:
									sameDepth.append((neighbour['name'],neighbour['line'],station['name']))
									visited_nodes.append(neighbour['name'])
							else:
								if neighbour['line'] in [4,5,6]:
									sameDepth[-1]=((neighbour['name'],neighbour['line'],station['name']))
					break
		counter+=1
		visited.append(sameDepth)
	cost=0
	for level in visited:
		for node in level:
			if node[1] in [1,2,3]:
				cost=cost+2
			elif node[1] in [4,5,6]:
				cost=cost+1
			else:
				cost=cost+0
	return visited,cost

print 'Breath First Search:'
array,cost=BFS(data,'Rogier','Roi Baudouin')
print array
print 'Cost:'
print cost

print 'Uniform Cost Search:'
array,cost=UCS(data,'Rogier','Roi Baudouin')
print array
print 'Cost:'
print cost

print 'Depth First Search :'
array,cost=DFS(data,'Rogier','Roi Baudouin')
print array
print 'Cost:'
print cost

print 'Iterative Deepening Search: '
array,cost=IDS(data,'Rogier','Roi Baudouin')
print array
print 'Cost:'
print cost

