from datetime import datetime
from dayfinder import get_approximation_day
import sys
import math
from atproto import Client, models

test = "test" in sys.argv

if test:
    print("Running in test mode. Tweets will not be sent")
else:
    import mastodon

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

    error = abs((now.day / now.month) - approx_day.value)
    error /= (now.day / now.month)
    tweet2 += "error = "
    digits = 10 ** 4
    tweet2 += str(math.floor(error * 100 * digits) / digits) + "%"

    if test:
        print("If not in test mode, I would've tweeted:")
        print("   ", tweet)
        print("   ", "\n    ".join(tweet2.split("\n")))
    else:
        import config as c

        # Mastodon
        mdon = mastodon.Mastodon(
            access_token="mdon.secret", api_base_url="https://mathstodon.xyz")

        mresult = mdon.toot(tweet)
        print("updated status: " + tweet)

        mdon.status_post(
            "@" + c.username + " " + tweet2,
            in_reply_to_id=mresult["id"])
        print("updated status: " + tweet2)

        # Bluesky
        client = Client()
        with open("bsky.secret") as f:
            app_password = f.read().strip()
        client.login(c.bky_user, app_password)

        first_post = models.create_strong_ref(client.send_post(tweet))
        client.send_post(text=tweet2, reply_to=models.AppBskyFeedPost.ReplyRef(
            parent=root_post_ref, root=root_post_ref))
