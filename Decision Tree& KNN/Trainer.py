__author__ = 'Nisha Bhanushali'
# Name: Nisha Bhanushali
# Date: 10/07/2016
# This library is imported because it consists of methods which help to read the csv files
import csv
# This library is imprted to perform the square operation
import math

class Node():
    """
    This method creates node object for the decision tree.
    For each node, the name of the attribute, the label of the attribute,
    its left and right child, the threshold value is store.
    """
    def __init__(self, name=None,threshold=None,value=None,label=None):
        self.left = None                    #Left Node
        self.name = name                    #Name of the node
        self.threshold=threshold            #Threshold value at that node
        self.value=value                    #className of the node
        self.label=label                    # label of the node e.g, leaf, root
        self.right = None                   # Right Node
        self.dataset=[]
        self.Leaf=False
def readFile():
    """
    This method opens the datafile. Its reads the csv file row by row.
    Stores the file in the 2D array. It then builds the decision tree
    of the dataset by calling the method decisionTree(). This method
    then calls the generatePrintStatements() where the if-else statements
    for the classifier are generated. This if-else statements are then
    written to the python file by calling writeTofile() method.
    :return: None
    """
    f=open('CleanedData.csv','rt')

    try:
        reader=csv.reader(f)
        count=0
        dataset=[]
        for row in reader:
            dataset.append(row)
        root=Node()
        decisionTree(dataset,root,'root')
        list=[]
        # list=generatePrintStatements(root,list)
        list=generateTree(root,list,'\t')
        writeTofile(root,list)
    finally:
        f.close()


def computeGini(index,dataset):

     """
     This method computes the minimum weighted gini index of
     attribute. This is done by checking all the values of
     that attribute. It computes the gini index for the
     values less than threshold and for values greater than
     threshold. It computes the weighted gini index for the
     attribute and returns it along with the threshold at which
     it is computed.
     :param index:      column number of the attribute
     :param dataset:    the dataset
     :return: minimum weighted gini index, best threshold value
     """
     threshList=thresholds(index,dataset)
     min_weighted_gini=1000
     min_threshold=threshList[0]
     for iter in range (len(threshList)):
         #Generates a list of threshold values for which the weighted gini index is to be computed
         threshold=threshList[iter]
         class0_under=0                     #Count of attributes which have class zero and which have value <= threshold
         class1_under=0                     #Count of attributes which have class one and which have value <= threshold
         class0_above=0                     #Count of attributes which have class zero and which have value > threshold
         class1_above=0                     #Count of attributes which have class one and which have value > threshold
         pabove0=0
         pabove1=0
         pbelow0=0
         pbelow1=0

         for pos in range(1,len(dataset)):
             if(float(dataset[pos][index])<=threshold):
                 if(float(dataset[pos][len(dataset[0])-1])==1):
                     class1_under+=1
                 else:
                     class0_under+=1
             elif(float(dataset[pos][index])>threshold):
                  if(float(dataset[pos][len(dataset[0])-1])==1):
                     class1_above=class1_above+1
                  else:
                     class0_above=class0_above+1

         total_above=class0_above+class1_above
         total_below=class0_under+class1_under
         total=total_above+total_below

         if(total_above==0):
            pabove1=0
            pabove0=0
         else :
            pabove1=class1_above/total_above
            pabove0=class0_above/total_above
         if(total_below==0):
            pbelow1=0
            pbelow0=0
         else:
            pbelow1=class1_under/total_below
            pbelow0=class0_under/total_below
         # Computes the gini index for above than threshold value
         gini_above=1-math.pow(pabove1,2)-math.pow(pabove0,2)
         # Computes the gini index for below or less than threshold value
         gini_below=1-math.pow(pbelow1,2)-math.pow(pbelow0,2)

         # Computes the weighted gini index for the same
         weighted_gini=(total_below/total)*gini_below+(total_above/total)*gini_above
         # print(weighted_gini)
         if(weighted_gini<min_weighted_gini):
                 min_weighted_gini=weighted_gini
                 min_threshold=threshold
     return min_weighted_gini,min_threshold

