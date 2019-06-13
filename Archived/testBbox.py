import matplotlib.pyplot as plt
import matplotlib.transforms as mtransforms
import matplotlib.patches as mpatch
from matplotlib.patches import FancyBboxPatch

styles = mpatch.BoxStyle.get_styles()
spacing = 1.2

larrow=styles['larrow']

print(styles)

figheight = (spacing * len(styles) + .5)
fig = plt.figure(figsize=(4 / 1.5, figheight / 1.5))
fontsize = 0.3 * 72


#for i, stylename in enumerate(sorted(styles)):
    #fig.text(0.5, (spacing * (len(styles) - i) - 0.5) / figheight, stylename,
              #ha="center",
              #size=fontsize,
              #transform=fig.transFigure,
              #bbox=dict(boxstyle=stylename, fc="w", ec="k"))

#plt.show()