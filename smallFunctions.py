import re
import numpy as np

import datetime
import calendar

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
  
def str2Datetime(line,fmt="%Y-%m-%d %H:%M:%S"):
  return datetime.datetime.strptime(line,fmt)
  
  
def datetime2Unix(timeDate):  
  return calendar.timegm(timeDate.timetuple())
    
def loadData(dataPath,numSegments,delimiter=None):
  file=open(dataPath,'r')
  resultArray=[]
  for line in file:
    if validateLine(line,numSegments):      
      line=line.split(delimiter)
      resultArray.append(line)      
  return np.array(resultArray)
      
timeStr="2019-06-06 00:00:30"    
print(datetime2Unix(str2Datetime(timeStr)))
      
      
#line="2019-06-06 00:00:30.663 157     11237.35  216.91    57844.11  88888.00"








#s = "01/12/2011 01:01:01"
#temp=datetime.datetime.strptime(s, "%d/%m/%Y %H:%M:%S")
##temp=temp.replace(tzinfo=pytz.utc)
###print(datetime.datetime.strptime(s, "%d/%m/%Y %H:%M:%S %Z").timetuple())


##result=time.mktime(temp.timetuple())
###1322701261
##print(temp)
##print(result)


##test

##a1=datetime.datetime(2011, 12,1, 1, 1, 1, 0)
##print(a1)
#a2=calendar.timegm(temp.timetuple())
#print(a2)
    
    