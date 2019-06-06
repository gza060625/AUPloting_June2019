import re

oneMinDataPath="/home/ebuntu3/#code/AUPloting_June2019/data/AUTUMNX_SALU_TGBO_2019_06_06_PT1M.txt"


def containLetter(line): 
  x = re.search("[a-zA-Z]", line)
  return True if x else False

def checkSegments(line,numSegments,delimiter=None):
  splitLine=line.split(delimiter)
  return True if (len(splitLine)==numSegments) else False
  
def validateLine(line,numSegments):
  return True if ((not containLetter(line)) and checkSegments(line,numSegments)) else False
    
    
    
def loadData(dataPath,numSegments,methodDiction=None,delimiter=None):
  file=open(dataPath,'r')
  for line in file:
    if validateLine(line,numSegments):      
      line=line.split(delimiter)
      
      
      
      
#line="2019-06-06 00:00:30.663 157     11237.35  216.91    57844.11  88888.00"

#print(containLetter(line))
#print(checkSegments(line,7))
#print(validateLine(line,7))


loadData(oneMinDataPath)


    
    