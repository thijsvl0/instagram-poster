from datetime import datetime
from dependencies import ROOT_DIR
import sqlite3
from sqlite3 import Error
import os

db = None

def main():
    global db
    db = database(os.path.join(ROOT_DIR,'main.self'))

class database:
    def __init__(self, db_file):
        self.conn = self.create_connection(db_file)
        self.cursor = self.conn.cursor()
        self.make_posts_table()

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
    
    def make_posts_table(self):
        self.execute('CREATE TABLE IF NOT EXISTS posts (id integer PRIMARY KEY, title text, img text, reddit_id string, insta_id string, date date)')

    def add_post(self, title, img, reddit_id, insta_id):
        self.execute('INSERT INTO posts(title, img, reddit_id, insta_id, date) values(?,?,?,?,?)', (title, img, reddit_id, insta_id, datetime.now().strftime("%d/%m/%Y %H:%M:%S"), ) )
        self.conn.commit()

    def get_post_by_id(self, post_id):
        self.execute('SELECT * FROM posts WHERE id = ?', (post_id, ))
        return self.cursor.fetchone()

    def get_post_by_reddit_id(self, reddit_id):
        self.execute('SELECT * FROM posts WHERE reddit_id = ?', (reddit_id, ))
        return self.cursor.fetchone()

    def get_posts(self):
        self.execute('SELECT * FROM posts')
        return self.cursor.fetchall()

    def del_post(self,post_id):
        self.execute('DELETE FROM posts WHERE id = ?', (post_id, ))
        self.conn.commit()

if __name__ == 'db':
    main()

if __name__ == '__main__':
    main()