def decisionTree(dataset,node,label):
    """
    Builds the decision tree using 3 criterias. Stops
    when all the records are in the same class. Splits
    the data based on the minimum threshold value of an
    attribute which it finds by computing the minimum
    gini index. It divides the data into left half
    and right half and recursively calls the decision tree
    method until the stopping criteria is satisfied.

    :param dataset: which needs to be classified
    :param node:    the node which is to be classified
    :param label:   label of the node
    :return: the complete decision tree
    """
    value=0
    if(len(dataset)==1 or len(dataset)==0 or stopCondition(dataset,value)!=-1):
        if(stopCondition(dataset,value)==1):
            node.value=1
            node.Leaf=True
        else:
            node.value=0
            node.Leaf=True
        return
    else:
        threshold,index,name=bestSplit(dataset)
        node.name=name
        node.threshold=threshold
        node.label=label
        node.left=Node()
        node.right=Node()
        node.dataset=dataset
        list_left,list_right=divideData(dataset,index,threshold)

        decisionTree(list_left,node.left,'left')
        decisionTree(list_right,node.right,'right')

def bestSplit(dataset):
    """
    This methods finds the best split by computing the
    gini index of each attribute which it does by calling
    the method computeGini(). It then chooses the attribute
    which has minimum gini index
    :param dataset: the whole data set
    :return: best threshold, the index of the column, and the name of the attribute
    """
    min_weighted_gini=1000000
    min_threshold=0
    index=0
    for iter in range(len(dataset[0])-1):

        weighted_gini,threshold=computeGini(iter,dataset)
        if(weighted_gini<min_weighted_gini):
            min_weighted_gini=weighted_gini
            min_threshold=threshold
            index=iter
    name=dataset[0][index]
    return min_threshold,index,name

def thresholds(index,dataset):
    """
    Generates a list of threshold values for a given
    attribute. This method is called from computeGini()
    method. It returns the list to the
    :param index:
    :param dataset:
    :return:
    """

    threshList=[]
    iterx=1
    for iterx in range(1,len(dataset)):
            threshList.append(float(dataset[iterx][index]))
    return threshList

def stopCondition(dataset,value):
    lastIndex=len(dataset[0])-1
    dataset1=dataset[1:]
    count1=0
    count0=0
    for row in dataset1:
        if(row[lastIndex]=='1'):
                count1=count1+1
        else:

                count0=count0+1

    if(count1/len(dataset1)>=0.95 ):
            return 1
    elif( count0/len(dataset1)>=0.95):
            return 0
    else:
            return -1

def divideData(dataset,index,threshold):

    """
    This methods divides the data into two parts.
    All the data which have the attribute value less than
    threshold is left data. All the data with attribute
    greater than threshold are classified as the right data
    :param dataset:       dataset which needs to be divided
    :param index:         attribute on basis of which the data is to be divided
    :param threshold:     the threshold value for a particular attribute
    :return:the left data and the right data
    """
    dataset1=dataset[1:]
    list_left=[row for row in dataset1 if (float(row[index]) <=threshold)]
    list_right=[row for row in dataset1 if (float(row[index]) >threshold)]
    list_left.insert(0,dataset[0])
    list_right.insert(0,dataset[0])
    return list_left,list_right

