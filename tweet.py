from datetime import datetime
from dayfinder import get_approximation_day
import sys
import math

test = "test" in sys.argv

if test:
    print("Running in test mode. Tweets will not be sent")
else:
    import twitter

now = datetime.now()

approx_day = get_approximation_day(now.day, now.month)

if approx_day is not None:
    tweet = "Happy " + str(approx_day) + " Approximation Day!"

    tweet2 = str(approx_day) + " = " + str(approx_day.value)
    tweet2 += "\n\n"
    tweet2 += "Today = " + str(now.day) + "/" + str(now.month)
    if now.day % now.month == 0:
        tweet2 += " = " + str(now.day // now.month)
    else:
        tweet2 += " = " + str(now.day / now.month)

    tweet2 += "\n\n"

    error = abs((now.day / now.month) - approx_day.value) / (now.day / now.month)
    tweet2 += "error = "
    tweet2 += str(math.floor(error * 1000000) / 100000) + "%"

    if test:
        print("If not in test mode, I would've tweeted:")
        print("   ", tweet)
        print("   ", "\n    ".join(tweet2.split("\n")))
    else:
        import config as c
        tw = twitter.Twitter(auth=twitter.OAuth(
            c.token, c.secret, c.consumer_key, c.consumer_secret))
        result = tw.statuses.update(status=tweet)
        print("updated status: " + tweet)

        result = tw.statuses.update(
            status="@" + c.username + " " + tweet2,
            in_reply_to_status_id=result["id"])
        print("updated status: " + tweet2)
