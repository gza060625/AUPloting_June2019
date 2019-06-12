import numpy as np
import matplotlib.pyplot as plt

import re


import datetime
import calendar

import glob, os

import collections

oneMinDataPath="/home/ebuntu3/#code/AUPloting_June2019/data/AUTUMNX_SALU_TGBO_2019_06_06_PT1M.txt"
tenLinesData="/home/ebuntu3/#code/AUPloting_June2019/data/testData10.txt"

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
   
  midnightUnix=findMidnightUnix(unix[0])
  
  stepsArray=np.arange(0,24,step)
  
  xTicks=stepsArray.copy()
  xTicks.fill(midnightUnix)
  xTicks=xTicks+(stepsArray*secondInHour)  
  
  xLabels=stepsArray.copy()
  xLabels=list(map(num2TimeStamp,stepsArray))
  
  return xTicks,xLabels

def setX(ax,unix,step=4):
  ticks,labels=findX(unix,step)

  ax.set_xticks(ticks)
  ax.set_xticklabels(labels)
  
  ax.set_xlim(findMidnightUnix(unix[0]),unix[0]+60*60*24)
  

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
  result=[]
  for path in paths:
    matchResult=matchAUTUMN(path)
    if matchResult:
      result.append([matchResult,path])
  return result

#########################################################################
##### 
#########################################################################
def timeStamp():
  return datetime.datetime.now().strftime("%H.%M.%S")
#########################################################################
##### 
#########################################################################
lineStyles=collections.deque(['-','--','-.',':'])


def drawOneRow(file,xA,yA,zA,setLabels=False):  
  lineStyle=lineStyles[0]
  lineStyles.rotate(1)
  print(lineStyle)
  yLenged={'fontname':'monospace',
           'backgroundcolor':'#e2e3e5',
            'fontweight':'bold',
            'url':"http://google.com",
            'fontsize':'12',
            #'position':(0,0)
            #'horizontalalignment ':'left'
            }  
  
  unix,x,y,z=filePath2AUTUM_1Min(file[1],7)
  xA.plot(unix,x,'b',linestyle=lineStyle)
  
  #xA.grid(True,color='g', linestyle='-')
  #xA.legend()

  #print(xA.get_xlim())
  yA.plot(unix,y,'r',linestyle=lineStyle)
  zA.plot(unix,x,'g',linestyle=lineStyle)
  #zA.set_ylabel()
  zA.set_ylabel(file[0], rotation=0, labelpad=25,**yLenged)
  #zA.yaxis.set_label_position("right")  
  #zA.yaxis.set_label_coords(-0.1,1.02)
  zA.yaxis.set_label_coords(1.08,0.75)
  
  
  if setLabels:
    setX(xA,unix,step=8)  #Need to factor out
    
    

  
 #-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol"; 
def stylePlot(fig,ax):
  
  titleStyle={'fontname':'monospace',
           'backgroundcolor':'#e2e3e5',
            'fontweight':'bold',
            'url':"http://google.com",
            'fontsize':'12',
            #'horizontalalignment ':'left'
            }  
  
  
  fig.set_facecolor('xkcd:mint green')
  
  rowNum,colNum=ax.shape
  
  
  
  for _,subplot in np.ndenumerate(ax):   
    
    subplot.set_facecolor('xkcd:salmon')
    subplot.spines['right'].set_visible(False)
    subplot.spines['top'].set_visible(False)  
    subplot.spines['bottom'].set_color('c')
    subplot.spines['bottom'].set_linewidth(3)
    subplot.spines['bottom'].set_linestyle("dashed")
    
    subplot.spines['left'].set_linewidth(3)
    #subplot.axes().get_xaxis().set_visible(True)
    
  for col in range(colNum):
    subplot=ax[rowNum-1][col]
    subplot.spines['bottom'].set_linewidth(3)
    subplot.spines['bottom'].set_visible(True) 
    subplot.spines['bottom'].set_linestyle("solid")
  
  ax[0][0].set_title("X-Field",pad=6,**titleStyle)
  ax[0][1].set_title("Y-Field",pad=6,**titleStyle)
  ax[0][2].set_title("Z-Field",pad=6,**titleStyle)
  
  
  
    
 

def drawPlot(path):
  plotTitleSyle={'fontname':'monospace',
           'backgroundcolor':'#e2e3e5',
            'fontweight':'bold',
            'url':"http://google.com",
            'fontsize':'12',
            #'position':(0,0)
            #'horizontalalignment ':'left'
            }    
  
  allFiles=findFiles(path,"*.txt")
  validFiles=validateDataFiles(allFiles)
  
  length=len(validFiles)
  
  fig,ax=plt.subplots(length,3,sharex=True, sharey=True,figsize=(12,length*1.2))  

  stylePlot(fig,ax)
  
  
  #fig.text(0.06, 0.5, 'common ylabel', ha='center', va='center', rotation='vertical')
  
  
  
  for i in range(length):
    if i!=0:
      drawOneRow(validFiles[i],*ax[i,:]) 
    else:
      drawOneRow(validFiles[i],*ax[i,:],setLabels=True)     
      
  #st=fig.suptitle("Title centered above all subplots", fontsize=14)
  #st.set_y(0.95)
  #fig.subplots_adjust(top=0.85)  
  #fig=figure(1)
  #plt.text(0.5, 0.95, 'test', horizontalalignment='center')
 

  
  superPlot=fig.add_subplot(111, frameon=False)
  superPlot.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
  #superPlot.grid(False) 
  #bbox=dict(facecolor='none', edgecolor='red', pad=0)
  plt.xlabel("testXlabel",**plotTitleSyle,labelpad=0)
  plt.ylabel("TestYLabel",**plotTitleSyle,labelpad=20)
  ax=plt.gca()
  ax.xaxis.set_label_coords(0.5,1.065)  
  #fig.suptitle('bold figure suptitle', fontsize=14, fontweight='bold',labelpad=20)
  #plt.ylabel.set_label_position('top')
  
  
  plt.tight_layout()  
  plt.subplots_adjust(wspace=0.1, hspace=0.05)   
  
  plt.savefig("test"+timeStamp()+".svg",dpi=300,format='svg', facecolor=fig.get_facecolor())
  plt.show()
  
  
  return None

#inputPath="/home/ebuntu3/#code/AUPloting_June2019/data/"
inputPath="/home/ebuntu3/#code/AUPloting_June2019/testData/"
drawPlot(inputPath)




