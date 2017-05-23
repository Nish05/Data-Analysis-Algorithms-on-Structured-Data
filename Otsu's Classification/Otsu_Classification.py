__author__ = 'Nisha Bhanushali'
# Name: Nisha Bhanushali
# Date: 09/09/2016
# This library is imported because it consists of methods which help to read the csv files
import csv
# This library is imported because it consists of methods which help to plot the graphs
from matplotlib import pyplot as plt
#This library is used to compute the distance between the two points
import math

#This method is called from the main method and it reads the csv file segregrates the
# columns of the file into three parts force, deflection and classes. The force and
# delfection are store din one list while a seperate list is maintained for the classes
# of those rows. The next step I do is to compute the flexbility which is done by calling
# the method computeFlex and passing the parameter list to that method. The next step is
# is to generate a list of threshold values which is done calling the method computeThres().
# Then sorted the flexibility and classes in the increased order of flexibility and passed
# it to the setThreshold() method.

def readFile():
     f=open('Classified_Data.csv','rt')
     try:

         reader=csv.reader(f)                         #Reading the csv file
         list=[]                                      #List consisting of force and deflection
         classes=[]                                   # List of classes
         count=0
         #Reading the line row-wise
         for row in reader:
             l=[]
             if(count!=0):
                l.append(float(row[0]))
                l.append(float(row[1]))
                classes.append(int(row[2]))
                list.append(l)
             count+=1

         flexibility=computeFlex(list)                  # Computing the flexibility using the formula deflection/force
         # print(flexibility)
         threshold=computeThres()                       # Generating a list of threshold

         sorted_flex,sorted_classes=zip(*sorted(zip(flexibility,classes)))  #Sorting the flexibility and classes based on flexibility
         bestThreshold=setThreshold(sorted_flex,sorted_classes,threshold)                 #Call the method setThreshold to set up the threshold value

         classifyData(bestThreshold)
     finally:
         f.close()

# This method is called from the readFile() method. The parameter to this method
# is list of list of force and deflection. It computes the flexibility using the formula deflection
# divided by the force. This method then returns the list of flexibility.
def computeFlex(list):
     listFlex=[]              #list to store the stiffness computed
     size=len(list)

     #Computing the quantized stiffness
     for i in range(0,size):
        l1=list[i]
        num=float(l1[1])           #Numerator is the deflection
        den=float(l1[0])           #Denominator is the force applied
        flex=num/den
        flex_quantized=round(flex*50.0)/50.0
        listFlex.append(flex_quantized)
     return listFlex

# This method generates a list of threshold. Each threshold is at the interval of
# 0.02 and is computed till 1.2. Each threshold is then appended to the list of
# thresholds. This list is then returned to the readFile() method.
def computeThres():
    list_threshold=[]
    thresh=0.02
    while thresh<=1.2 :
        list_threshold.append(round(thresh,2))
        thresh=thresh+0.02
    return list_threshold

# This method determines the threshold value based on the minimum misclassification rate.
# The misclassification rate is computed calling the method search_misses and the parameters
# passed to this method are the threshold value and the sorted list of flexibility and their
# corresponding classes. Then the number of wrong values is computed using the formula :
# n_wrong=n_misses+n_fa for each threshold value. The n_wrong is compared with the
# misclassification rate and the threshold value which generates the least misclassification
# rate is selected. Since, thresholds list has thresholds in the increasing order, I did not
# need to explicitly handle the tie breaking condition because always the larger threshold will
# be selected in the case if for two thresholds the misclassification rate is minimum.
# Then the best threshold value is the one with the least misclassification rate.
# The graph is plotted for the misclassification rate as the function of threshold by calling
# the function plotGraph() which has parameters as the threshold, misclassified melons and
# and the best misclassified rate.
def setThreshold(sorted_flex,sorted_classes,threshold):
    best_misclass_rate=10000
    best_threshold=0
    best_missed=0
    best_fracMiss=0
    best_fa=0
    best_unripe=0
    x_threshold=[]
    y_fracMelons=[]
    x_FAR=[]
    y_TPR=[]

    for iter in range(0,len(threshold)):
        thresh=threshold[iter]
        n_misses,n_fa,unripe_count,cr,hit=search_misses(thresh,sorted_flex,sorted_classes)
        n_wrong=n_misses+n_fa
        fract_miss=n_wrong/(n_misses+n_fa+cr+hit)
        FAR=n_fa/(n_fa+cr)
        TPR=hit/(hit+n_misses)
        x_threshold.append(threshold[iter])
        y_fracMelons.append(fract_miss)
        x_FAR.append(FAR)
        y_TPR.append(TPR)
        if(n_wrong<=best_misclass_rate):
            best_misclass_rate=n_wrong
            best_threshold=thresh
            best_missed=n_misses
            best_fa=n_fa
            best_unripe=unripe_count
            best_fracMiss=fract_miss



    best_threshold=round(best_threshold*50)/50
    print('Best threshold',best_threshold)
    print('Best Missed',best_missed)
    print('Best false alarm',best_fa)
    print('Best Unripe count',best_unripe)

    plotGraph(x_threshold,y_fracMelons,best_fracMiss)
    X,Y=misclassCordinates(x_FAR,y_TPR)
    plotROC(x_FAR,y_TPR,X,Y)

    return best_threshold

