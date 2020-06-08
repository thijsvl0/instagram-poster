from instagram import bot as instagram_bot
import instagram
from reddit import reddit_video
from dependencies import ROOT_DIR
import os

if __name__ == '__main__':
    # post = reddit_video()
    # post.post_proccessing(os.path.join(ROOT_DIR, 'images', 'gygkwb.gif'), 'gif')
    instagram.post_cycle()
