from random import choice, sample
import praw
from dependencies import ROOT_DIR
import os
from db import db
import io  
import requests
from PIL import Image, ImageSequence
from moviepy import editor

bot = None

def main():
    global bot
    bot = reddit()

class reddit:
    def __init__(self):
        client_id = os.getenv("CLIENT_ID")
        client_secret = os.getenv("CLIENT_SECRET")
        user_agent = os.getenv("USER_AGENT")
        self.bot = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)
        self.subreddit_pool = self.get_subreddit_pool()
    
    def get_hot(self, subreddit, limit=None):
        return self.bot.subreddit(subreddit).hot(limit=limit)

    def get_subreddit_pool(self):
        return ['dankmemes', 'PewdiepieSubmissions']

    def get_post(self, limit=5):
        posts = list(self.get_hot(choice(self.subreddit_pool), limit))
        for _post in sample(posts, len(posts)):
            if db.get_post_by_reddit_id(_post.id) == None:
                if _post.is_self == False:
                    extension = _post.url.split('.')[-1]
                    if extension in ['jpg', 'png', 'jpeg']:
                    # if extension in ['gif']:
                        return reddit_post(_post)
        print("No Hits")
        return self.get_post(limit+5)

class reddit_post:
    def __init__(self, reddit_post:praw.models.Submission):
        self.post = reddit_post
        self.id = reddit_post.id
        self.url = reddit_post.url
        self.title = reddit_post.title

        self.extension = self.get_extension()
        self.type: reddit_image | reddit_video = self.get_type()

        self.name = '{}.{}'.format(self.id, self.extension)
        self.path = None
    
    def get_extension(self):
        extension = self.url.split('.')[-1]
        return extension

    def get_type(self):
        if self.extension in ['jpg', 'png', 'jpeg']:
            return reddit_image()
        elif self.extension in ['gif', 'mp4']:
            return reddit_video()
    def post_process(self):
        self.path = self.type.post_proccessing(self.path, self.extension)

    def dl_content(self):
        r = requests.get(self.url)
        if r.status_code == 200:
            r.raw.decode_content = True
            if not os.path.exists(os.path.join(ROOT_DIR, 'images')):
                os.makedirs(os.path.join(ROOT_DIR, 'images'))
            self.path = os.path.join(ROOT_DIR,'images',self.name)
            with open(self.path, 'wb') as f:
                f.write(r.content)

    

class reddit_image:
    def __init__(self):
        self.path = None
        self.content = None
        self.extension = None

    def post_proccessing(self, path, extension):
        self.path = path
        self.content = Image.open(self.path)
        self.extension = extension
        self.convert()
        self.content = self.make_square((255,255,255))
        self.content = self.content.convert('RGB')
        self.content = self.content.save(self.path, quality=95)
        return self.path

    def convert(self):
        if self.extension == 'png' or self.extension == 'jpeg':
            os.remove(self.path)
            self.path = self.path.replace('png', 'jpg').replace('jpeg', 'jpg')

    def make_square(self, background_color):
        width, height = self.content.size
        if width == height:
            return self.content
        elif width > height:
            result = Image.new(self.content.mode, (width, width), background_color)
            result.paste(self.content, (0, (width - height) // 2))
            return result
        else:
            result = Image.new(self.content.mode, (height, height), background_color)
            result.paste(self.content, ((height - width) // 2, 0))
            return result

class reddit_video:
    def __init__(self):
        self.path = None
        self.content = None

    def post_proccessing(self, path, extension):
        self.path = path
        self.content = Image.open(self.path)
        self.content = self.make_square((255,255,255))
        self.content[0].save(self.path, save_all=True, append_images=self.content[1:], quality=95, loop=0)
        self.make_video()
        return self.path
    
    def make_video(self):
        clip = editor.VideoFileClip(self.path)
        self.path = self.path.replace('.gif', '.mp4')
        clip.write_videofile(self.path)

    def make_square(self, background_color):
        frames = []
        for frame in ImageSequence.Iterator(self.content):

            width, height = frame.size
            result = None
            if width == height:
                pass
            elif width > height:
                result = Image.new('RGBA', (width, width), background_color)
                result.paste(frame, (0, (width - height) // 2))
            else:
                result = Image.new('RGBA', (height, height), background_color)
                result.paste(frame, ((height - width) // 2, 0))
            b = io.BytesIO()
            result.save(b, format="GIF")
            result = Image.open(b)
            frames.append(result)
            
        return frames



if __name__ == "reddit":
    main()

# if __name__ == "__main__":
#     main()