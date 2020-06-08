import reddit
import instagram
from db import db
from random import randint
import sched, time
from dependencies import ROOT_DIR

def main():
    schedule = sched.scheduler(time.time, time.sleep)
    schedule.enter(1, 1, sched_poster, (schedule,))
    schedule.run()

def sched_poster(schedule):
    freq = (10800+((120*randint(0, 50))/2)/2)
    try:
        instagram.post_cycle()
        print('{} Sec till next post'.format(freq))
    except TypeError:
        schedule.enter(freq,1, sched_poster, (schedule,))

    schedule.enter(freq,1, sched_poster, (schedule,))

# if __name__ == "main":
#     main()

if __name__ == "__main__":
    main()
