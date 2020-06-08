import requests
import instabot
from reddit import bot as reddit_bot
from db import db
import os
from random import choice
from time import sleep

bot = None

def main():
    global bot
    bot = instagram(instabot.Bot(comment_delay=0))

def post_cycle():
    reddit_post = reddit_bot.get_post()
    reddit_post.dl_content()
    reddit_post.post_process()
    insta_id = bot.post(reddit_post.path, reddit_post.title)
    db.add_post(reddit_post.title, reddit_post.path, reddit_post.id, insta_id)
    # bot.post_comment(insta_id, bot.get_hashtag_pool())


class instagram:
    def __init__(self, insta_bot):
        self.user = os.getenv("INSTAGRAM_USER")
        self.password = os.getenv("INSTAGRAM_PASSWORD")
        self.bot = insta_bot
        self.login()

    def login(self):
        username = self.user
        password = self.password
        self.bot.login(username=username, password=password)

    def logout(self):
        self.bot.logout()

    def get_hashtag_pool(self):
        return [
                    '#meme #memes #bestmemes #instamemes #funny #funnymemes #dankmemes #offensivememes #edgymemes #spicymemes #nichememes #memepage #funniestmemes #dank #memesdaily #jokes #memesrlife #memestar #memesquad #humor #lmao #igmemes #lol #memeaccount #memer #relatablememes #funnyposts #sillymemes #nichememe #memetime',
                    '#memeimages #newestmemes #todaymemes #recentmemes #decentmemes #memearmy #memedose #memehumor #questionablememes #sickmeme #oldmeme #unusualmeme #memeculture #memehour #bizarrememe #scarymeme #sarcasm #goofymemes #entertaining #ironic #stupidmemes #crazymemes #lightmeme #annoyingthings #memehearted #wtfmeme #dogmemes #catmeme #fortnitememes #clevermemes',
                    '#oddlymemes #dumbmemes #interestingmemes #likablememes #beameme #fulltimememer #cornymeme #surrealmeme #wowmemes #originalmemes #creepymemes #memefarm #mememaker #memebased #meming #memelord #latinmemes #schoolmemes #relevantmeme #bestjokes #memeboss #dadjokes #famousmemes #memeintelligence #memeuniversity #gamingmemes #rapmemes #coldmemes #memeit #prettyfunny'
                ]

    def post(self, file, title):
        extension = file.split('.')[-1]
        if extension == 'jpg':
            return self.post_image(file, title)
        elif extension == 'gif':
            return self.post_video(file, title)


    def post_image(self, image, title):
        insta_post = self.bot.upload_photo(image, title.rstrip()+"\n®\n®\n®\n"+choice(self.get_hashtag_pool()))
        # insta_post = self.bot.upload_photo(image, title+"\n                 \n New Line")
        os.rename(image+'.REMOVE_ME', image)
        return insta_post['pk']
    
    def post_video(self, video, title):
        insta_post = self.bot.upload_video(video, title)
        print(insta_post)
        os.rename(video+'.REMOVE_ME', video)
        return insta_post['pk']

    def post_comment(self, insta_id, comment):
        if isinstance(comment, list):
            self.bot.comment(insta_id,  choice(comment))
        elif isinstance(comment, str):
            self.bot.comment(insta_id, comment)
    

    


if __name__ == "instagram":
    main()

# if __name__ == "__main__":
#     main()