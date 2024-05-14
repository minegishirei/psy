import tweepy
import sys

#Twitter Developer Portalから取得したキーを設定
CONSUMER_KEY = 'M8qVyxkSeg8fEfEJb9TjMOGll'
CONSUMER_SECRET = '2qB1l7fs6b837qIetaN9lHSPHI6Awmd3SqWI9NbEyCcMV22OvZ'
ACCESS_TOKEN = '1349555933257469955-2UBWgME3lXUZmw4vmGbWtpcu5UIGXa'
ACCESS_SECRET = 'gSUCGz10sG6U7IRL0PrYSK4DPRhoyXKKWNwypj6iaRea6'

#ツイート内容

CONSUMER_KEY = "YnuweXfQMN1WHpxpYZeFVqDRM"
CONSUMER_SECRET = "IMKJRAueZ28Ghp4epL0TT2f1d753x4GocQssFw9Jw2LHaTgU0M"
ACCESS_TOKEN = "1349555933257469955-Bo7TrvVDVIgHRCWmNLJnYnlxv9dHn6"
ACCESS_SECRET = "Eko1yGXwJi0kDnECKbtxMNpvsoBkuGamULGGivIacpW1r"

#オブジェクト作成
client = tweepy.Client(
	consumer_key = CONSUMER_KEY,
	consumer_secret = CONSUMER_SECRET,
	access_token = ACCESS_TOKEN,
	access_token_secret = ACCESS_SECRET
)

_, arg = sys.argv

if arg.startswith("tw:"):
	text = arg.replace("tw:")
	client.create_tweet(text=text)



