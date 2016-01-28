import json
from pprint import pprint

with open('brussels_metro_v2.json') as data_file:    
    data = json.load(data_file)

#a short and simple recursive function will convert any decoded 
#JSON object from using unicode strings in the assignment file to UTF-8-encoded byte strings
def byteify(input):
    if isinstance(input, dict):
        return {byteify(key): byteify(value)
                for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input
print(data)
data=byteify(data)
#modules

#Breath First Search 
def BFS(input_data,start,end):
	#breath search can be implemented by queues
	counter=0;
	array=[]
	array.append(start)
	findstation=0;
	while (counter<len(array) and findstation==0):
		for station in input_data['stations']:
			if station['name']==end:
				findstation=1;
				array.append(station['name'])
				break;
			elif station['name']==array[counter]:
				for neighbour in station['neighbours']:
					if neighbour['name'] not in array:
						array.append(neighbour['name'])
				break;
		counter+=1
	return array

#Deep First Search 
def DFS(input_data,start,end):
	visited=[]
	stack=[]
	stack.append(start)
	findstation=0;
	while(len(stack)!=0 and findstation==0):
		currentStation=stack.pop();
		visited.append(currentStation)
		for station in input_data['stations']:
			if station['name']==end:
				findstation=1;
				visited.append(station['name'])
				stack.append(station['name'])
				break;
			elif station['name']==currentStation:
				for neighbour in station['neighbours']:
					if neighbour['name'] not in visited and neighbour['name'] not in stack:
						stack.append(neighbour['name'])
				break;
	return visited

array=BFS(data,'Rogier','Roi Baudouin')
print array
print len(array)
array1=DFS(data,'Rogier','Roi Baudouin')
print array1
