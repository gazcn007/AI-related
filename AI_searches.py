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


#Breath First Search 
def BFS(input_data,start,end):
	#breath search can be implemented by queues
	counter=0;
	array=[]
	array.append(start)
	findstation=0;
	while (counter<len(array) and findstation==0):
		if array[counter]==end:
			findstation=1;
			break;
		else:
			for station in input_data['stations']:
				if station['name']==array[counter]:
					for neighbour in station['neighbours']:
						if neighbour['name'] not in array:
							if neighbour['name']==end:
								array.append(neighbour['name'])
								findstation=1
								break;
							else:
								array.append(neighbour['name'])
					break;
		counter+=1
	return array

#Uniform Cost Search
def UCS(input_data,start,end):
	#UCS can be achieved by tuple array
	#1st attribute name of the station node 
	#2nd attribute for total cost of getting to the station node from starting point
	#3nd attribute for parent of the station node
	#records [i][0] is name of node, [i][1] is current sum cost, [i][2] records the parent of this node
	records=[]
	records.append((start,0,None))
	print records[0][0]
	visited=[]
	#we can sort a tuples array by sorted([('abc', 121),('abc', 231),('abc', 148), ('abc',221)], key=lambda x: x[1])
	findstation=0;
	while(findstation==0):
		visited.append(records[0])
		for station in input_data['stations']:
			if station['name']==records[0][0]:
				for neighbour in station['neighbours']:
					#check if our records and visited array have this station's neighbour or not
					#if so we are not adding it into our records and visited array
					if neighbour['name'] not in visited and not any(neighbour['name'] in list for list in records):
						#if we find a station that is the ending point
						#we can append it to visited[], return visited[], break the loop and we are done
						#by far, we just need to blindly find the destination, so we can stop here
						#if we are evaluating the shortest path, we will need to run more step until the node has a cheapest path.
						#(at head of the list after it is being sorted by cost sum)
						if neighbour['name']==end:
							visited.append(neighbour['name'])
							findstation=1
							break;
						else:
							temp=(neighbour['name'],records[0][1]+1,records[0][0])
							records.append(temp)
				break;
		records.remove(records[0])
		records=sorted(records, key=lambda x: x[1])
	print visited

#Depth First Search 
def DFS(input_data,start,end):
	visited=[]
	#DFS can be quickly achieved by stacks
	stack=[]
	stack.append(start)
	findstation=0;
	while(len(stack)!=0 and findstation==0):
		currentStation=stack.pop();
		visited.append(currentStation)
		insertionPoint=len(stack)
		for station in input_data['stations']:
			if station['name']==currentStation:
				for neighbour in station['neighbours']:
					if neighbour['name'] not in visited and neighbour['name'] not in stack:
						#if we find the station, break the while loop, and return our visited path
						if neighbour['name']==end:
							visited.append(neighbour['name'])
							findstation=1
							break;
						else:
							#since the question asked us to do it clockwise from 12 o'clock, so we need to push into our stack in
							#the same order how json file is like
							stack.insert(insertionPoint,neighbour['name'])
				break;
	return visited

#Iterative Deepening Search
def IDS(input_data,start,end):
	#Iterative Deepening Search can be achieved by using 2D array [[]]
	visited=[]
	sameDepth=[] #this is a collection of station nodes that have teh same depth
	findstation=0
	sameDepth.append(start)
	visited.append(sameDepth)
	counter=0
	while(counter<=len(visited) and findstation==0):
		sameDepth=[]
		for node in visited[counter]:
			for station in input_data['stations']:
				if station['name']==node:
					for neighbour in station['neighbours']:
						if not any(neighbour['name'] in sublist for sublist in visited) and not(neighbour['name'] in sameDepth):
							#if we find the station, break the while loop, and return our visited path
							if neighbour['name']==end:
								sameDepth.append(neighbour['name'])
								findstation=1
								break;
							else:
								sameDepth.append(neighbour['name'])
					break
		counter+=1
		visited.append(sameDepth)
	return visited


array=BFS(data,'Rogier','Roi Baudouin')
print array
array1=DFS(data,'Rogier','Roi Baudouin')
print array1 
array2=IDS(data,'Rogier','Roi Baudouin')
print array2
print UCS(data,'Rogier','Roi Baudouin')
if any(121 in list for list in (sorted([('abc', 121),('abc', 231),('abc', 148), ('abc',221)], key=lambda x: x[1]))):
	print 'succus'