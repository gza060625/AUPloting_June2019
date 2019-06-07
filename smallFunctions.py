import re
import numpy as np

oneMinDataPath="/home/ebuntu3/#code/AUPloting_June2019/data/AUTUMNX_SALU_TGBO_2019_06_06_PT1M.txt"
tenLinesData="/home/ebuntu3/#code/AUPloting_June2019/data/testData10.txt"


def containLetter(line): 
  x = re.search("[a-zA-Z]", line)
  return True if x else False

def checkSegments(line,numSegments,delimiter=None):
  splitLine=line.split(delimiter)
  return True if (len(splitLine)==numSegments) else False
  
def validateLine(line,numSegments):
  return True if ((not containLetter(line)) and checkSegments(line,numSegments)) else False
    
#def dataLine2Array(line,delimiter=None):
  #result=line.split(delimiter)
  #return result
  
    
def loadData(dataPath,numSegments,delimiter=None):
  file=open(dataPath,'r')
  resultArray=[]
  for line in file:
    if validateLine(line,numSegments):      
      line=line.split(delimiter)
      resultArray.append(line)
      
  return resultArray
      
      
      
      
line="2019-06-06 00:00:30.663 157     11237.35  216.91    57844.11  88888.00"

#print(containLetter(line))
#print(checkSegments(line,7))
#print(validateLine(line,7))
#print(dataLine2Array(line,7))
temp=loadData(tenLinesData,7)
a=np.array(temp)
for x in temp:
  print(x)
  
  
print(a[:,1])

#test


    
    