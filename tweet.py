from twitter import *
from random import choice
from datetime import datetime

print(datetime.now())

import config

twitter = Twitter(
    auth = OAuth(config.token, config.secret, config.consumer_key, config.consumer_secret))

tweet = "Bello world!"

results = twitter.statuses.update(status=tweet)
print(f"updated status: {tweet}")

