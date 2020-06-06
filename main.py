from dotenv import load_dotenv
import reddit
import instagram
from random import randint
import sched, time

freq = 10800
def main():
    schedule = sched.scheduler(time.time, time.sleep)
    instagram.login()
    schedule.enter(1, 1, sched_poster, (schedule,))
    schedule.run()
    
def sched_poster(schedule):
    freq = (10800+((120*randint(0, 50))/2)/2)
    print('{} Sec till next post'.format(freq))

    try:
        instagram.post_cycle()
    except TypeError:
        schedule.enter(freq,1, sched_poster, (schedule,))

    schedule.enter(freq,1, sched_poster, (schedule,))

# if __name__ == "main":
#     main()

if __name__ == "__main__":
    load_dotenv('./.env')
    reddit.main()
    instagram.main()
    main()
