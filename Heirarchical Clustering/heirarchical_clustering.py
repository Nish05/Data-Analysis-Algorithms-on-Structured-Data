__author__ = 'Nisha Bhanushali'
# Date : 10/16/2016
# This library is imported because it consists of methods which help to read the csv files
import csv
# This library is imprted to perform the square operation and the power operation
import math

def readFile():
    """
    This method reads the dataset and creates a 2D array of the dataset. It performs
    agglomerative clustering by calling the method clustering() and passing the
    dataset as the parameter
    :return:
    """
    file=open('SHOPPING_CART.csv')
    try:
        dataset=[]
        csv.register_dialect('strip', skipinitialspace=True)
        reader = csv.reader(file, dialect='strip')
        for row in reader:
            dataset.append(row)
        clustering(dataset)
    finally:
        file.close()

def distance(cluster1,cluster2):
    """
    This method computes the euclidean distance
    between the two centroids and returns the
    euclidean distance to the clustering() method
    :param cluster1:
    :param cluster2:
    :return:
    """
    total_dist=0
    total=0                         #The total euclidean distance between two centroids
    for iter in range (1,len(cluster1)):
        total+=math.pow(float(cluster1[iter])-float(cluster2[iter]),2)
    total_dist=math.sqrt(total)
    return total_dist

def clustering(dataset):
    """
    This method performs agglomerative clustering by initially
    considering each record of the dataset as a cluster. It computes
    the euclidean distance between all the clusters and finds the
    two clusters which have minimum distance and merges two clusters
    and computes the centroid by calling the calculateSum() and
    passes the sum calculated to the calculateCentroid() method
    and the new centroid is computed. Amongst the two clusters
    being merged the cluster which is at the higher index is
    removed and the new centroid computed is put in the position
    at the lower index. It prints the output when the number of clusters
    formed is 3.
    :param dataset:     The dataset which is to be clustered
    :return:
    """

    Cluster=[]                                      #Stores the cluster centroid
    ClusterIds=[]                                   #Stores the Ids of the records in the same cluster
    size=[]
    guest_Ids=[]
     # Initializing the initial clusters
    for iter in range(1,len(dataset)):
        list=[]
        list.append(iter)
        Cluster.append(dataset[iter])
        ClusterIds.append(list)

    # Agglomerative clustering
    while(len(Cluster)>1):
        minDist=10000
        index1=-1
        index2=-1
        indexx=0

        while(indexx <len(Cluster)):
            indexy=0
            while( indexy <len(Cluster)):

                if(indexx!=indexy):

                    dist=distance(Cluster[indexx],Cluster[indexy])
                    if(dist<minDist):
                        minDist=dist
                        index1=indexx
                        index2=indexy
                indexy+=1
            indexx+=1
        if(index1!=-1 and index2!=-1):

            #Inserting the ids in the cluster they belong to
            idList=ClusterIds[max(index1,index2)]
            position=min(index1,index2)
            toRemovePos=max(index1,index2)
            list2= ClusterIds[toRemovePos]
            print('Iteration number : ',101-len(Cluster))
            for count in range (len(list2)):
                ClusterIds[position].append(list2[count])
                print('Merged IDS : ',ClusterIds[position])


            # Updating the centroid
            idNums1=ClusterIds[position]
            ClusterIds.remove(idList)

            sum1=calculateSum(idNums1,dataset)
            centroid=calculateCentroid(sum1,len(idNums1))
            minList1=Cluster[position]
            minList2=Cluster[toRemovePos]
            Cluster.remove(minList1)
            Cluster.remove(minList2)
            Cluster.insert(position,centroid)

        #Printing the 3 clusters
            if(len(Cluster)==3):
                for iter in range(len(ClusterIds)):
                    size.append(len(ClusterIds[iter]))
                    guest_Ids.append(ClusterIds[iter])

    for iter in range(len(guest_Ids)):
            print('Size is: ',size[iter])
            print('Guest Ids: ',guest_Ids[iter])

def calculateSum(idNums,dataset):
    """
    This method is used to create a centroid. It calculates the
    sum of the attribute values. and returns the sum to the
    clustering() method
    :param idNums:          The id number of records in the same cluster
    :param dataset:         The original average which is calculated
    :return: the calculated sum
    """
    list=[]
    for count in range(len(dataset[0])):
        list.append(0)
    for iterx in range(0,len(idNums)):
        row=dataset[idNums[iterx]]
        for itery in range(len(row)):
            list[itery]+=float(row[itery])
    return list

def calculateCentroid(list1,length):
    """
    It computes the centroid of the clustered
    by dividing the computed sum by the number of
    records in the same cluster.
    :param list1:  the centroid whose average is to be computed
    :param length: number of records in the cluster
    :return: centroid of the cluster
    """
    centroid=[]
    for iter in range(len(list1)):
        centroid.append((list1[iter]/length))
    return centroid



readFile()
