import csv
import re
from datetime import datetime, timedelta

class Task:

    def __init__(self, row):
        self.title = row[2]
        self.proj = row[4]
        self.context = row[5]
        self.duration = row[9]
        self.date = datetime.strptime(row[8][:10], '%Y-%m-%d').date()
        self.time = self._list_time(row) # a list of timestamps, or breakpoints of a task

    def __str__(self):
        return self.title
    
    def __repr__(self):
        return self.title

    def _list_time(self, row):
        res = []
        try:
            s = datetime.strptime(row[6][11:16], '%H:%M').time()
            if (s.hour+8>24):
                s = s.replace(hour=s.hour-16) # deal with the situation that the time exceeds 24 
            else:
                s = s.replace(hour=s.hour+8)
            res.append(s)
        except:
            if not self.duration:
                return []        
        if row[11]:
            middle = re.findall('[0-9]{1,2}\:[0-9]{2}', row[11])
            middle = [datetime.strptime(i, '%H:%M').time() for i in middle]
            res += middle
        
        e = datetime.strptime(row[8][11:16], '%H:%M').time()
        try:
            e = e.replace(hour=e.hour+8) # deal with the situation that the time exceeds 24 
        except:
            e = e.replace(hour=e.hour-16)
            self.date = self.date.replace(day=self.date.day+1)
        res.append(e)
        
        if len(res) > 2 and res[-1] == res[-2]: # deal with the duplicate end time
            res.pop()
        if len(res) > 1 and res[0] == res[1]:
            res.pop(0)

        if len(res) == 1 and self.duration != '':
            d = int(self.duration[:-1])
            d = timedelta(minutes=d)
            res[0] = datetime.combine(self.date, res[0])
            res = [res[0] - d] + res
        try:
            res = [datetime.combine(self.date, i) for i in res] # combine date and time
        except:
            pass # incase that it has been datetime object
        return res

tasks = []

with open('Omnifocus.csv') as f:
    content = csv.reader(f)
    next(content)
    for row in content:
        if len(row) > 8:
            tasks.append(Task(row))