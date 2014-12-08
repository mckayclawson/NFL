#Data Mining Project 4

import csv
import random
import math
import operator

#loads the csv files
def loadDataset(filename, split, trainingSet=[] , testSet=[]):
	with open(filename, 'rb') as csvfile:
	    lines = csv.reader(csvfile)
	    dataset = list(lines)
	    for x in range(len(dataset)-1):
	        #convert columns from str to float
			for y in [3,5,6,7,8,9,10,11,12,13,21,22,27]:
				#normalize the age value to the average age of a starting NFL QB(28)
			    if y == 3:
			    	dataset[x][y] = int(dataset[x][y]) - 28
			    	#convert integer fields to integers
			    else if y == 5 or y == 7 or y == 8 or y == 10 or y == 11 or y == 12 or y == 22 or y == 27:
			    	dataset[x][y] = int(dataset[x][y])
			    #convert the QBR to float
			    else if y == 21:
			    	dataset[x][y] = float(dataset[x][y])
			    #convert percentages from strings to floats
			    else if y == 9 or y == 11:
			    	tempStr = dataset[x][y].strip('%')
			    	tempFloat = float(tempStr)
			    	tempResult = tempFloat/100
			    	dataset[x][y] = tempResult
			    #convert QB-Record into win loss ratio
			    else if y == 6:
			    	tempStr = dataset[x][y].split('-')
			    	winPerc = float(tempStr[0])/(float(tempStr[0]) + float(tempStr[1]))
			    	dataset[x][y] = winPerc
			    #convert the avg-pick number into a round number for use as the target variable
			    else if y == 29:
			    	tempInt = int(dataset[x][y])
			    	dataset[x][y] = tempInt/10

	        if random.random() < split:
	            trainingSet.append(dataset[x])
	        else:
	            testSet.append(dataset[x])

#function to calculate distance
def euclideanDistance(instance1, instance2, length):
	distance = 0.0
	#print instance1, instance2
	#again selecting colums 
	for x in [3,5,6,7,8,9,10,11,12,13,21,22,27,29]:
		distance += pow((instance1[x] - instance2[x]), 2)
	return math.sqrt(distance)

#iteratively tests using euclidean distance
def getNeighbors(trainingSet, testInstance, k):
	distances = []
	length = len(testInstance)-1
	for x in range(len(trainingSet)):
		dist = euclideanDistance(testInstance, trainingSet[x], length)
		distances.append((trainingSet[x], dist))
	distances.sort(key=operator.itemgetter(1))
	neighbors = []
	for x in range(k):
		neighbors.append(distances[x][0])
	return neighbors

#find the closest neighbors and predicts the score
def getResponse(neighbors):
	avg = 0.0
	for x in range(len(neighbors)):
		try:
			#takes the average of all neighbors as the predicted score
			response = float(neighbors[x][29])
			avg += response
		except ValueError:
			response += 0
	return avg/len(neighbors)


#figures out the accuracy of the predictions
def getAccuracy(testSet, predictions):
	correct = 0
	for x in range(len(testSet)):
		try:
			if((float(testSet[x][10]) < 76.5 and predictions[x] < 76.5) or (float(testSet[x][10]) >= 76.5 and predictions[x] >= 76.5)):
				correct += 1
		except ValueError:
			correct = correct
	return (correct/float(len(testSet))) * 100.0

	
def main():
	# prepare data
	trainingSet=[]
	testSet=[]
	split = 0.67
	loadDataset('years_2014_passing_passing.csv', split, trainingSet, testSet)
	print 'Train set: ' + repr(len(trainingSet))
	print 'Test set: ' + repr(len(testSet))
	# generate predictions
	predictions=[]
	k = 3
	error = 0.0
	

main()
