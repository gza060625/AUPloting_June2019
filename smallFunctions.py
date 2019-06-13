import numpy as np
import matplotlib.pyplot as plt

import re


import datetime
import calendar

import glob, os

import collections

from fonts import *

#############################

AUTUMN_X_List=['SALU','PUVR','INUK','KJPK','RADI','VLDR','STFL','SEPT','SCHF']
AUTUMN_List=['INUV','FSJ','SLL','LARG','ATH','LABG','ATH','LABC','REDR','ROTH','LETH']





dateStr="2019 06 06"

#########################################################################
##### Extract File to Data
#########################################################################
def containLetter(line): 
  x = re.search("[a-zA-Z]", line)
  return True if x else False

def checkSegments(line,numSegments,delimiter=None):
  splitLine=line.split(delimiter)
  return True if (len(splitLine)==numSegments) else False
  
def validateLine(line,numSegments):
  return True if ((not containLetter(line)) and checkSegments(line,numSegments)) else False
    
  
def str2Datetime(line,fmt="%Y-%m-%d %H:%M:%S"):
  return datetime.datetime.strptime(line,fmt)  
  
def datetime2Unix(timeDate):  
  return calendar.timegm(timeDate.timetuple())
    
def loadData(dataPath,numSegments,delimiter=None):
  print(dataPath)
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

def filePath2AUTUM_1Min(path,numSegments):
  temp=loadData(path,numSegments)
  return extractInfoFromAUTUMN_1Min(temp)

#########################################################################
##### Lables
#########################################################################

def num2TimeStamp(time):
  time=int(time)
  return '{0:02d}:00'.format(time)

def findMidnightUnix(unix):
  return unix-unix%86400

def findX(unix,step):
  
  secondInHour=60*60  
   
  #midnightUnix=findMidnightUnix(unix[0])
  midnightUnix=unix
  
  stepsArray=np.arange(0,24,step)
  
  xTicks=stepsArray.copy()
  xTicks.fill(midnightUnix)
  xTicks=xTicks+(stepsArray*secondInHour)  
  
  xLabels=stepsArray.copy()
  xLabels=list(map(num2TimeStamp,stepsArray))
  
  return xTicks,xLabels

def setX(ax,dateStr,step=4):
  
  temp=str2Datetime(dateStr,fmt="%Y %m %d")
  unix=datetime2Unix(temp)
  
  ticks,labels=findX(unix,step) 
  

  ax.set_xticks(ticks)
  ax.set_xticklabels(labels)    
  
  ax.set_xlim(unix,unix+60*60*24)
  
  


#########################################################################
##### File Management
#########################################################################

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
  result=dict()
  for path in paths:
    matchResult=matchAUTUMN(path)
    if matchResult and matchResult in AUTUMN_X_List:      
      result[matchResult]=path

  return result

#########################################################################
##### 
#########################################################################
def timeStamp():
  return datetime.datetime.now().strftime("%_d.%H.%M.%S")
#########################################################################
##### 
#########################################################################

lineStyles=collections.deque(['-','--','-.',':'])

def drawOneRow(name,path,xA,yA,zA,setLabels=False):
  
  colors=['b','r','g']
  
  lineStyle=lineStyles[0]
  lineStyles.rotate(1)
  

  
  unix,x,y,z=filePath2AUTUM_1Min(path,7)
  
  xA.plot(unix,x,colors[0],linestyle=lineStyle)  
  yA.plot(unix,y,colors[1],linestyle=lineStyle)
  zA.plot(unix,x,colors[2],linestyle=lineStyle)
  
  zA.set_ylabel(name, rotation=0, labelpad=30,**legendObsName)
  
  zA.yaxis.set_label_coords(1.10,0.68)  
  
  #if setLabels:
    #setX(xA,unix,step=8)  #Need to factor out
    
  