# This method computes all the parameters that are required for
# plotting all the graphs. For , each threshold value this method
# computes the true positve count, false positive count, true negative
# count and false negative count. This all values are computed for the
# ripe melons and returned back to the setThreshold() method.
def search_misses(thresh,sorted_flex,sorted_classes):
    misses=0
    fa=0
    count=0
    hit=0
    cr=0
    for iter in range(0,len(sorted_flex)):
        if((sorted_classes[iter]==2 and sorted_flex[iter]<thresh)):
            misses+=1

        if((sorted_classes[iter]!=2 and sorted_flex[iter]>=thresh)):
                if(sorted_classes[iter]==1):
                    count+=1
                fa+=1
        if((sorted_classes[iter]!=2 and sorted_flex[iter]<thresh)):
                cr+=1
        if((sorted_classes[iter]==2 and sorted_flex[iter]>=thresh)):
            hit+=1

    return misses,fa,count,cr,hit

# This method plots the graph with the threshold on x-axis and
# misclassification rate on y-axis. It also draws a circle around
# the threshold values which have minimum misclassification rate

def plotGraph(x_threshold,y_fracMelons,best_misrate):
    list_best_threshold=search(x_threshold,y_fracMelons,best_misrate)
    fig,ax=plt.subplots()
    for iter in range(0,len(list_best_threshold)):
        circle=plt.Circle((list_best_threshold[iter], best_misrate), 0.01, color='r', fill=False)
        plt.gcf().gca().add_artist(circle)
        fig.show()
    plt.plot(x_threshold,y_fracMelons)


    plt.title('Misclassification as function of Threshold')
    plt.xlabel('Threshold')
    plt.ylabel('Misclassification Rate')
    plt.show()

# This method searches for the threshold values which have the minimum misclassification
# rate. Since,we know the minimum misclassification rate, we can obtain all the threshold
# values which have minimum misclassification rate. This is done by maintaining two lists
# one for threshold and another for their corresponding misclassification rate. Now,
# for all the threshold values this method finds out the one's which have the minimum
# threshold and appends it the list and this list is returned back to the setThreshold
# method.
def search(x_threshold,y_fracMelons,best_misrate):
    list_index=[]
    list_threshold=[]
    for iter in range(0,len(y_fracMelons)):
        if(y_fracMelons[iter]==best_misrate):
            list_index.append(iter)
    for iter in range(0,len(list_index)):
        list_threshold.append(x_threshold[list_index[iter]])

    return list_threshold

# This method classifies the unclassified unknown data into ripe and unripe melons.
# The threshold which has the minimum misclassification rate and is computed on the
# training data is used to classify the data into two parts. The ripe one's are
# assigned label 1 and the unripe are assigned label 0. This list is then store
# in the new csv file which is done by calling the method writeToFile().
def classifyData(bestThreshold):
    f=open('MELONS_TO_CLASSIFY.csv','rt')
    try:
        reader=csv.reader(f)
        list=[]
        labels=[]
        count=0
        for row in reader:
            l1=[]
            if(count!=0):
                l1.append(row[0])
                l1.append(row[1])
                list.append(l1)
            count+=1
        flexibility=computeFlex(list)
        for iter in range(0,len(flexibility)):
            l1=[]
            if(flexibility[iter]<bestThreshold):
                l1.append(0)
            else:
                l1.append(1)
            labels.append(l1)
        writeToFile(labels)
    finally:
        f.close()

# This method writes the list of labels which are generated by the classifyData() method
# to the csv file.

def writeToFile(labels):
    csv.register_dialect('mydialect')
    with open('CLASSIFICATIONS.csv','w') as output_File:
        writer=csv.writer(output_File,dialect='mydialect')
        for row in labels:
            writer.writerow(row)

# This method plots the ROC curve with False Positive Rate
# as the x-axis and true positive rate as the y-axis.
# This method also plots the circle around the point which is
# closest to the upper left corner.
def plotROC(x_FAR,y_TPR,X,Y):
    plt.ylim(-0.2,1.2)
    plt.xlim(-0.2,1.2)
    fig,ax=plt.subplots()
    plt.plot(x_FAR,y_TPR,'r',linewidth=2)
    for iter in range (0,len(X)):
        circle=plt.Circle((X[iter], Y[iter]), 0.02, color='b', fill=False)
        plt.gcf().gca().add_artist(circle)
        fig.show()
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristics')
    plt.show()

# This method finds the point on the graph which has
# the lowest misclassification rate by computing the
# distance of all points from the leftmost point.
# The point which has minimum distance is the one which
#  has least misclassification rate.It finds out all the
# values which have this maximum slope and then returns
# the co-ordinates of those points to the method setThreshold()
def misclassCordinates(x_FAR,y_TPR):
    minDist=1000
    X=[]
    Y=[]
    for iter in range(len(x_FAR)):
            if( math.sqrt((x_FAR[iter] - 0)**2 + (y_TPR[iter] - 1)**2)<minDist):
               minDist= math.sqrt((x_FAR[iter] - 0)**2 + (y_TPR[iter] - 1)**2)
    for iter in range(len(x_FAR)):
            if(math.sqrt((x_FAR[iter] - 0)**2 + (y_TPR[iter] - 1)**2)==minDist):
                X.append(x_FAR[iter])
                Y.append(y_TPR[iter])
    return X,Y

# This is the main method which calls the readFile method which
# is the method which processes the file.
def main():
    readFile()
main()



























































































































































































































































