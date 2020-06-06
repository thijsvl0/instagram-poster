import sqlite3
from sqlite3 import Error
import os
import praw
import instabot
import requests
from PIL import Image


class database:
    def __init__(self, db_file):
        self.conn = self.create_connection(db_file)
        self.cursor = self.conn.cursor()

    def create_connection(self, db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file, check_same_thread=False)
        except Error as e:
            print(e)
        finally:
            return conn

    def execute(self, query, placeholder = ""):
        try:
            self.cursor.execute(query, placeholder)
        except Error as e:
            print(e)

class reddit:
    def __init__(self):
        client_id = os.getenv("CLIENT_ID")
        client_secret = os.getenv("CLIENT_SECRET")
        user_agent = os.getenv("USER_AGENT")
        self.bot = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)
    
    def get_hot(self, subreddit, limit=None):
        return self.bot.subreddit(subreddit).hot(limit=limit)

class reddit_post:
    def __init__(self, reddit_post:praw.models.Submission):
        self.post = reddit_post
        self.id = reddit_post.id
        self.url = reddit_post.url

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
            if not os.path.exists(os.path.abspath('images')):
                os.makedirs(os.path.abspath('images'))
            self.path = os.path.abspath('images/{}'.format(self.name))
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
        return

    def post_proccessing(self, image, extension):
        return
