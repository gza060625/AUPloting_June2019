import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

# Make an example plot with two subplots...
fig = plt.figure()
from matplotlib.transforms import Bbox

ax1 = fig.add_subplot(2,1,1)
ax1.plot(range(10), 'b-')

ax2 = fig.add_subplot(2,1,2)
ax2.plot(range(20), 'r^')

# Save the full figure...
fig.savefig('full_figure.png')


ex=fig.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
print(ex)
print(type(ex))
print(ex.extents)

my_blit_box = Bbox.from_bounds(*ex.extents)
print(my_blit_box)


fig.savefig('full_figure2.png',bbox_inches=ex.expanded(1.1,1.2))




# Save just the portion _inside_ the second axis's boundaries
extent = ax2.get_window_extent().transformed(fig.dpi_scale_trans.inverted())

fig.savefig('ax2_figure.png', bbox_inches=extent)

# Pad the saved area by 10% in the x-direction and 20% in the y-direction
fig.savefig('ax2_figure_expanded.png', bbox_inches=extent.expanded(1.1, 1.2))