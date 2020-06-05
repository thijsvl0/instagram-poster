from classes import reddit
from random import choice, sample
from praw import models
import db

bot = None
subreddit_pool = ['dankmemes', 'PewdiepieSubmissions', 'BlackPeopleTwitter']

def main():
    global bot
    bot = reddit()

def get_post(limit=5)->models.reddit.submission.Submission:
    posts = list(bot.get_hot(choice(subreddit_pool), limit))
    for _post in sample(posts, len(posts)):
        if db.get_post_by_reddit_id(_post.id) == None:
            if _post.is_self == False:
                if any(format in  _post.url for format in ['jpg','png', 'jpeg']):
                    return _post
    print("No Hits")
    return get_post(limit+5)

    

# if __name__ == "reddit":
#     main()

# if __name__ == "__main__":
#     main()