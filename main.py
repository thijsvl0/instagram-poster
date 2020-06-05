from dotenv import load_dotenv
import reddit
import instagram
import sched, time


def main():
    schedule = sched.scheduler(time.time, time.sleep)
    instagram.login()
    schedule.enter(1, 1, sched_poster, (schedule,))
    schedule.run()
    
def sched_poster(schedule):
    try:
        instagram.post_cycle()
    except TypeError:
        schedule.enter(300,1, sched_poster, (schedule,))

    schedule.enter(300,1, sched_poster, (schedule,))

# if __name__ == "main":
#     main()

if __name__ == "__main__":
    load_dotenv('./.env')
    reddit.main()
    instagram.main()
    main()
