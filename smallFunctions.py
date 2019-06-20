import numpy as np
import matplotlib.pyplot as plt

import re

import datetime,calendar

import glob, os,sys

import collections

from fonts import *

#########################################################################
##### Parameters
#########################################################################

AUTUMN_X_List=['SALU','PUVR','INUK','KJPK','RADI','VLDR','STFL','SEPT','SCHF']
AUTUMN_List=['INUV','FSJ','SLL','LARG','ATH','LABG','ATH','LABC','REDR','ROTH','LETH']
requiredObsList=[]


inputPath="/autumndp/L3" 

outputPath="/home/enson/stackPlot_Testing_Enson/outputFolder"

#########################################################################
##### Style
#########################################################################
padding=2

saveType="png"

titleStyle={'fontname':'monospace',
          'backgroundcolor':'#e2e3e5',
       'fontweight':'bold',
        'url':"http://google.com",
        'fontsize':'12'           
        } 

xyzFieldStyle={'fontname':'monospace',
               'color':'#222B29',
               'backgroundcolor':'#F4F7F7',
               'fontweight':'bold',
               'url':"http://google.com",
               'fontsize':'12'      
        } 

unit={'fontname':'monospace',
          #'backgroundcolor':'#e2e3e5',
       #'fontweight':'bold',        
        'fontsize':'10'           
        } 

legendObsName={'fontname':'monospace',
             'backgroundcolor':'#222B29',
             'color':'#E1EAE8',
             'fontweight':'bold',            
             'fontsize':'12',
             #'bbox':dict(boxstyle=larrow)
        }  

xSubTitle=unit

canvasColor='#F4F7F7'
plotColor='#A6C2BC'
thickBorderColorV='#445753'
thickBorderColorH='#F4F8F5'
gridColor='#C8D9CD'
tickColor=gridColor

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
  # print("resultArray: {} ".format(len(resultArray)))   
  return np.array(resultArray)

def stripTimetoInteger(time):
  return time[:8]

def createDatetime(date,time):
  dateTime=date+' '+time  
  dateTime=str2Datetime(dateTime)
  return datetime2Unix(dateTime)  

def offsetByUTC00(array):
  return array-np.average(array)


def extractInfoFromAUTUMN_1Min(array):
  # print(len(array))
  if len(array)==0:
    return [],[],[],[]
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
  # print(path)
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

  midnightUnix=unix
  
  stepsArray=np.arange(0,24,step)
  
  xTicks=stepsArray.copy()
  xTicks.fill(midnightUnix)
  xTicks=xTicks+(stepsArray*secondInHour)  
  
  xLabels=stepsArray.copy()
  xLabels=list(map(num2TimeStamp,stepsArray))
  
  return xTicks,xLabels

def setX(ax,date,step=4): 
  
  unix=datetime2Unix(date)

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
  


#########################################################################
#####Auxilary 
#########################################################################
def timeStamp():
  return ''
  return datetime.datetime.now().strftime(".%H.%M.%S")

def printDictionary(d):
  for key,val in d.items():
      print (key, "=>", val)

def strAndFill(x):
  x=str(x)
  x=x.zfill(2)
  return x

#########################################################################
##### Drawing
#########################################################################    
  
def stylePlot(fig,ax,year,month,day):
 
  dateStr=" ".join([year,month,day])
  rowNum,colNum=ax.shape
  
  fig.set_facecolor(canvasColor)  
  
  currentDate=str2Datetime(dateStr,fmt="%Y %m %d")
  setX(ax[0][0],currentDate,step=6)
  
  
  for _,subplot in np.ndenumerate(ax):   
    
    subplot.set_facecolor(plotColor)
    
    subplot.grid(color=gridColor)
    
    subplot.spines['right'].set_visible(False)
    
    subplot.spines['top'].set_visible(False) 
    
    subplot.spines['bottom'].set_color(thickBorderColorH)
    subplot.spines['bottom'].set_linewidth(6)
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
    axis.set_ylabel("nt", labelpad=10,rotation=0,**unit)

    
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
  plt.subplots_adjust(wspace=0.05, hspace=0.12)
  
def findSize(l,k=1.5,b=2.5):
  return l*k+b

