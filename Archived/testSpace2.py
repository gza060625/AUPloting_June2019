import matplotlib.pyplot as plt

ax = [plt.subplot(2,2,i+1) for i in range(4)]

for a in ax:
    a.set_xticklabels([])
    a.set_yticklabels([])
    a.set_aspect('equal')

plt.subplots_adjust(wspace=0, hspace=0)
plt.show()