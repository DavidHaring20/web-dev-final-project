import time

##################################################
now = time.localtime()
day = str(now[2])

def get_date_time():
    if day[len(day) - 1] == '1':
        return time.strftime("%d.%m.%Y. %H:%M", time.localtime())