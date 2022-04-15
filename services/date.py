import time

##################################################
now = time.localtime()
day = str(now[2])

def get_date_time():
    if day[len(day) - 1] == '1':
        return time.strftime("%dst %B %Y. %H:%M:%S", time.localtime())
    elif day[len(day) - 1] == '2':
        return time.strftime("%dnd %B %Y. %H:%M:%S", time.localtime())
    elif day[len(day) - 1] == '3':
        return time.strftime("%drd %B %Y. %H:%M:%S", time.localtime())
    else:
        return time.strftime("%dth %B %Y. %H:%M:%S", time.localtime())