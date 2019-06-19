import numpy as np
import matplotlib.pyplot as plt

import re

import datetime,calendar

import glob, os,sys

import collections

from fonts import *

#############################

AUTUMN_X_List=['SALU','PUVR','INUK','KJPK','RADI','VLDR','STFL','SEPT','SCHF']
AUTUMN_List=['INUV','FSJ','SLL','LARG','ATH','LABG','ATH','LABC','REDR','ROTH','LETH']
AUTUMN_List=[]

inputPath="/autumndp/L3"  #Only when number of input argument is 1


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
  # print(dataPath)
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
  return array-np.average(array)


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
 
  
def findFilesInOneFOlder(path,regExp):
  currentPath=os.getcwd()  
  os.chdir(path) 
  
  result=[os.path.join(path,file) for file in glob.glob(regExp)]  
  
  os.chdir(currentPath)  
  return result

def validateFilesInOneFolder(paths):
  result=dict()
  for path in paths:
    matchResult=matchAUTUMN(path)
    if matchResult and matchResult in AUTUMN_X_List:      
      result[matchResult]=path
  return result

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
  
  #plt.autoscale()
  
def findSize(l,k=1.5,b=2.5):
  return l*k+b

def rejectOutliers(array):

  mask=[x<1000 for x in array[:,1]]
  array=array[mask]


  average=np.average(array[:,1])
  std=np.std(array[:,1])
  print(average)
  # print(average,std)
  limit=std*6
  mask=[ average-limit<=x<=average+limit for x in array[:,1]]
  # print(mask)
  return array[mask]

def findSDeviation(array):
  array=np.array(array) 
  array=rejectOutliers(array)
  # [print(x) for x in array]  
  
  numOfData=np.sum(array[:,0])   
  
  temp=[n*std*std for n,std in array] 
  SDeviation=np.sqrt(np.sum(temp)/(numOfData))
  
  print(SDeviation)
  return SDeviation

def drawOneRow(name,unix,x,y,z,xA,yA,zA,setLabels=False):
  
  #lineStyles=collections.deque(['-','--','-.',':'])
  #lineStyle=lineStyles[0]
  #lineStyles.rotate(1)

  colors=['b','r','g']  
  
  xA.plot(unix,x,colors[0])  
  yA.plot(unix,y,colors[1])
  zA.plot(unix,z,colors[2])
  
  zA.set_ylabel(name, rotation=0, labelpad=30,**legendObsName)  
  zA.yaxis.set_label_coords(1.10,0.68)


def drawPlot(path,year,month,day):

  dateString="-".join([year,month,day])  
  print("Working On: "+dateString)
  
  # allFiles=findFilesInOneFOlder(path,"*.txt")
  # validatedFiles=validateFilesInOneFolder(allFiles)  

  validatedFiles=findFilesInServer(path,year,month,day)  
  
  length=len(AUTUMN_X_List)  


  

  fig,ax=plt.subplots(length,3,sharex=True, sharey=True,figsize=(12,findSize(length)))  
  

  stylePlot(fig,ax,year,month,day)   


  counter=0
  for siteName in AUTUMN_X_List+AUTUMN_List:  #To keep the sequence required
    if siteName in validatedFiles: 
      unix,x,y,z=filePath2AUTUM_1Min(validatedFiles[siteName],7)
      print(siteName,' ',dateString)
      drawOneRow(siteName,unix,x,y,z,*ax[counter,:])
    else:
      drawOneRow(siteName,[],[],[],[],*ax[counter,:])
    counter=counter+1

  plt.savefig("./tempDir/StackPlot_"+dateString+timeStamp()+"."+saveType,dpi=300,format=saveType, facecolor=fig.get_facecolor(),bbox_inches='tight')
  
  plt.close()
  

def validateFile(paths):
  result=[]
  for path in paths:
    if path in AUTUMN_List+AUTUMN_X_List:
      result.append(path)
  return result
  

def findFilesInServer(path,year,month,day):
  currentPath=os.getcwd() 

  os.chdir(path)
  
  result=dict()
  regExp=path+"/*"

  obsNames=[os.path.basename(file) for file in glob.glob(regExp)]   
  obsNames=validateFile(obsNames)

  for name in obsNames:
    folderPath=os.path.join(path,name,"fluxgate",year,month,day)+"/*.txt"
    # print(folderPath)
    txtFile=glob.glob(folderPath)
    if txtFile:
      result[name]=txtFile[0]
  os.chdir(currentPath)
  # print(result)
  return result



def checkArguments(num=5):
  length=len(sys.argv)
  if length>=num:
    return sys.argv[1:5]
  if length==1:
    date=datetime.datetime.utcnow()
    date=[date.year, date.month, date.day]
    date=list(map(strAndFill,date))
    return [inputPath]+date    
  if length==4:
    return [inputPath]+sys.argv[1:4]
  return False

def callRangeOfDate():
  path=inputPath
  counter=5
  end=datetime.datetime(2019,6,14)

  for i in range(counter):
    print("Remains: "+str(counter-i))
    year=strAndFill(end.year)
    month=strAndFill(end.month)
    day=strAndFill(end.day)
    end=end-datetime.timedelta(1)

    arguments=[path,year,month,day]
    # print(arguments)
    drawPlot(*arguments)
  return None

def createFolder(dirName = 'tempDir' ):  
  try:
      # Create target Directory
      os.mkdir(dirName)
      print("Directory " , dirName ,  " Created ") 
  except FileExistsError:
      print("Directory " , dirName ,  " already exists")

if __name__ =="__main__": 



  # arguments=checkArguments()
  
  # path="/home/ebuntu3/#code/AUPloting_June2019/data0605"
  # path='/autumndp/L3/'
  # createFolder()
  # arguments=[path,"2019","06","05"]

  # print(arguments)
  # drawPlot(*arguments)
  # drawPlot(path,"2019","03","12")
  # drawPlot(path,"2019","04","10")
  # drawPlot(path,"2019","05","14")

  # callRangeOfDate()
  checkArguments()




