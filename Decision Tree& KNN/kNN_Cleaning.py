__author__ = 'Nisha Bhanushali'
# Name: Nisha Bhanushali
# Date: 10/07/2016
# This library is imported because it consists of methods which help to read the csv files
import csv
# This library is imprted to perform the square operation
import math

def readFile(filename):
     """
     This method reads the csv file and then calls the method computekNN().
     This method forms the clusters using the kNN algorithm.
     :return:
     """
     f=open(filename,'rt')
     try:
         reader=csv.reader(f)                          #This function is responsible for reading the file
         data=[]
         count=0
         for row in reader:
             if(count!=0):
                row_append=[float(i) for i in row]
                data.append(row_append)
             count+=1
     finally:
         f.close()
     return data


def computeKNN(traindata):
    """
    This method is responsible to perform the
    kNN clustering algorithm on the training data.
    It takes the record of the training data and
    finds the k nearest distances in the training data
    and then using the majority votes finds the value
    of each record. The best value of k is found using
    the minimum misclassification rate
    :param traindata:     the training dataset
    :return:
    """
    maxDist=1000

    bestMisclas=100000           #This the the best misclassfication rate to find best k value
    bestK=0                      #The best value of K for clustering
    bestLabels=[]                #The labels of the values on the training data
    for K in range(2,31):
        list_labels=[]
        for iterx in range(len(traindata)):
            list_dist=[]
            list_neighbor=[]
            for iter in range(len(traindata)):
                    if(iterx!=iter):
                        dist=computeDist(traindata[iterx],traindata[iter])
                        list_dist.append(dist)
                        list_neighbor.append(iter)
            list_dist,list_neighbor=zip(*sorted(zip(list_dist,list_neighbor)))
            nearestNeighbor=[]

            # Finding out K nearest neighbors
            for count in range(K):
                nearestNeighbor.append(list_neighbor[count])

            # Finding out the majority votes
            count_0=0
            count_1=0
            for neighbor in nearestNeighbor:
                # print(traindata[neighbor])
                if(traindata[neighbor][3]==0.0):
                    count_0=count_0+1
                elif(traindata[neighbor][3]==1.0):
                    count_1=count_1+1

            # Checking the majority count
            if(count_0>count_1):
                label=0
                list_labels.append(label)
            else:
                label=1
                list_labels.append(label)

        misClas=0
        # Computes the misclassification rate for the value of K
        for index in range(len(traindata)):
            if(list_labels[index]!=traindata[index][3]):
                misClas=misClas+1
        # Checks for the best misclassification value
        if(misClas<bestMisclas):
            bestMisclas=misClas
            bestK=K
            bestLabels=list_labels

        # break
    print('Best K : ',bestK)
    print('Best Labels : ',bestLabels)
    print('Best Misclassification Rate : ',bestMisclas)
    return bestLabels

def computeDist(trainx,trainy):
    """
    This method is responsible for computing the distance
    between two records.
    :param trainx:       record 1 of training data
    :param trainy:       record 2 of training data
    :return: the distance of the training data
    """
    dist=0
    for iter in range(len(trainx)-1):
        dist+=math.pow(float(trainx[iter])-float(trainy[iter]),2)
    total_dist=math.sqrt(dist)
    return total_dist

def maxData(trainingData, iter):
    """
    Maximum value in the column of the training data
    :param trainingData:     training data set
    :param iter:       column number
    :return:
    """
    return max([sublist[iter] for sublist in trainingData])

def minData(trainingData, iter):
    """
    Computes the minimum value of the column of the
    training data
    :param trainingData:       training data
    :param iter:               column number
    :return:
    """
    return min([sublist[iter] for sublist in trainingData])

def main():
    """
    This method is responsible reading the csv file of the training data and
    the testing data. It normalizes the data and uses that data to find
    noise in the training dataset and replacing the noisy records. It uses
    the refines labels and stores it in the training data which is further
    used for classification. It calculates the max and min column by calling the
    methods maxData and minData
    :return:
    """
    # Reads the traindata and the test data csv file
    traindata=readFile('DEC_TREE_TRAINING_data.csv')
    testdata=readFile('DEC_tree_testing__data.csv')
    maxValues=[]
    minValues=[]

    # FInds the max and min value of the column of the dataset
    for count in range(len(traindata[0])-1):
        maxValue=maxData(traindata,count)
        maxValues.append(maxValue)
        minValue=minData(traindata,count)
        minValues.append(minValue)
        denom=[max - min for max, min in zip(maxValues, minValues)]
    normTrainData=[]
    TrainData_1=[]

    # Normalizes the training data to dynamic zero ranging using the max and min values
    for iter in range(len(traindata)):
           norm1=[current - min for current, min in zip(traindata[iter], minValues)]
           norm2=[current/denomi for current,denomi in zip(norm1,denom)]
           normTrainData.append(norm2)
           TrainData_1.append(norm2)

    # Appends the labels of the training data since they are removed in the above step
    for iter in range(len(traindata)):
        TrainData_1[iter].append(traindata[iter][3])

    # Computes the cleaned labels by performing knn on the data
    bestLabels=computeKNN(TrainData_1)

    # Replaces the old labels by new refined labels
    for iter in range(len(bestLabels)):
        traindata[iter][3]=bestLabels[iter]

    # Writes the data to a new file by creating a new file and
    # writing the dataset to the new file
    csv.register_dialect('mydialect')
    list_name=['Attrib01','Attrib02','Attrib03','RedDwarf']
    with open('CleanedData.csv', 'w') as f:
      writer=csv.writer(f,dialect='excel')
      writer.writerow(list_name)
      writer.writerows(traindata)

main()
