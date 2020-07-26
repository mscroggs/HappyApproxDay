from twitter import *
from datetime import datetime
from dayfinder import get_approximation_day
import sys

test = "test" in sys.argv

if test:
    print("Running in test mode. Tweets will not be sent")

now = datetime.now()

approx_day = get_approximation_day(now.day, now.month)

if approx_day is not None:
    if not test:
        import config

        twitter = Twitter(
            auth = OAuth(config.token, config.secret, config.consumer_key, config.consumer_secret))

        tweet = f"Happy {approx_day.constant()} Approximation Day!"

        results = twitter.statuses.update(status=tweet)
    print(f"updated status: {tweet}")