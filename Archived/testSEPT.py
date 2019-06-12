import numpy as np
import matplotlib.pyplot as plt

import re


import datetime
import calendar

import glob, os

import collections

from smallFunctions import *



path="/home/ebuntu3/#code/AUPloting_June2019/data/AUTUMNX_SEPT_TGBO_2019_06_10_PT1M.txt"

result=loadData(path,7)
unix,x,y,z=extractInfoFromAUTUMN_1Min(result)

plt.plot(unix,x)
print(unix)
plt.show()
