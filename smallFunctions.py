import numpy as np
import matplotlib.pyplot as plt

import re


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

def stripTimetoInteger(time):
  return time[:8]

def createDatetime(date,time):
  dateTime=date+' '+time  
  dateTime=str2Datetime(dateTime)
  return datetime2Unix(dateTime)  

def offsetByUTC00(array):
  return array-array[0]


def extractInfoFromAUTUMN_1Min(array):
  date=array[:,0]
  
  time=array[:,1]  
  vec_stripTimetoInteger=np.vectorize(stripTimetoInteger)
  time=vec_stripTimetoInteger(time)
  
  vec_createDatetime=np.vectorize(createDatetime)
  unix=vec_createDatetime(date,time) 
  
  vec_float=np.vectorize(float)
  x=vec_float(array[:,3])
  y=vec_float(array[:,4])
  z=vec_float(array[:,5]) 
  
  x=offsetByUTC00(x)
  y=offsetByUTC00(y)
  z=offsetByUTC00(z)  
  
  return unix,x,y,z


def num2TimeStamp(time):
  time=int(time)
  return '{0:02d}:00'.format(time)

def findX(unix,step):
  
  secondInHour=60*60
  
  firstData=unix[0]  
  midnightUnix=firstData-firstData%86400
  
  stepsArray=np.arange(0,24.001,step)
  
  xTicks=stepsArray.copy()
  xTicks.fill(midnightUnix)
  xTicks=xTicks+(stepsArray*secondInHour)
  
  print(xTicks)
  
  xLabels=stepsArray.copy()
  xLabels=list(map(num2TimeStamp,stepsArray))
  print(xLabels)
  
  return xTicks,xLabels

def setX(ax,unix,step=4):
  ticks,labels=findX(unix,step)
  ax.set_xticks(ticks)
  ax.set_xticklabels(labels)  
  
 

#inputPath="/home/ebuntu3/#code/AUPloting_June2019/data/testData10.txt"
inputPath="/home/ebuntu3/#code/AUPloting_June2019/data/AUTUMNX_SALU_TGBO_2019_06_06_PT1M.txt"
d=loadData(inputPath,7)
unix,x,y,z=extractInfoFromAUTUMN_1Min(d)

_,ax=plt.subplots(1,3)
ax[0].plot(unix,x)
ax[1].plot(unix,y)
ax[2].plot(unix,z)
#a,b=findX(unix)
#for label in ax.xaxis.get_ticklabels():
  #label.set_rotation(45)
#print(unix)
for a in ax:
  setX(a,unix,step=6)
  #a.set_xlim(0)

plt.show()