def drawOneRow(name,unix,x,y,z,xA,yA,zA,setLabels=False):
  
  colors=['b','r','g']  
  
  xA.plot(unix,x,colors[0])  
  yA.plot(unix,y,colors[1])
  zA.plot(unix,z,colors[2])
  
  zA.set_ylabel(name, rotation=0, labelpad=30,**legendObsName)  
  zA.yaxis.set_label_coords(1.10,0.68)


def drawPlot(AUTU,year,month,day):

  print("Working on {} {} {}".format(year,month,day))

  dateString="-".join([year,month,day])  

  validatedFiles=findFilesInServer(year,month,day)
  
  length=len(requiredObsList) 

  fig,ax=plt.subplots(length,3,sharex=True, sharey=True,figsize=(12,findSize(length)))  
  
  stylePlot(fig,ax,year,month,day)   

  counter=0
  for siteName in requiredObsList:  #To keep the sequence required
    if siteName in validatedFiles: 
      unix,x,y,z=filePath2AUTUM_1Min(validatedFiles[siteName],7)
      # print(siteName,' ',dateString)
      drawOneRow(siteName,unix,x,y,z,*ax[counter,:])
    else:
      drawOneRow(siteName,[],[],[],[],*ax[counter,:])
    counter=counter+1

  saveType="png"
  saveName="_".join([AUTU,"SUMMARY","TGBO",dateString,"PT1M","L4"])+"."+saveType
  path=findOutputPath(year,month,day,outputPath=outputPath)
  createOutputFolder(path)
  savePath=os.path.join(path,saveName)
  plt.savefig(savePath,dpi=300,format=saveType, facecolor=fig.get_facecolor(),bbox_inches='tight')
  
  plt.close()
  

def findOutputPath(year,month,day,outputPath=outputPath):
  return os.path.join(outputPath,year,month,day)
def createOutputFolder(path):  
  os.makedirs(path, exist_ok=True)

def validateFile(paths):
  result=[]
  for path in paths:
    if path in requiredObsList:
      result.append(path)
  return result
  

def findFilesInServer(year,month,day,path=inputPath):
  currentPath=os.getcwd() 
  os.chdir(path)
  
  result=dict()
  regExp=path+"/*"

  obsNames=[os.path.basename(file) for file in glob.glob(regExp)]
  obsNames=validateFile(obsNames)  

  for name in obsNames:
    instrumentName=os.listdir(os.path.join(path,name))[0]
    
    folderPath=os.path.join(path,name,instrumentName,year,month,day)+"/*.txt"    
    txtFile=glob.glob(folderPath)
    if txtFile:
      result[name]=txtFile[0]

  os.chdir(currentPath)  
  return result





def checkArguments(num=5):
  global requiredObsList
  
  length=len(sys.argv)
  if length<2:
    print("Not enough input parameters")
    return False
  
  
  if sys.argv[1] == "AUTUMN":
    print("{} selected.".format(sys.argv[1]))
    requiredObsList=AUTUMN_List    
  elif sys.argv[1] =="AUTUMNX":
    print("{} selected.".format(sys.argv[1]))
    requiredObsList=AUTUMN_X_List
  else:
    print("Invalid input {}".format(sys.argv[1]))
    return False
    
    
  #if length>=num:
    #return sys.argv[1:5]
  if length==2:
    date=datetime.datetime.utcnow()
    date=[date.year, date.month, date.day]
    date=list(map(strAndFill,date))
    return [sys.argv[1]]+date    
  if length==5:
    return sys.argv[1:5]
  
  return False

def callRangeOfDate():
  global requiredObsList
  path=inputPath
  counter=5
  end=datetime.date.today()
  start=datetime.datetime(1999,5,1)
  
  while start.date() <= end:    
    year=strAndFill(start.year)
    month=strAndFill(start.month)
    day=strAndFill(start.day)   
    
    start=start+datetime.timedelta(1)
    
    arguments=["AUTUMN",year,month,day]
    requiredObsList=AUTUMN_List    
    drawPlot(*arguments)

    arguments=["AUTUMNX",year,month,day]
    requiredObsList=AUTUMN_X_List   
    drawPlot(*arguments)

  return None

def createFolder(dirName):  
  try:
      # Create target Directory
      os.mkdir(dirName)
      print("Directory " , dirName ,  " Created ") 
  except FileExistsError:
      print("Directory " , dirName ,  " already exists")

if __name__ =="__main__": 
  callRangeOfDate()
  # res=checkArguments()
  # drawPlot(*res)




