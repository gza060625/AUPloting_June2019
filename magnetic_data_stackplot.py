#!/usr/bin/python3

################################################################################
# magnetic_data_stackplot.py
# June 24, 2019
# Enson Guo
#
# Generate summary stack plot of all 1-minute magnetic data into a single
# image that can be quickly inspected.  Similar in structure to summary plot
# on NRCan's magnetic data website
#
# USAGE
# Plot TODAYs data for all sites in a project (AUTUMNX, AUTUMN)
# magnetic_data_stackplot.py <PROJECT> 
# magnetic_data_stackplot.py AUTUMNX
#
# Plot a specific date 
# magnetic_data_stackplot.py <PROJECT> <YYYY> <MM> <DD>
# magnetic_data_stackplot.py AUTUMNX 2019 02 29
#
# Plot a specific range of dates 
# magnetic_data_stackplot.py <PROJECT> <YYYY> <MM> <DD> <PROJECT> <YYYY> <MM> <DD>
# magnetic_data_stackplot.py AUTUMNX 2019 02 29 2019 02 29
# Note takes <PROJECT> as one parameter, but will plots both projects
################################################################################

import numpy as np
import matplotlib.pyplot as plt

import re
import datetime,calendar
import glob, os,sys
import collections

from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)

#########################################################################
##### Parameters
#########################################################################

AUTUMN_X_List=['SALU','AKUL','PUVR','INUK','KJPK','RADI','VLDR','STFL','SEPT','SCHF']
AUTUMN_List=['INUV','FSJ','SLL','LARG','ATH','LABC','REDR','ROTH','LETH']
requiredObsList=[]




inputPath="/autumndp/L3" 

outputPath="/home/enson/stackPlot_Testing_Enson/outputFolder"
# outputPath="/autumndp/L4"


#########################################################################
##### Style
#########################################################################

borderOut=2
borderIn=1
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
               'backgroundcolor':'#ffffff',
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
             'backgroundcolor':'#ffff00',
             'color':'#222B29',
             'fontweight':'bold',            
             'fontsize':'12',             
             #'bbox':dict(boxstyle=larrow)
        }  

xSubTitle=unit

canvasColor='#FFFFFF'
plotColor='#FFFFFF'
thickBorderColorV='#445753'
thickBorderColorH='#545654'
gridColor='#222B29'
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
  # print("loadData: {} ".format(len(resultArray)))   
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
  
  # print("extractInfoFromAUTUMN_1Min: {}".format(len(unix)))
  return unix,x,y,z

def filePath2AUTUM_1Min(path,numSegments):
  # print("TagA: {}".format(path))
  temp=loadData(path,numSegments)
  unix,x,y,z=extractInfoFromAUTUMN_1Min(temp)
  # print("filePath2AUTUM_1Min: {}".format(len(unix)))
  return unix,x,y,z

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
  ml = MultipleLocator(60*60)
  # plt.plot(a)
  # plt.axes().yaxis.set_minor_locator(ml)
  # plt.show()
  ax.xaxis.set_minor_locator(ml)
  # ax.xaxis.grid(True, which='minor')

  # ax.xaxis.set_minor_locator(ticks-100)

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
    subplot.grid(which='minor', alpha=0.5)
    subplot.grid(which='major', alpha=1,linestyle=':')
  
    
    # subplot.spines['right'].set_visible(False)
    
    # subplot.spines['top'].set_visible(False) 

    subplot.spines['top'].set_color(thickBorderColorH)
    subplot.spines['top'].set_linewidth(borderOut)
    subplot.spines['top'].set_linestyle("solid")
    
    subplot.spines['bottom'].set_color(thickBorderColorH)
    subplot.spines['bottom'].set_linewidth(borderOut)
    subplot.spines['bottom'].set_linestyle("solid")
    
    subplot.spines['left'].set_linewidth(borderOut)
    subplot.spines['left'].set_color(thickBorderColorV)

    subplot.spines['right'].set_linewidth(borderOut)
    subplot.spines['right'].set_color(thickBorderColorV)


    
  for col in range(colNum):
    subplot=ax[rowNum-1][col]
    subplot.spines['bottom'].set_linewidth(2)
    subplot.spines['bottom'].set_visible(True) 
    subplot.spines['bottom'].set_color(thickBorderColorV)
    subplot.spines['bottom'].set_linestyle("solid")
    
  
  ax[0][0].set_title("X-Field",pad=12,**xyzFieldStyle)
  ax[0][1].set_title("Y-Field",pad=12,**xyzFieldStyle)
  ax[0][2].set_title("Z-Field",pad=12,**xyzFieldStyle)
  
  firstCol=ax[:,0]
  for axis in firstCol:
    axis.set_ylabel("nt", labelpad=10,rotation=0,**unit) 

    
  lastRow=ax[-1,:] 
  for axis in lastRow: 
    axis.set_xlabel("UTC in Hours  "+dateStr,**xSubTitle)
    axis.tick_params(axis='x',which='minor',bottom=True,length=2,color='black',width=1)
    axis.tick_params(axis='x',which='major',bottom=True,length=6,color='black',width=2)

  firstRow=ax[0,:] 
  for axis in firstRow: 
    axis.spines['top'].set_visible(True) 
    axis.tick_params(axis='x',which='minor',top=True,length=2,color='black',width=1)
    axis.tick_params(axis='x',which='major',top=True,length=6,color='black',width=2)





    
  #############################Plot Titles################################# 
  #superPlot=fig.add_subplot(111, frameon=False)
  #superPlot.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
  #plt.xlabel("Magnetic Summary plots: "+dateStr,**titleStyle,labelpad=0)
  #plt.ylabel("TestYLabel",**titleStyle,labelpad=30)
  #ax=plt.gca()
  #ax.xaxis.set_label_coords(0.5,1.07)   
  ################################################################################ 
  
  
  #plt.tight_layout(pad=padding)
  plt.subplots_adjust(wspace=0.05, hspace=0.2)
  
