import matplotlib.pyplot as plt

a = plt.subplot()


a.set_xticklabels([])
a.set_yticklabels([])
a.set_aspect('equal')



csfont = {'fontname':'Comic Sans MS'}
hfont = {'fontname':'Helvetica'}
yLenged={'fontname':'BlinkMacSystemFont',
          'backgroundcolor':'#e2e3e5',
          'fontweight':'bold',
          #'url':"http://google.com"
        'ha ':'left'
          }

plt.title('SALU',**yLenged)
plt.xlabel('xlabel', **hfont)
plt.savefig('test2.svg')
plt.show()