"""A Python Script hosted on Heroku for running the Twitter Bot @sosvovtot.
   Posts news-tweets from @svtnyheter, translated into Rövarspråket.

   Written by Viktor Stubbfält, 2022-07-05"""

import os     # To handle environment variables
import tweepy # To handle Twitter actions

### Init keys being stored as config vars on Heroku:
API_KEY =             os.getenv("API_KEY")
API_KEY_SECRET =      os.getenv("API_KEY_SECRET")
ACCESS_TOKEN =        os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
BEARER_TOKEN =        os.getenv("BEARER_TOKEN")

### Authenticate our client:
client = tweepy.Client(consumer_key = API_KEY,
                       consumer_secret = API_KEY_SECRET,
                       access_token = ACCESS_TOKEN,
                       access_token_secret = ACCESS_TOKEN_SECRET,
                       bearer_token = BEARER_TOKEN)

### Get the 20 most recent Tweets from both SVT account and Bot account:
ID_BOT = 1543388377571106816
tweets_bot = client.get_users_tweets(id = ID_BOT, max_results = 20).data

ID_SVT = 372142346
tweets_svt = client.get_users_tweets(id = ID_SVT,
                                     max_results = 20,
                                     exclude = ["retweets", "replies"]).data

def encode(string):
    """Encodes a string into Rövarspråket."""
    consonants_lowercase = "bcdfghjklmnpqrstvwxz"
    consonants_uppercase = "BCDFGHJKLMNPQRSTVWXZ"
    for char in consonants_lowercase:
        string = string.replace(char, char + "o" + char)
    for char in consonants_uppercase: # Gets a bit ugly here because of how Capitals (X -> Xox)
        char_lowercase = consonants_lowercase[consonants_uppercase.index(char)]
        string = string.replace(char, char + "o" + char_lowercase)
    return string

### Encode and then store the recent SVT article-tweets as strings in a list:
new_tweets = []
for tweet in tweets_svt:
    split = tweet.text.split("https") # All of their Tweets end with a URL to their website.
    new_tweet = encode(split[0]) + "https" + split[1] # Don't encode the URL.
    new_tweet = new_tweet.replace('\n', '') # Remove newlines, Twitter doesn't even display those...
    if len(new_tweet) <= 280: # Check Twitter character limit
        new_tweets.append(new_tweet)

### From that list, remove all tweets that have already been posted from the bot (i.e. duplicates):
for old_tweet in tweets_bot:
    for new_tweet in new_tweets.copy(): # Avoid modifying a list that is being iterated through.

        # Don't compare the URLs, Twitter seems to shorten them differently every tweet.
        if old_tweet.text.split("https")[0] == new_tweet.split("https")[0]:
            new_tweets.remove(new_tweet)

### Finally, tweet the new, and encoded articles that remain, in chronological order:
new_tweets.reverse()
for tweet in new_tweets:
    client.create_tweet(text = tweet)
