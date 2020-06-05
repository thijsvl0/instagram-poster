import sqlite3
from sqlite3 import Error
import os
import praw
import instabot

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