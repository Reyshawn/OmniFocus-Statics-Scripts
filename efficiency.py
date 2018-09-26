import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
from task import tasks


def get_freq(days):
    # accumulate total number of activities during each minute in past days
    END = tasks[0].date - timedelta(days)
    counter = {0:0}
    i = 0
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


def draw_bar(days):
    data = get_freq(days)
    k = sorted(list(data.keys()))
    res = [0]*(k[1])
    for i in range(1,len(k)-1):
        res += [data[k[i]]]*(k[i+1]-k[i])
    
    res += [0]*(1440 - k[-1])
    d = datetime(2018,1,1)

    fig, ax = plt.subplots()
    ax.plot(range(len(res)), res)
    
    ticks = {}
    for hour in range(24):
        ticks[hour*60] = hour
    

    ax.set_xticks(list(ticks.keys()))
    ax.set_xticklabels(list(ticks.values()))
    
    plt.show()
    

if __name__ == '__main__':
    draw_bar(30)