def findPlotSize(l,k=1.1,b=2.5):
  return l*k+b

def drawOneRow(name,unix,x,y,z,xA,yA,zA,setLabels=False):
  
  colors=['k','r','b']  
  print("Plot Site:{}".format(name))
  xA.plot(unix,x,colors[0])  
  yA.plot(unix,y,colors[1])
  zA.plot(unix,z,colors[2])
  
  zA.set_ylabel(name, rotation=0, labelpad=0, verticalalignment='top',horizontalalignment='left',**legendObsName)  
  zA.yaxis.set_label_coords(1.02,1)
  
  ylbl = zA.yaxis.get_label()
  temp=ylbl.get_position()
  print(temp)

  props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
  zA.text(1.02, 0.55, "textstr", transform=zA.transAxes, fontsize=12,verticalalignment='top', horizontalalignment='left',bbox=props)
  # zA2 = zA.twinx()
  # zA2.xaxis.set_ticklabels([])
  # zA2.set_ylabel("ZA2", rotation=0, labelpad=30,**legendObsName)  
  # zA2.yaxis.set_label_coords(1,0.38)
  # zA.text(0.05, 0.95, "TEXTBOX", transform=zA.transAxes, fontsize=14,verticalalignment='top', bbox=props)

def checkAKUL(requiredObsList,year,month,day):
  year=int(year)
  month=int(month)
  day=int(day)
  requiredDay=datetime.datetime(year,month,day)
  cutoffDay=datetime.datetime(2016,4,25)
  if (requiredDay>cutoffDay) and 'AKUL' in requiredObsList:
    requiredObsList.remove('AKUL')
  return requiredObsList

def drawPlot(AUTU,year,month,day):
  #print("TestingMode: {} {} {} {}".format(AUTU,year,month,day))
  #return
  global requiredObsList
  requiredObsList=checkAKUL(requiredObsList,year,month,day)

  print("Working on {} {} {}".format(year,month,day))

  dateString="-".join([year,month,day])  
  txtInOneDay=findAllTxtInServer(year,month,day)
  
  
  length=len(requiredObsList)
  # fig,ax=plt.subplots(length,3,sharex=True, sharey=True,figsize=(18,findPlotSize(length)))  
  fig,ax=plt.subplots(length,3,sharex=True, sharey=True,figsize=(findPlotSize(length),length))  
  
  stylePlot(fig,ax,year,month,day)   

  counter=0
  for siteName in requiredObsList:  #To keep the sequence required
    if siteName in txtInOneDay: 
      unix,x,y,z=filePath2AUTUM_1Min(txtInOneDay[siteName],7)
      # print(siteName,' ',dateString)
      # print("Site: {} Unix: {} ".format(siteName,len(unix)))
      drawOneRow(siteName,unix,x,y,z,*ax[counter,:])
    else:
      drawOneRow(siteName,[],[],[],[],*ax[counter,:])
    counter=counter+1

  saveType="png"
  saveName="_".join([AUTU,"SUMMARY","TGBO",dateString,"PT1M","L4"])+"."+saveType
  path=findOutputPath(year,month,day,outputPath=outputPath)
  createOutputFolder(path)
  # path="/home/enson/stackPlot_Testing_Enson"
  savePath=os.path.join(path,saveName)
  plt.savefig(savePath,dpi=70,format=saveType, facecolor=fig.get_facecolor(),bbox_inches='tight')
  
  plt.close()
  

def findOutputPath(year,month,day,outputPath=outputPath):
  return os.path.join(outputPath,year,month,day)
def createOutputFolder(path):  
  os.makedirs(path, exist_ok=True)

def checkWithRequiredList(paths):
  result=[]
  for path in paths:
    if path in requiredObsList:
      result.append(path)
  return result
  

def findAllTxtInServer(year,month,day,path=inputPath):
  currentPath=os.getcwd() 
  os.chdir(path)
  
  result=dict()
  regExp=path+"/*"

  obsNames=[os.path.basename(file) for file in glob.glob(regExp)]
  obsNames=checkWithRequiredList(obsNames)  

  for name in obsNames:
    instrumentName=os.listdir(os.path.join(path,name))[0]
    
    folderPath=os.path.join(path,name,instrumentName,year,month,day)+"/*.txt"    
    txtFile=glob.glob(folderPath)
    if txtFile:
      result[name]=txtFile[0]

  os.chdir(currentPath)  
  return result






def checkArguments():
  global requiredObsList  
  
  # print(sys.argv)
  
  length=len(sys.argv)
  if length<2 or 2<length<5 or 5<length<8:    
    print("Invalid Input ")
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

  if length==2:
    date=datetime.datetime.utcnow()
    date=[date.year, date.month, date.day]
    date=list(map(strAndFill,date))
    arguments=[sys.argv[1]]+date
    drawPlot(*arguments)
    return     
  if length==5:
    arguments=sys.argv[1:2]+[str(int(x)).zfill(2) for x in sys.argv[2:5]]
    drawPlot(*arguments)
    return 
  
  if length==8:
    arguments=sys.argv[1:2]+[int(x) for x in sys.argv[2:8]]    
    callRangeOfDate(*arguments)
    
    return   
  
  return False

def callRangeOfDate(AUTU,ayear,amonth,aday,byear,bmonth,bday):
  global requiredObsList
  
  path=inputPath
  #counter=5
  #end=datetime.date.today()
  start=datetime.datetime(ayear,amonth,aday)
  end=datetime.datetime(byear,bmonth,bday)
  
  while start.date() <= end.date():    
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

  checkArguments()




