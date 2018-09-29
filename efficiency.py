import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from datetime import datetime, timedelta
from task import tasks



def get_freq(days, START=None):
    # accumulate total number of activities during each minute in past days
    i = 0
    if START:
        START = datetime.strptime(START, '%Y.%m.%d').date()
        while (tasks[i].date != START):
            i += 1
    END = tasks[i].date - timedelta(days)
    counter = {0:0}
    
    while (tasks[i].date != END):
        temp = {}
        for t in range(0,len(tasks[i].time), 2):
            temp[tasks[i].time[t].hour*60+tasks[i].time[t].minute] = 1
            temp[tasks[i].time[t+1].hour*60+tasks[i].time[t+1].minute] = 0
        counter = count_merge(counter, temp)
        i += 1
    return counter


def count_merge(c, t):
    if len(c) == 1:
        return {**c, **t}
    c_ = sorted(list(c.keys()))
    t_ = sorted(list(t.keys()))
    j = 0
    for i in range(0, len(t_), 2):
        if c_[-1] < t_[i]:
            return {**c, **t}
        while (c_[j] < t_[i] ):
            j += 1
        c[t_[i]] = c[c_[j-1]] + 1
        c_.insert(j,t_[i])
        j += 1
        while (c_[j] <= t_[i+1]):
            c[c_[j]] += 1
            j += 1
            if j == len(c_):
                break
        c[t_[i+1]] = c[c_[j-1]] - 1
        c_.insert(j,t_[i+1])
        j += 1
    return c


def draw_bar(days, START=None):
    data = get_freq(days, START)
    k = sorted(list(data.keys()))
    res = [0]*(k[1])
    for i in range(1,len(k)-1):
        res += [data[k[i]]]*(k[i+1]-k[i])
    res += [0]*(1440 - k[-1])

    x = np.array(list(range(len(res))))
    y = np.array(res)

    fig, ax = plt.subplots()
    
    colors = cm.YlGnBu(y / float(max(y)))
    ax.bar(x, y,  width=1.0, color=colors)
    
    ticks = {}
    for hour in range(0,24,3):
        ticks[hour*60] = '{}:00'.format(hour)
    ticks[24*60] = '0:00'

    ax.set_xticks(list(ticks.keys()))
    ax.set_xticks(list(range(0,24*60,60)), minor=True)
    ax.set_xticklabels(list(ticks.values()))

    ax.grid(b=True, which='minor', axis='x', linestyle='dotted')

    ax.set_xlim(6*60, 24*60)
    
    plt.show()
    

if __name__ == '__main__':
    draw_bar(14, '2018.9.28')