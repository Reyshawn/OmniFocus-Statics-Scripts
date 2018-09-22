from omnifocus import durations, dates
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

weekday = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
dates = dates[:120]

Matrix = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[]}
heatmap = []

# edge case, the start date is not Sunday
st = dates[0].weekday()
while st < 6:
    st += 1
    Matrix[st].append(0)

for i in range(len(dates)):
    Matrix[dates[i].weekday()].append(durations[i])

l = len(Matrix[6])
for i in range(len(Matrix)):
    if len(Matrix[i]) < l:
        Matrix[i].append(0) # the Matrix is not squared 
    heatmap.append(Matrix[i][::-1])

heatmap = np.array(heatmap)

ticks = {} # week number  -> month name
ticks[0] = months[dates[-1].month-1]
for i in range(1,len(dates)):
    if dates[-(i+1)].month == dates[-i].month:
        continue
    ticks[i // 7] = months[dates[-(i+1)].month-1]

cmap = mpl.cm.get_cmap('Greens', 10)

fig, ax = plt.subplots()
im = ax.imshow(heatmap, cmap=cmap)
cbar = ax.figure.colorbar(im, ax=ax)

ax.set_xticks(list(ticks.keys()))
ax.set_xticklabels(list(ticks.values()))
ax.set_yticks(np.arange(len(weekday)))
ax.set_yticklabels(weekday)

ax.set_xticks(np.arange(heatmap.shape[1]+1)-.5, minor=True)
ax.set_yticks(np.arange(heatmap.shape[0]+1)-.5, minor=True)
ax.grid(which="minor", color='k', linestyle='-', linewidth=0.5)
# ax.grid(which="minor", color='w', linestyle='-', linewidth=1) # the white edge color
ax.tick_params(which="minor", bottom=False, left=False)

plt.show()
