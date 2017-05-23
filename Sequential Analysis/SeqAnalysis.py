__author__ = 'Nisha Bhanushali'

# The variables declared below are used to declare the size of the bigraph and
# trigraph. It defines the rows and columns of the bigraph and trigraphs
w, h ,d = 28, 28,28

# Initializing the cells of the bigraph
biGraph = [[0 for x in range(w)] for y in range(h)]

# Initializing the cells of the trigraph
triGraph= [[[0 for x in range(w)] for y in range(h)]for z in range(d)]

def readFile():
     """
     This method reads each word in the file which is present on each
     line of the word file. This method first coverts the word to the lower
     case. It then removes the non alphabetical characters from the word.
     It appends ^ at the start of the word and $ at the end of the word.
     The method putInbiGraph is called to insert the count of 2 characters
     in the bigraph.
     The method putInTriGraph is called to insert the count of 3 characters
     appearing together in the trigraph.
     This method forms the clusters using the kNN algorithm.
     :return:
     """
     with open('words.txt', 'r') as f:
         for line in f:
            word=line.lower()
            word=rmvNonAlphaChars(word)
            word='^'+word+'$'
            putInbiGraph(word)
            putInTriGraph(word)
     f.close()


def rmvNonAlphaChars(word):
    """
    This method removes all the non alphabetical characters
    from the word.
    :param word: the word to be processed
    :return: processed word
    """
    string=""
    for c in word :
        if(ord(c)>96 and ord(c)<123):
            string+=c
    return string

def putInbiGraph(word):
    """
    This method increments the count of the characters which appear
    adjacent to each other in the bigraph matrix.
    :param word:
    :return:
    """
    for iter in range(len(word)-1):
        char1=word[iter]
        char2=word[iter+1]
        if(char1=='^'):
            iterx=0
        else:
            iterx=ord(char1)-96

        if(char2=='$'):
            itery=27
        else:
            itery=ord(char2)-96
        biGraph[iterx][itery]+=1
def putInTriGraph(word):
    """
    This method updates the count of the sequence consisting
    of three characters in the trigraph
    :param word: the word to be traversed
    :return:None
    """
    for iter in range(len(word)-2):
        char1=word[iter]
        char2=word[iter+1]
        char3=word[iter+2]
        if(char1=='^'):
            iterx=0
        else:
            iterx=ord(char1)-96
        itery=ord(char2)-96
        if(char3=='$'):
            iterz=27
        else:
            iterz=ord(char3)-96
        triGraph[iterx][itery][iterz]+=1
