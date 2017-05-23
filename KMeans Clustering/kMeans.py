__author__ = 'Nisha Bhanushali'
# Date : 10/30/2016
import matplotlib.pyplot as plt
import csv
import math
import random
from mpl_toolkits.mplot3d import Axes3D

def readFile():
     """
     This method reads the csv file and then calls the method computeKmeans().
     This method forms the clusters using the kmeans algorithm.
     :return:
     """
     f=open('KMEANS_DATA.csv','rt')
     try:
         reader=csv.reader(f)                          #This function is responsible for reading the file
         dataset=[]
         count=0
         for row in reader:
             if(count!=0):
                row_append=[float(i) for i in row]
                dataset.append(row_append)
             count+=1
         print(dataset)
         computeKmeans(dataset,13)
     finally:
         f.close()

def computeKmeans(dataset,K):
    """
    This method is responsible for performing the kmeans algorithm. It forms the
    clusters for various values of K ranging from 1 to 12. It forms the clusters
    until the best sse is obtained which is done upto 10 iterations when the K
    value does not change. The centroid is calculated using the mean of all the
    points in the cluster.The distance of all the data points to the centroid
    is computed using the euclidean distance formula. The stopping condition of
    the clustering is when the cluster remains unchanged.
    :param dataset:      the dataset of which the clustering is to be done
    :param K:            the maximum number of clusters which can be formed
    :return:
    """
    sse=[]                                          #sum of squared error for each value of K
    cluster_K=[]                                    # clusters for each value of K
    for k in range(K) :
        sse.append(0.0)

    # The clustering is done for each value of the K
    for k in range(1,13):
        best_sse=100000
        best_cluster=[]
        best_centroid=[]
        count_iterations=0

        # Performing the clustering for same value of K until the sse remains unchanged
        # for 10 iterations
        while(count_iterations<=10):
            centroid=[]
            cluster=[]
            current_sse=0
            for iter in range(k):
                cluster1=[]
                cluster.append(cluster1)

            # Determining the initial centroid seed points
            my_list=list(range(len(dataset)))
            seedPoints=random.sample(my_list,k)
            for iter in range(len(seedPoints)):
                centroid.append(dataset[iter])
            flag=False
            while(flag==False):
                # computing distance of all the data points to the cluster
                for count in range(len(dataset)):
                    min_dist=1000000
                    cluster_Id=0
                    for center_id in range(len(centroid)):
                        dist=0.0
                        for iter in range(len(centroid[center_id])):
                            dist+=math.pow(dataset[count][iter]-centroid[center_id][iter],2)
                        dist=math.sqrt(dist)
                        if(dist<min_dist):
                            min_dist=dist
                            cluster_Id=center_id
                    cluster[cluster_Id].append(count)

                # Finding the new prototype for each cluster
                centroid_new=[]
                for iter in range(len(cluster)):
                    # Initializing the new centroid for each cluster
                    cent=[]
                    for iter1 in range(len(centroid[0])):
                        cent.append(0)
                    # print(cluster[iter])
                    clusterpoints=cluster[iter]
                    # print('Length of cluster points ',len(clusterpoints))
                    for recordNum in clusterpoints:
                        data=dataset[recordNum]
                        for pos in range(len(data)):
                            cent[pos]+=data[pos]
                    for index in range(len(cent)):
                        cent[index]=cent[index]/len(clusterpoints)
                    centroid_new.append(cent)

                #Checking whether the stopping condition is satisfied or not
                check_Flag=False
                for count in range(len(centroid)):
                    for pos in range(len(centroid[count])):
                        if(centroid[count][pos]!=centroid_new[count][pos]):
                            check_Flag=True
                            break
                    if check_Flag==True:
                        break
                if(check_Flag==False):
                    flag=True
                else:
                    centroid=centroid_new
                    cluster=[]
                    for iter in range(k):
                        cluster1=[]
                        cluster.append(cluster1)
            #Computes the sse for each value of K
            for iter in range(len(centroid)):
                    cent=centroid[iter]
                    datapoints=cluster[iter]
                    # print(datapoint)
                    for count in datapoints:
                        data=dataset[count]
                        for iterx in range(len(data)):
                            current_sse+=math.pow(data[iterx]-cent[iterx],2)
            # Checks whether the current sse is less than the best sse
            if(current_sse<best_sse):
                best_sse=current_sse
                sse[k]=current_sse
                best_cluster=cluster
                best_centroid=centroid_new
            if(current_sse==best_sse):
                count_iterations=count_iterations+1
        print('K is :',k)
        best_centroid.sort(key=len)
        print('Centroid : ',best_centroid)
        best_cluster.sort(key=len)
        print('Clusters : ',best_cluster)
        size=getSize(best_cluster)
        print('Size of cluster : ',size)
        cluster_K.append(best_cluster)

    K=[0,1,2,3,4,5,6,7,8,9,10,11,12]
    sse.pop(0)
    K.pop(0)
# elbow curve
    #Plots a graph with number of clusters on x axis and sum of squared error
    # on the y axis
    plt.ylim(300,8000)
    plt.xlim(0,13)
    plt.plot(K,sse,'r',linewidth=2)
    plt.grid(True)
    plt.xlabel('Number of clusters')
    plt.ylabel('Sum of squared error')
    plt.title('Elbow for KMeans clustering')
    plt.show()

# Plotting the clusters of the graph with different colors
    colorList=['r','g','b','y','m','k','c','w']
    count=0
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
#Plotting the graph with attribute 1 on the x-axis and attribute-2 on y axis
    for cluster in cluster_K[7]:
        list_x=[]
        list_y=[]
        list_z=[]
        for iter in cluster:
            list_x.append(float(dataset[iter][0]))
            list_y.append(float(dataset[iter][1]))
            list_z.append(float(dataset[iter][2]))
        ax.scatter(list_x,list_y,list_z,s=25,c=colorList[count])
        ax.set_xlabel('Attribute-1')
        ax.set_ylabel('Attribute-2')
        ax.set_zlabel('Attribute-3')
        count+=1
    plt.show()

def getSize(cluster):
    """
    This method is responsible for computing the sizes of the each cluster
    :param cluster: the clusters whose size is to be found
    :return:
    """
    sizes=[]
    for count in range (len(cluster)):
            sizes.append(len(cluster[count]))
    return sizes
readFile()
