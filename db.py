from datetime import datetime
from classes import database

db = None

def main():
    global db
    db = database('main.db')
    make_posts_table()

def make_posts_table():
    db.execute('CREATE TABLE IF NOT EXISTS posts (id integer PRIMARY KEY, title text, img text, reddit_id string, date date)')

def add_post(title, img, reddit_id):
    db.execute('INSERT INTO posts(title, img, reddit_id, date) values(?,?,?)', (title, img, reddit_id, datetime.now().strftime("%d/%m/%Y %H:%M:%S"), ) )

def get_post_by_id(post_id):
    db.execute('SELECT * FROM posts WHERE id = ?', (post_id, ))
    return db.cursor.fetchone()

def get_post_by_reddit_id(reddit_id):
    db.execute('SELECT * FROM posts WHERE reddit_id = ?', (reddit_id, ))
    return db.cursor.fetchone()

def get_posts():
    db.execute('SELECT * FROM posts')
    return db.cursor.fetchall()

def del_post(post_id):
    db.execute('DELETE FROM posts WHERE id = ?', (post_id, ))
    db.conn.commit()

if __name__ == 'db':
    main()

if __name__ == '__main__':
    main()