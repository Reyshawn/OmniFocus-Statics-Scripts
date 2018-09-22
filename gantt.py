import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib as mpl
from datetime import datetime, timedelta
from task import tasks

# support the display of Chinese and Japanese characters 
from matplotlib.font_manager import FontProperties
font = FontProperties(fname='/System/Library/Fonts/Hiragino Sans GB.ttc')

# define the global value, colors, months 
COLORS = ['orange', 'gold', 'coral', 'c', 'deeppink', 'darkcyan', 'deepskyblue']
MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

def get_dailytasks(day, tasks=tasks):
    # choose a day to display the gantt chart of your activities in omnifocus
    # check if the type of day is string or datetime object 
    if not isinstance(day, datetime):
        _DAY = datetime.strptime(day, '%Y.%m.%d').date()
    else:
        _DAY = day.date()
    
    i = 0
    daily_tasks = []

    while (tasks[i].date != _DAY):
        i += 1

    while (tasks[i].date == _DAY):
        daily_tasks.append(tasks[i])
        i += 1
    return daily_tasks


def get_dict(day, onedate=False):
    daily_tasks = get_dailytasks(day)
    dict_gantt = {}

    # convert the datetime object to numeric number
    for i in range(len(daily_tasks)):
        if len(daily_tasks[i].time) > 1:
            if onedate:
                daily_tasks[i].time = [datetime.combine(datetime(2018,1,1).date(),t.time())for t in daily_tasks[i].time]
            dict_gantt[daily_tasks[i].title] = [mdates.date2num(t) for t in daily_tasks[i].time]
    
    # [start1,end1,start2,end2] => [(start1,end1), (start2, end2)]
    for i, title in enumerate(dict_gantt):
        temp = []
        for j in range(0, len(dict_gantt[title]), 2):
            # if the task hasn't been finished until tomorrow 
            if (dict_gantt[title][j+1] < dict_gantt[title][j]):
                next_day = mdates.num2date(dict_gantt[title][j+1]) + timedelta(days=1)
                dict_gantt[title][j+1] = mdates.date2num(next_day)

            if (j > 1) and (dict_gantt[title][j] < dict_gantt[title][j-1]):
                next_day = mdates.num2date(dict_gantt[title][j]) + timedelta(days=1)
                dict_gantt[title][j] = mdates.date2num(next_day)
                nnext_day = mdates.num2date(dict_gantt[title][j+1]) + timedelta(days=1)
                dict_gantt[title][j+1] = mdates.date2num(nnext_day)

            temp.append((dict_gantt[title][j], dict_gantt[title][j+1] - dict_gantt[title][j]))
        dict_gantt[title] = temp

    return dict_gantt


def draw_gantt(day): 
    dict_gantt = get_dict(day, onedate=False)

    fig, ax = plt.subplots()
    
    n = len(dict_gantt)
    bar_size = 5

    for i, title in enumerate(dict_gantt):
        ax.broken_barh(dict_gantt[title], (10 * (i + 1), bar_size), color=COLORS[i%7])
        ax.text(dict_gantt[title][0][0], 10 * i + 16, title, ha='left', fontproperties=font,fontsize=6)

    ax.xaxis.set_major_locator(mdates.HourLocator(byhour=range(0, 24, 3)))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax.xaxis.set_minor_locator(mdates.HourLocator(byhour=range(0, 24, 1)))

    plt.grid(b=True, which='minor', linestyle='dotted')

    # doesn't display y axis as default 
    ax.set_yticks([])
    # ax.set_yticks([5 + 10 * n for n in range(1, n + 1)])
    # ax.set_ylim(5, 5 + 10 * (n + 1))
    # ax.set_yticklabels(dict_gantt)

    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    # plt.tight_layout()

    plt.show()


def draw_dailybar(range_days):
    days = range_days.split('-')
    days = [i.strip() for i in days]
    start_date = datetime.strptime(days[0], '%Y.%m.%d')
    end_date = datetime.strptime(days[1], '%Y.%m.%d')
    
    d = start_date
    fig, ax = plt.subplots()
    k = 0
    ticks = {}
    while (d>=end_date):
        if d.day == 1:
            ticks[k] = MONTHS[d.month-1]
        dict_gantt = get_dict(d, onedate=True)
        for i, title in enumerate(dict_gantt):
            ax.broken_barh(dict_gantt[title], (k, 1), color=COLORS[i%7])
        k += 1
        d -= timedelta(days=1)

    ax.xaxis.set_major_locator(mdates.HourLocator(byhour=range(0, 24, 3)))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax.xaxis.set_minor_locator(mdates.HourLocator(byhour=range(0, 24, 1)))

    ax.set_xlim(mdates.date2num(datetime(2018,1,1,6,0)) , mdates.date2num(datetime(2018,1,2,2,0)))

    plt.grid(b=True, which='minor', linestyle='dotted')

    ax.set_yticks(list(ticks.keys()))
    ax.set_yticklabels(list(ticks.values()))

    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.show()

if __name__ == '__main__':
    draw_gantt('2018.9.21')
    # draw_dailybar('2018.9.21 - 2018.6.1')