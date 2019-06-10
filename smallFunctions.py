import numpy as np
import matplotlib.pyplot as plt

import re


import datetime
import calendar

import glob, os

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

def filePath2AUTUM_1Min(path):
  temp=loadData(path,7)
  return extractInfoFromAUTUMN_1Min(temp)


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
  print(ticks)
  print(labels)
  ax.set_xticks(ticks)
  ax.set_xticklabels(labels)  



def matchAUTUMN(s):
  regExp=r'.*AUTUMN.?_([a-zA-Z]*)_.*'
  matchObj = re.match( regExp, s) 
  if matchObj:    
    return matchObj.group(1)
  else:
    return False
 
  
def findFiles(path,regExp):
  currentPath=os.getcwd()  
  os.chdir(path) 
  
  result=[os.path.join(path,file) for file in glob.glob(regExp)]  
  
  os.chdir(currentPath)  
  return result

def validateDataFiles(paths):
  result=[]
  for path in paths:
    matchResult=matchAUTUMN(path)
    if matchResult:
      result.append([matchResult,path])
  return result


def drawOneRow(file,xA,yA,zA):    
  unix,x,y,z=filePath2AUTUM_1Min(file[1])
  xA.plot(unix,x)
  yA.plot(unix,y)
  zA.plot(unix,x)
 

def drawPlot(path):
  
  allFiles=findFiles("./data","*.txt")
  validFiles=validateDataFiles(allFiles)
  
  length=len(validFiles)
  
  fig,ax=plt.subplots(length,3,sharex=True, sharey=True)
  
  for i in range(length):
    drawOneRow(validFiles[i],*ax[i,:]) 
  
  
  return None

inputPath="/home/ebuntu3/#code/AUPloting_June2019/data/"
drawPlot(inputPath)
plt.show()
##inputPath="/home/ebuntu3/#code/AUPloting_June2019/data/testData10.txt"
#inputPath="/home/ebuntu3/#code/AUPloting_June2019/data/AUTUMNX_SALU_TGBO_2019_06_06_PT1M.txt"
#d=loadData(inputPath,7)
#unix,x,y,z=extractInfoFromAUTUMN_1Min(d)

#_,ax=plt.subplots(3,3,sharex=True, sharey=True)

##ax[0,0].plot(unix,x)
##ax[0,1].plot(unix,y)
##ax[0,2].plot(unix,z)
###a,b=findX(unix)
###for label in ax.xaxis.get_ticklabels():
  ###label.set_rotation(45)
###print(unix)
##for a in ax[0,:]:
  ##setX(a,unix,step=6)
  ###a.set_xlim(0)
#r=findFiles("./data","*.txt")
#r=validateDataFiles(r)
#drawOneRow(r[0],*ax[0,:])
#plt.show()



#line="/home/ebuntu3/#code/AUPloting_June2019/data/AUTUMNX_SALU_TGBO_2019_06_06_PT1M.txt"
#line="/home/ebuntu3/#code/AUPloting_June2019/data/AUTUMNX_PUVR_TGBO_2019_06_06_PT1M.txt"
#print(matchAUTUMN(line))


