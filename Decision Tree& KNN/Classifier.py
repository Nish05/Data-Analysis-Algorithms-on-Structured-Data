import csv
def readFile():
   main('DecTree_Testing.csv','test')
   main('DecTree_validation_data.csv','validation')
def main(filename,filetype):
   f=open(filename,'rt')
   try:
       reader=csv.reader(f)
       if(filetype=='test'):
           count=0
           classTrue=0
           classFalse=0
           for row in reader:
               if(count!=0):
                   label=computeForRow(row)
                   print(label)
                   if(label==int(row[4])):
                       classTrue=classTrue+1
                   else:
                       classFalse=classFalse+1
               count=count+1
           total=classTrue+classFalse
           accuracy=classTrue/total
           print('Accuracy : %f'%(accuracy*100))
       else:
           list=[]
           count=0
           for row in reader:
               if(count!=0):
                   l=[]
                   label=computeForRow(row)
                   l.append(label)
                   list.append(l)
               count=count+1
           writeToFile(list)
   finally:
           f.close()
def writeToFile(labels):
   csv.register_dialect('mydialect')
   with open('MyClassifications.csv','w') as output_File:
       writer=csv.writer(output_File,dialect='mydialect')
       for row in labels:
           writer.writerow(row)
def computeForRow(row):
    classLabel=0
    Attrib01=float(row[0])
    Attrib02=float(row[1])
    Attrib03=float(row[2])
    Attrib04=float(row[3])
    if( Attrib03 <= 4.810000 ):
		 if( Attrib01 <= 4.370000 ):
			if( Attrib03 <= 3.750000 ):
				classLabel= 1
			else:
				classLabel= 0
		else:
			if( Attrib03 <= 2.220000 ):
				if( Attrib03 <= 1.510000 ):
					classLabel= 0
				else:
					if( Attrib02 <= 1.820000 ):
						classLabel= 0
					else:
						if( Attrib03 <= 1.930000 ):
							classLabel= 1
						else:
							classLabel= 0
			else:
				if( Attrib01 <= 5.390000 ):
					if( Attrib01 <= 5.220000 ):
						if( Attrib03 <= 2.850000 ):
							classLabel= 1
						else:
							if( Attrib01 <= 4.710000 ):
								classLabel= 0
							else:
								if( Attrib02 <= 2.030000 ):
									classLabel= 1
								else:
									if( Attrib03 <= 3.640000 ):
										classLabel= 1
									else:
										classLabel= 0
					else:
						classLabel= 0
				else:
					if( Attrib02 <= -0.370000 ):
						if( Attrib01 <= 6.220000 ):
							classLabel= 1
						else:
							classLabel= 0
					else:
						classLabel= 1
	else:
		if( Attrib01 <= 6.140000 ):
			classLabel= 0
		else:
			if( Attrib01 <= 6.750000 ):
				if( Attrib02 <= 6.240000 ):
					if( Attrib02 <= 3.720000 ):
						if( Attrib03 <= 6.650000 ):
							classLabel= 1
						else:
							classLabel= 0
					else:
						classLabel= 0
				else:
					classLabel= 1
			else:
				classLabel= 1
        return classLabel
if __name__=="__main__":
   readFile()
