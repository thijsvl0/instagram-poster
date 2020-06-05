import requests
import instabot
import reddit
import db
import os
from PIL import Image
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
    reddit_post = reddit.get_post()
    print(reddit_post)
    image = get_image(reddit_post)
    insta_id = post_image(image, reddit_post)
    post_comment(insta_id)

def post_image(img, reddit_post):
    img = process_image(img)
    insta_post = bot.upload_photo(img, reddit_post.title)
    insta_id = insta_post['pk']
    db.add_post(reddit_post.title, img, reddit_post.id, insta_id)
    os.rename(img+'.REMOVE_ME', img)
    return insta_id

def post_comment(insta_id):
    bot.comment(insta_id, choice(hashtag_pool))

def get_image(post):
    extension = post.url.split('.')[-1]

    r = requests.get(post.url, stream=True)
    if r.status_code == 200:
        r.raw.decode_content = True
        if not os.path.exists('./images'):
            os.makedirs('./images')
        path = os.path.join('./images', post.id+'.'+extension)
        with open(path, 'wb') as f:
            f.write(r.content)
        
        return path
    else:
        get_image(post)

def process_image(path):
    im = Image.open(path)
    if '.png' in path or '.jpeg' in path:
        os.remove(path)
        path = path.replace('.png', '.jpg')
        path = path.replace('.jpeg', '.jpg')
        
    im_new = expand2square(im, (255,255,255))
    rgb_im = im_new.convert('RGB')
    rgb_im.save(path, quality=95)
    return path

def expand2square(pil_img, background_color):
    width, height = pil_img.size
    if width == height:
        return pil_img
    elif width > height:
        result = Image.new(pil_img.mode, (width, width), background_color)
        result.paste(pil_img, (0, (width - height) // 2))
        return result
    else:
        result = Image.new(pil_img.mode, (height, height), background_color)
        result.paste(pil_img, ((height - width) // 2, 0))
        return result
    

    


# if __name__ == "instagram":
#     main()

# if __name__ == "__main__":
#     main()