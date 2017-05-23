__author__ = 'Nisha Bhanushali'

import csv    #Import the csv to read the csv file
import statistics   #import statistics to perform compute different statistical values
from collections import Counter #to compute the mode on the list of data points
from matplotlib import pyplot as plt #to plot the scatter-point graph and histogram
import sys

# This method reads the Unclassified_Data.csv file, it stores the values in the list and then calls the
# method scatter(), histogram() and mysteryData() to perform the various tasks
def readFile():
    #the open method creates an object of the csv file

    var=input('Enter the path for the Unclassified Data csv file')
    f=open(var,'rt')
    try:
        # The below line reads the csv file
        reader = csv.reader(f)
        #list to store the values from the csv file to the list, this list is then used compute stiffness
        # and quantized_stiffness
        list=[]

        #this are the variables used to plot the graph
        # of force(Newtons) vs deflection(mm)
        x=[]
        y=[]
        i=0
        for row in reader:
            l=[]
            if(i!=0):
                l.append(row[0])
                x.append(float(row[0]))
                l.append(row[1])
                y.append(float(row[1]))
                list.append(l)
            i=i+1
       # Call to the method which plots the scatter-plot diagram
        scatter(x,y)

       # Call to the method which plots the histogram of the stiffness
        histogram(list)

       # Call to the method which reads mystery data and computes the
       # mean, median, mode, mid-range and standard deviation
        mysteryData()

    finally:
        f.close()

# This method is called from the readFile() method. x is the Force applied(Newtons) and y is the
# deflection(mm). This method plots the scatter-plot graph with the above mentioned x and y axis
def scatter(x,y):
        plt.scatter(x,y)
        plt.title('Scatter plot graph')
        plt.xlabel('Force (Newtons)')
        plt.ylabel('Deflection (mm)')
        plt.show()

# This method is called from the readFile() method. list is the list of multiple force values
# and the corresponding deflection obtained for that force. This method computes the
# stiffness=deflection/force and then quantizes the deflection. The histogram is then
# plotted. This method calls the Otsu() which then divides the data into three clusters
# and computes two threshold values

def histogram(list):

      list_stiffness=[]              #list to store the stiffness computed
      size=len(list)

      #Computing the quantized stiffness
      for i in range(0,size):
        l1=list[i]
        num=float(l1[1])           #Numerator is the deflection
        den=float(l1[0])           #Denominator is the force applied
        stiff=num/den
        stiff_quantized=round(stiff*50.0)/50.0
        list_stiffness.append(stiff_quantized)

      #Plotting the histogram
      plt.hist(list_stiffness,bins=50)
      plt.title('Histogram of Flexibility')
      plt.xlabel('Flexibility')
      plt.ylabel('Frequency of the flexibility')
      plt.show()
      Otsu(list_stiffness)

# This method is the implementation of the Otsu's algorithm to find out two threshold values.
# This method is called from the histogram() method and the input parameter to the method is
# is the list of quantized flexibility computed. This method calls compute_threshold() and
# search_count() method
def Otsu(list_stiffness):
    list_stiffness.sort()
    list_stiff=list_stiffness
    best_mixed_variance=10000      # the weighted variance is set to the highest possible value
    best_threshold=0
    # Computing the threshold values

    threshold=compute_threshold(list_stiffness)
    count_threshold=0
    count_above=0
    count_under=0


    #Finding the mimimum weighted variance
    while(count_threshold<2):

        for i in range(0,len(threshold)):
            last_under=search_count(threshold[i],list_stiff)
            wt_under=last_under/len(list_stiff)              # fraction of points below the threshold
            variance_under=statistics.pvariance(list_stiff[:last_under+1],wt_under) # variance below the threshold
            last_above=len(list_stiff)-last_under
            wt_above=last_above/len(list_stiff)             # fraction of points above the threshold
            if(last_under<len(list_stiff)-1):
                variance_above=statistics.pvariance(list_stiff[last_under+1:],wt_above) # variance of points above the threshold
            mixed_variance=wt_under*variance_under+wt_above*variance_above  # calculating the mixed variance
            if(mixed_variance<best_mixed_variance):
                best_mixed_variance=mixed_variance
                best_threshold=threshold[i]
                count_under=last_under
                count_above=last_above
        if(count_under>count_above):
            list_stiff=list_stiffness[:count_under+1]
        else:
            start=count_under+1
            list_stiff=list_stiffness[start:]
        count_threshold+=1
        print('Best threshold :',best_threshold)
        print('Minimum weighted variance :',best_mixed_variance)
        best_mixed_variance=1000
        best_threshold=0

# This method is called from the Otsu() method. It counts the number of points that are less than the threshold value
def search_count(thresh,list_stiffness):
    start=0
    count=0
    while(start<len(list_stiffness)):
        if(list_stiffness[start]<thresh):
            count+=1
        start+=1
    return count

# This method generates a list of all possible threshold values
def compute_threshold(list_stiffness):
    list_threshold=[]
    thresh=0.02
    while thresh<=1.2 :
        list_threshold.append(round(thresh,2))
        thresh=thresh+0.02
    return list_threshold

# This method processes the mysteryData file and computes the mode, median, mid-range, average and standard deviation
# of the data points
def mysteryData():
   #the open method creates an object of the csv file
    var=input('Enter the path for the Mystery Data csv file')
    f=open(var,'rt')
    try:
        # Reading the csv file
        reader=csv.reader(f)
        list_points=[]
        count=0
        for row in reader:
            if(count!=0):
                list_points.append(float(row[0]))
            count=count+1
        data=Counter(list_points)
        mode=data.most_common(4)
        print('Mode : ',mode)

        median=statistics.median(list_points)
        print('Median : ',median)

        average=statistics.mean(list_points)
        print('Average : ',average)

        mid_range=(max(list_points)+min(list_points))/2
        print('Mid Range : ',mid_range)
        std=statistics.pstdev(list_points)
        print('Standard deviation : ',std)



        # Removing the last element from the list
        list_points.pop()
        print('')
        print('After removing the last element in the list')
        # Computing the mode, median, mid-range, average, standard deviation on the new list
        data=Counter(list_points)
        mode=data.most_common(4)
        print('Mode : ',mode)

        median=statistics.median(list_points)
        print('Median : ',median)

        mid_range=(max(list_points)+min(list_points))/2
        print('Mid Range : ',mid_range)

        average=statistics.mean(list_points)
        print('Average : ',average)

        std=statistics.pstdev(list_points)
        print('Standard deviation : ',std)

    finally:
        f.close()
# This method is the main method which calls the readFile() method.
def main():
    readFile()
# Calling the main method
main()
