from smallFunctions import *

import numpy as np
import matplotlib.pyplot as plt

import re


import datetime
import calendar

import glob, os

import collections




    
  
def stylePlot(fig,ax):
  

  
  rowNum,colNum=ax.shape
  
  fig.set_facecolor('xkcd:mint green')  
  
  
  for _,subplot in np.ndenumerate(ax):   
    
    subplot.set_facecolor('xkcd:salmon')
    
    subplot.spines['right'].set_visible(False)
    
    subplot.spines['top'].set_visible(False) 
    
    subplot.spines['bottom'].set_color('c')
    subplot.spines['bottom'].set_linewidth(3)
    subplot.spines['bottom'].set_linestyle("dashed")
    
    subplot.spines['left'].set_linewidth(3)
    subplot.spines['left'].set_color('c')
    
  for col in range(colNum):
    subplot=ax[rowNum-1][col]
    subplot.spines['bottom'].set_linewidth(3)
    subplot.spines['bottom'].set_visible(True) 
    subplot.spines['bottom'].set_linestyle("solid")
    
  
  ax[0][0].set_title("X-Field",pad=8,**titleStyle)
  ax[0][1].set_title("Y-Field",pad=8,**titleStyle)
  ax[0][2].set_title("Z-Field",pad=8,**titleStyle)
  
  firstCol=ax[:,0]
  for axis in firstCol:
    axis.set_ylabel("nt", labelpad=12,**titleStyle)

    
  lastRow=ax[-1,:] 
  for axis in lastRow: 
    axis.set_xlabel("UTC in Hours  "+dateStr)
    
    
    
  plt.tight_layout()  
  plt.subplots_adjust(wspace=0.1, hspace=0.05)
  
    
 

def drawPlot(path):
  
  allFiles=findFiles(path,"*.txt")
  validFiles=validateDataFiles(allFiles)
  
  length=len(validFiles)
  
  fig,ax=plt.subplots(length,3,sharex=True, sharey=True,figsize=(12,length*1.2))  

  stylePlot(fig,ax) 
  
   
  for i in range(length):
    if i!=0:
      drawOneRow(validFiles[i],*ax[i,:]) 
    else:      
      drawOneRow(validFiles[i],*ax[i,:],setLabels=True)
  
  plt.savefig("T"+timeStamp()+".svg",dpi=300,format='svg', facecolor=fig.get_facecolor())
  plt.show()

if __name__ =="__main__":
  inputPath="/home/ebuntu3/#code/AUPloting_June2019/data0606/"
  #inputPath="/home/ebuntu3/#code/AUPloting_June2019/testData/"
  #inputPath="/home/ebuntu3/#code/AUPloting_June2019/testData2/"
  drawPlot(inputPath)