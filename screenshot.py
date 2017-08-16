"""Take screenshots of a URL"""

import os
import boto
from boto.s3.key import Key
from io import BytesIO
from PIL import Image
from selenium import webdriver

driver = webdriver.PhantomJS()
s3 = boto.connect_s3()
BUCKET_NAME = os.environ['BUCKET_NAME']
bucket = s3.get_bucket(BUCKET_NAME)
k = Key(bucket)

def take_screenshot(user, tweet_id):
    url = "https://mobile.twitter.com/{}/status/{}".format(user, tweet_id)
    driver.get(url)
    image_data = driver.get_screenshot_as_png()
    image = Image.open(BytesIO(image_data))
    cover = image.crop((0, 0, 400, 800))
    filename = "screenshots/{}.png".format(tweet_id)
    cover.save(filename)
    k.key = filename
    k.set_contents_from_filename(filename)
    os.remove(filename)
    return "{}.png".format(tweet_id)