def writeTofile(root,list):
    """
    This methods generates a new python file. It writes the program
    into that file. It reads the csv file of the test data and the
    validation data. It then writes the code to read those files.
    Depending on the type of the file it performs operations.
    For test data, it reads each row and using the if-else
    statements of the decision tree, it assigns class to that
    record and prints the class. It then computes the accuracy
    for the test data.For validation data, it reads each row
    of the csv file and finds the label of the record and
    stores back into the new csv file.
    :param root:        root of the decision tree
    :param list:        list of if-else statements that is to be printed
    :return:None
    """
    f=open('HW_04B_Bhanushali_Nisha_Classifier.py','w')
    f.write('import csv\n')
    f.write('def readFile():\n')
    f.write('   main(\'DecTree_Testing.csv\',\'test\')\n')
    f.write('   main(\'DecTree_validation_data.csv\',\'validation\')\n')
    f.write('def main(filename,filetype):\n')
    f.write('   f=open(filename,\'rt\')\n')
    f.write('   try:\n')
    f.write('       reader=csv.reader(f)\n')
    f.write('       if(filetype==\'test\'):\n')
    f.write('           count=0\n')
    f.write('           classTrue=0\n')
    f.write('           classFalse=0\n')
    f.write('           for row in reader:\n')
    f.write('               if(count!=0):\n')
    f.write('                   label=computeForRow(row)\n')
    f.write('                   print(label)\n')
    f.write('                   if(label==int(row[4])):\n')
    f.write('                       classTrue=classTrue+1\n')
    f.write('                   else:\n')
    f.write('                       classFalse=classFalse+1\n')
    f.write('               count=count+1\n')
    f.write('           total=classTrue+classFalse\n')
    f.write('           accuracy=classTrue/total\n')
    f.write('           print(\'Accuracy : %f\'%(accuracy*100))\n')
    f.write('       else:\n')
    f.write('           list=[]\n')
    f.write('           count=0\n')
    f.write('           for row in reader:\n')
    f.write('               if(count!=0):\n')
    f.write('                   l=[]\n')
    f.write('                   label=computeForRow(row)\n')
    f.write('                   l.append(label)\n')
    f.write('                   list.append(l)\n')
    f.write('               count=count+1\n')
    f.write('           writeToFile(list)\n')
    f.write('   finally:\n')
    f.write('           f.close()\n')
    f.write('def writeToFile(labels):\n')
    f.write('   csv.register_dialect(\'mydialect\')\n')
    f.write('   with open(\'MyClassifications.csv\',\'w\') as output_File:\n')
    f.write('       writer=csv.writer(output_File,dialect=\'mydialect\')\n')
    f.write('       for row in labels:\n')
    f.write('           writer.writerow(row)\n')
    f.write('def computeForRow(row):\n')
    f.write('    classLabel=0\n')
    f.write('    Attrib01=float(row[0])\n')
    f.write('    Attrib02=float(row[1])\n')
    f.write('    Attrib03=float(row[2])\n')
    f.write('    Attrib04=float(row[3])\n')
    for iter in range(len(list)):
        # if(iter==4):
        #     f.write('      else:\n')
        #     f.write(' ')
        # if(iter==7):
        #     f.write('       else:\n')
        #     f.write(' ')
        # if(iter==10):
        #     f.write('   else:\n')
        f.write(list[iter])
    f.write('        return classLabel\n')
    f.write('if __name__=="__main__":\n')
    f.write('   readFile()')

def generatePrintStatements(node,list):
    """
     This method generates the if else conditions using the
     decision treee. This is done recursively. By traversing
     the tree in the preorder fashion. This list is printed
     in the python file.
     :param node: initially root node is passed
     :return:list of the if-else statements to be printed

    """
    if(node==None):
        return
    else:
        stmnt=""
        if(node.label=='root'):

            stmnt='   if( %s <= %f ):\n'%(node.name,node.threshold)
            list.append(stmnt)
        else:
            if(node.name==None):
                stmnt='             classLabel=%u\n'%(node.value)
                list.append(stmnt)
            else:
                 stmnt='      if( %s <= %f ):\n'%(node.name,node.threshold)
                 list.append(stmnt)
        generatePrintStatements(node.left,list)
        generatePrintStatements(node.right,list)
    return list

def generateTree(node,list,nextTab):
    if(node.Leaf==True):
        stmnt=nextTab+'classLabel= %u\n'%(node.value)
        list.append(stmnt)
        return list
    else :
         stmnt=nextTab+'if( %s <= %f ):\n'%(node.name,node.threshold)
         list.append(stmnt)
         generateTree(node.left,list,nextTab+'\t')
         stmnt=nextTab+'else'+':\n'
         list.append(stmnt)
         generateTree(node.right,list,nextTab+'\t')
    return list
readFile()              #call to the main method
