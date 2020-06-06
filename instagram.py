import requests
import instabot
import reddit
import db
import os
from classes import reddit_post
from random import choice
from time import sleep

bot = None

hashtag_pool = [
    '#meme #memes #bestmemes #instamemes #funny #funnymemes #dankmemes #offensivememes #edgymemes #spicymemes #nichememes #memepage #funniestmemes #dank #memesdaily #jokes #memesrlife #memestar #memesquad #humor #lmao #igmemes #lol #memeaccount #memer #relatablememes #funnyposts #sillymemes #nichememe #memetime',
    '#memeimages #newestmemes #todaymemes #recentmemes #decentmemes #memearmy #memedose #memehumor #questionablememes #sickmeme #oldmeme #unusualmeme #memeculture #memehour #bizarrememe #scarymeme #sarcasm #goofymemes #entertaining #ironic #stupidmemes #crazymemes #lightmeme #annoyingthings #memehearted #wtfmeme #dogmemes #catmeme #fortnitememes #clevermemes',
    '#oddlymemes #dumbmemes #interestingmemes #likablememes #beameme #fulltimememer #cornymeme #surrealmeme #wowmemes #originalmemes #creepymemes #memefarm #mememaker #memebased #meming #memelord #latinmemes #schoolmemes #relevantmeme #bestjokes #memeboss #dadjokes #famousmemes #memeintelligence #memeuniversity #gamingmemes #rapmemes #coldmemes #memeit #prettyfunny'
]
def main():
    global bot
    bot = instabot.Bot(comment_delay=0)

def login():
    username = os.getenv("INSTAGRAM_USER")
    password = os.getenv("INSTAGRAM_PASSWORD")
    bot.login(username=username, password=password)

def logout():
    bot.logout()

def post_cycle():
    _reddit_post = reddit.get_post()
    print(_reddit_post.id)
    post = reddit_post(_reddit_post)
    post.dl_content()
    post.post_process()
    insta_id = post_image(post)
    post_comment(insta_id)

def post_image(post:reddit_post):
    insta_post = bot.upload_photo(post.path, post.post.title)
    insta_id = insta_post['pk']
    db.add_post(post.post.title, post.path, post.id, insta_id)
    os.rename(post.path+'.REMOVE_ME', post.path)
    return insta_id

def post_comment(insta_id):
    bot.comment(insta_id, choice(hashtag_pool))
    

    


# if __name__ == "instagram":
#     main()

# if __name__ == "__main__":
#     main()