def search():
    """
    This method consists of different queries which needs to be answered.
    :return:
    """
    # Finding the count of nn
    print('The count of nn is : ',biGraph[ord('n')-96][ord('n')-96])

    # Finding the count of ss
    print('The count of ss is : ',biGraph[ord('s')-96][ord('s')-96])

    # Finds the count of most common letter for a word in the corpus to start with
    print('The most common letter for a word in the corpus to start with has the frequency : ',max(biGraph[0]))
    maxi=0
    maxIndex=0
    for iter in range(len(biGraph)):
        if(biGraph[0][iter]>maxi):
            maxi=biGraph[0][iter]
            maxIndex=iter
    print('The most common letter is : ',chr(maxIndex+96))

    # Finds the most common letter for a word in the corpus to end with
    maxi=0
    maxIndex=0
    for iter in range(len(biGraph)):
        if(biGraph[iter][27]>maxi):
            maxi=biGraph[iter][27]
            maxIndex=iter
    print('The most common letter for a word in the corpus to end with has the frequency : ',maxi)
    print('The most common letter is : ',chr(maxIndex+96))
    # Finds the most common vowel likely to come after t
    maxChar='a'
    maxi=biGraph[ord('t')-96][ord('a')-96]
    max1=biGraph[ord('t')-96][ord('e')-96]
    max2=biGraph[ord('t')-96][ord('i')-96]
    max3=biGraph[ord('t')-96][ord('o')-96]
    max4=biGraph[ord('t')-96][ord('u')-96]
    if(max1>maxi):
        maxChar='e'
        maxi=max1
    if(max2>maxi):
        maxChar='i'
        maxi=max2
    if(max3>maxi):
        maxChar='o'
        maxi=max3
    if(max4>maxi):
        maxChar='u'
        maxi=max4
    print('The most common vowel likely to come after t is : ',maxChar,' with frequency : ',maxi)

    # Finds the letter most likely to come after u
    maxi=0
    maxIndex=0
    for iter in range(len(biGraph)):
        if(biGraph[ord('u')-96][iter]>maxi):
            maxi=biGraph[ord('u')-96][iter]
            maxIndex=iter
    print('The letter most likely to come after u is : ',chr(maxIndex+96))

    # Finds the common ending for the words in this corpus whether it is er or ed
    if(triGraph[ord('e')-96][ord('r')-96][27]>triGraph[ord('e')-96][ord('d')-96][27]):
        word='er'
        freq=triGraph[ord('e')-96][ord('r')-96][27]
    else:
        word='ed'
        freq=triGraph[ord('e')-96][ord('d')-96][27]
    print('The common ending for the words in this corpus: ',word,' with the frequency of: ',freq)

    # Finds the most common combination ant or ent
    if(triGraph[ord('a')-96][ord('n')-96][ord('t')-96]>triGraph[ord('e')-96][ord('n')-96][ord('t')-96]):
        word='ant'
        freq=triGraph[ord('a')-96][ord('n')-96][ord('t')-96]
    else:
        word='ent'
        freq=triGraph[ord('e')-96][ord('n')-96][ord('t')-96]
    print('The most common combination is: ',word,' with the frequency of: ',freq)

     # Finds the most common combination tio or ion
    if(triGraph[ord('t')-96][ord('i')-96][ord('o')-96]>triGraph[ord('i')-96][ord('o')-96][ord('n')-96]):
        word='tio'
        freq=triGraph[ord('t')-96][ord('i')-96][ord('o')-96]
    else:
        word='ion'
        freq=triGraph[ord('i')-96][ord('o')-96][ord('n')-96]
    print('The most common combination is: ',word,' with the frequency of: ',freq)

     # Finds the most common combination ene or ine
    if(triGraph[ord('e')-96][ord('n')-96][ord('e')-96]>triGraph[ord('i')-96][ord('n')-96][ord('e')-96]):
        word='ene'
        freq=triGraph[ord('e')-96][ord('n')-96][ord('e')-96]
    else:
        word='ine'
        freq=triGraph[ord('i')-96][ord('n')-96][ord('e')-96]
    print('The most common combination is: ',word,' with the frequency of: ',freq)

    # Finds the most common character to follow the two characters qu
    maxi=0
    maxIndex=0
    for iter in range(len(triGraph[ord('q')-96][ord('u')-96])):
        if(triGraph[ord('q')-96][ord('u')-96][iter]>maxi):
            maxi=triGraph[ord('q')-96][ord('u')-96][iter]
            maxIndex=iter
    print('The most common character to follow the two characters qu is: ',chr(maxIndex+96),' with the frequency of:',maxi)

    # Finds the most common character to follow the character q
    maxi=0
    maxIndex=0
    maxj=sum(triGraph[ord('q')-96][ord('u')-96])
    for iter in range(len(triGraph[ord('q')-96])):
        if(sum(triGraph[ord('q')-96][iter])>maxi and sum(triGraph[ord('q')-96][iter])<maxj):
            maxi=sum(triGraph[ord('q')-96][iter])
            maxIndex=iter
    print('The most common character to follow the character q is: ',chr(maxIndex+96),' with the frequency of:',maxi)

    #Finds the most common character to follow the two characters ba
    maxi=0
    maxIndex=0
    for iter in range(len(triGraph[ord('b')-96][ord('a')-96])):
        if(triGraph[ord('b')-96][ord('a')-96][iter]>maxi):
            maxi=triGraph[ord('b')-96][ord('a')-96][iter]
            maxIndex=iter
    print('The most common character to follow the two characters ba is: ',chr(maxIndex+96),' with the frequency of:',maxi)

    # Finding the count of aa
    print('The count of aa is : ',biGraph[ord('a')-96][ord('a')-96])

    # Finding the count of lp
    print('The count of lp is : ',biGraph[ord('l')-96][ord('p')-96])

# Call to method readFile() to build a bigraph or trigraph
readFile()
# Call to method search to run different queries
search()