from classes import reddit
from random import randint
from praw import models
import db

bot = None
subreddit_pool = ['dankmemes', 'PewdiepieSubmissions']

def main():
    global bot

    bot = reddit()

def get_post(limit=5):
    posts = bot.get_hot(subreddit_pool[randint(0, len(subreddit_pool)-1)], limit)
    post:models.reddit.submission.Submission = None
    for _post in posts:
        if db.get_post_by_reddit_id(_post.id) == None:
            post = _post
            break
    if post == None:
        get_post(limit+5)
    return post

    

# if __name__ == "reddit":
#     main()

# if __name__ == "__main__":
#     main()