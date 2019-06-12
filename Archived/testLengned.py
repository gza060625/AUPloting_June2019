from smallFunctions import *

import numpy as np
import matplotlib.pyplot as plt

import re


import datetime
import calendar

import glob, os

import collections


 

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
      print("here")
      drawOneRow(validFiles[i],*ax[i,:],setLabels=True)     
      
  #st=fig.suptitle("Title centered above all subplots", fontsize=14)
  #st.set_y(0.95)
  #fig.subplots_adjust(top=0.85)  
  #fig=figure(1)
  #plt.text(0.5, 0.95, 'test', horizontalalignment='center')
 

  
  #superPlot=fig.add_subplot(111, frameon=False)
  #superPlot.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
  #superPlot.grid(False) 
  #bbox=dict(facecolor='none', edgecolor='red', pad=0)
  #plt.xlabel("Magnetic Summary plots: "+dateStr,**plotTitleSyle,labelpad=0)
  #plt.ylabel("TestYLabel",**plotTitleSyle,labelpad=30)
  #ax=plt.gca()
  #ax.xaxis.set_label_coords(0.5,1.07)  
  #fig.suptitle('bold figure suptitle', fontsize=14, fontweight='bold',labelpad=20)
  #plt.ylabel.set_label_position('top')
  
  
  plt.tight_layout()  
  plt.subplots_adjust(wspace=0.1, hspace=0.05)   
  
  
  
  #plt.text(0,1,"testText")
  plt.savefig("T"+timeStamp()+".svg",dpi=300,format='svg', facecolor=fig.get_facecolor())
  plt.show()
  
  
  return None

#inputPath="/home/ebuntu3/#code/AUPloting_June2019/data/"
#inputPath="/home/ebuntu3/#code/AUPloting_June2019/testData/"
inputPath="/home/ebuntu3/#code/AUPloting_June2019/data0606/"
drawPlot(inputPath)