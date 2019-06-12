import matplotlib.pyplot as plt
import numpy as np

fig, axes = plt.subplots(3, 4, sharex=True, sharey=True)
# add a big axes, hide frame
fig.add_subplot(111, frameon=False)

t = np.arange(0.01, 5.0, 0.01)
s = np.exp(-t)
plt.plot(t, s)

# hide tick and tick label of the big axes
#plt.tick_params(labelcolor='none', top='off', bottom='off', left='off', right='off')
#plt.grid(False)
plt.xlabel("common X")
plt.ylabel("common Y")
ax=plt.gca()
ax.xaxis.set_label_coords(-0.1,1.02)

plt.show()