def stylePlot(fig,ax):
 

  rowNum,colNum=ax.shape
  
  fig.set_facecolor(canvasColor)  
  
  setX(ax[0][0],dateStr,step=6)
  
  
  for _,subplot in np.ndenumerate(ax):   
    
    subplot.set_facecolor(plotColor)
    
    subplot.grid(color=gridColor)
    
    subplot.spines['right'].set_visible(False)
    
    subplot.spines['top'].set_visible(False) 
    
    subplot.spines['bottom'].set_color(thickBorderColorH)
    subplot.spines['bottom'].set_linewidth(3)
    subplot.spines['bottom'].set_linestyle("dashed")
    
    subplot.spines['left'].set_linewidth(3)
    subplot.spines['left'].set_color(thickBorderColorV)
    
  for col in range(colNum):
    subplot=ax[rowNum-1][col]
    subplot.spines['bottom'].set_linewidth(3)
    subplot.spines['bottom'].set_visible(True) 
    subplot.spines['bottom'].set_color(thickBorderColorV)
    subplot.spines['bottom'].set_linestyle("solid")
    
  
  ax[0][0].set_title("X-Field",pad=8,**xyzFieldStyle)
  ax[0][1].set_title("Y-Field",pad=8,**xyzFieldStyle)
  ax[0][2].set_title("Z-Field",pad=8,**xyzFieldStyle)
  
  firstCol=ax[:,0]
  for axis in firstCol:
    axis.set_ylabel("nt", labelpad=8,rotation=0,**unit)

    
  lastRow=ax[-1,:] 
  for axis in lastRow: 
    axis.set_xlabel("UTC in Hours  "+dateStr,**xSubTitle)
    
  #############################Plot Titles################################# 
  #superPlot=fig.add_subplot(111, frameon=False)
  #superPlot.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
  #plt.xlabel("Magnetic Summary plots: "+dateStr,**titleStyle,labelpad=0)
  #plt.ylabel("TestYLabel",**titleStyle,labelpad=30)
  #ax=plt.gca()
  #ax.xaxis.set_label_coords(0.5,1.07)   
  ################################################################################ 
  
  
  #plt.tight_layout(pad=padding)
  plt.subplots_adjust(wspace=0.05, hspace=0.01)
  
  #plt.autoscale()
  
def findSize(l,k=1.5,b=2.5):
  return l*k+b
 

def drawPlot(path):
  
  # allFiles=findFiles(path,"*.txt")
  # validFiles=validateDataFiles(allFiles)

  validFiles=findFiles2(path)
  printDictionary(validFiles)

  
  length=len(validFiles)  
  

  fig,ax=plt.subplots(length,3,sharex=True, sharey=True,figsize=(12,findSize(length)))  
  
  if ax.ndim ==1:
    ax=ax.reshape((1,3))  

  stylePlot(fig,ax) 
  

    
  
  
  counter=0
  for siteName in AUTUMN_X_List+AUTUMN_List:
    if siteName in validFiles:      
      drawOneRow(siteName,validFiles[siteName],*ax[counter,:]) 
      counter=counter+1
   

  
  plt.savefig("T"+timeStamp()+".svg",dpi=300,format='svg', facecolor=fig.get_facecolor())
  plt.show()


  # def findFiles(path,regExp):
  # currentPath=os.getcwd()  
  # os.chdir(path) 
  
  # result=[os.path.join(path,file) for file in glob.glob(regExp)]  
  
  # os.chdir(currentPath)  
  # return result

def validateFile(paths):
  result=[]
  for path in paths:
    if path in AUTUMN_List+AUTUMN_X_List:
      result.append(path)
  return result
  

def findFiles2(path,year="2019", mon="06", day="06"):
  currentPath=os.getcwd() 

  os.chdir(path)
  
  result=dict()
  regExp=path+"/*"

  obsNames=[os.path.basename(file) for file in glob.glob(regExp)]   
  obsNames=validateFile(obsNames)

  for name in obsNames:
    folderPath=os.path.join(path,name,"fluxgate",year,mon,day)+"/*.txt"
    # print(folderPath)
    txtFile=glob.glob(folderPath)
    if txtFile:
      result[name]=txtFile[0]

 

  os.chdir(currentPath)
  return result

def printDictionary(d):
  for key,val in d.items():
      print (key, "=>", val)


if __name__ =="__main__":
  # inputPath="./data0606/"
  inputPath="/autumndp/L3"
  # r=findFiles2(inputPath)
  # print(r)
  drawPlot(inputPath)




