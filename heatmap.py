import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from task import tasks

WEEKDAY = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
MONTH = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

def get_daily_dura(tasks):
    durations = []
    dates = []
    for task in tasks:        
        if task.date in dates:
            if len(task.duration) > 0:
                durations[-1] += int(task.duration[:-1])
        else:
            dates.append(task.date)
            durations.append(0)
            if len(task.duration) > 0:
                durations[-1] += int(task.duration[:-1])
    durations = [d/60 for d in durations]
    return dates, durations


def get_heatmap(days):
    Matrix = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[]}
    heatmap = []

    dates, durations = get_daily_dura(tasks)
    dates = dates[:days]

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

    return heatmap, dates


def draw_heatmap(days):
    heatmap, dates = get_heatmap(days)
    ticks = {} # week number  -> month name
    ticks[0] = MONTH[dates[-1].month-1]
    for i in range(1,len(dates)):
        if dates[-(i+1)].month == dates[-i].month:
            continue
        ticks[i // 7] = MONTH[dates[-(i+1)].month-1]

    cmap = mpl.cm.get_cmap('Greens', 10)

    fig, ax = plt.subplots()
    im = ax.imshow(heatmap, cmap=cmap)
    cbar = ax.figure.colorbar(im, ax=ax)

    ax.set_xticks(list(ticks.keys()))
    ax.set_xticklabels(list(ticks.values()))
    ax.set_yticks(np.arange(len(WEEKDAY)))
    ax.set_yticklabels(WEEKDAY)

    ax.set_xticks(np.arange(heatmap.shape[1]+1)-.5, minor=True)
    ax.set_yticks(np.arange(heatmap.shape[0]+1)-.5, minor=True)
    ax.grid(which="minor", color='k', linestyle='-', linewidth=0.5)
    # ax.grid(which="minor", color='w', linestyle='-', linewidth=1) # the white edge color
    ax.tick_params(which="minor", bottom=False, left=False)

    plt.show()


if __name__ == '__main__':
    draw_heatmap(120)
