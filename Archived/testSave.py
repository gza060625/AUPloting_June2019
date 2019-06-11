import numpy as np
import matplotlib.pyplot as plt

import re


import datetime
import calendar

import glob, os

beingsaved = plt.figure()

# some scatters
plt.scatter(X_1_x, X_1_y)
plt.scatter(X_2_x, X_2_y)

beingsaved.savefig('destination_path.eps', format='eps', dpi=1000)