import matplotlib.pyplot as plt
import numpy as np

ax = plt.gca()
ax.set_xticks(np.arange(0,6,1))
ax.set_yticks(np.arange(0,6,1))
label = ax.set_xlabel('xlabel', ha='left', va = 'top', )#fontsize = 9)

# need to draw the figure first to position the tick labels
fig = plt.gcf()
fig.draw(fig.canvas.get_renderer())

# get a tick and will position things next to the last one
ticklab = ax.xaxis.get_ticklabels()[0]
trans = ticklab.get_transform()
ax.xaxis.set_label_coords(5.1, 0, transform=trans)

#plt.savefig('labelAtEnd2.png')
plt.show()