from datetime import datetime
from dayfinder import get_approximation_day
import sys
import twitter

test = "test" in sys.argv

if test:
    print("Running in test mode. Tweets will not be sent")

now = datetime.now()

approx_day = get_approximation_day(now.day, now.month)

if approx_day is not None:
    tweet = f"Happy {approx_day} Approximation Day!"

    if not test:
        import config as c
        tw = twitter.Twitter(auth=twitter.OAuth(
            c.token, c.secret, c.consumer_key, c.consumer_secret))
        results = tw.statuses.update(status=tweet)
    print(f"updated status: {tweet}")
