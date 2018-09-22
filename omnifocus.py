import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import csv
from datetime import datetime

dates = [] 
counter = [] # the number of tasks completed everyday 
durations = [] # the daily duration of total completed tasks 

with open('Omnifocus.csv') as f:
    content = csv.reader(f)
    next(content)
    for row in content:
        try:
            date = datetime.strptime(row[8][:10], '%Y-%m-%d')
        except:
            continue
        
        if date in dates:
            counter[-1] += 1
            if len(row[9]) > 0:
                durations[-1] += int(row[9][:-1])
        else:
            dates.append(date)
            counter.append(1)
            durations.append(0)
            if len(row[9]) > 0:
                durations[-1] += int(row[9][:-1])

durations = [d/60 for d in durations] # convert minutes to hours 


if __name__ == '__main__':
    months = mdates.MonthLocator()
    monthsFmt = mdates.DateFormatter('%m')
    days = mdates.DayLocator()

    fig, ax = plt.subplots()

    #ax.bar(dates[:100], counter[:100])
    ax.bar(dates[:120], durations[:120]) # depict the data within the last four months as default 

    ax.xaxis.set_major_locator(months)
    ax.xaxis.set_major_formatter(monthsFmt)
    ax.xaxis.set_minor_locator(days)

    ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
    ax.grid(True)

    plt.show()
