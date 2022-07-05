"""Twitter bot that posts news-tweets from SVT Nyheter, translated into Rövarspråket."""

import tweepy

### Authentication:
API_KEY = "key"
API_KEY_SECRET = "key"
CLIENT_ID = "key"
CLIENT_ID_SECRET = "key"
ACCESS_TOKEN = "key"
ACCESS_TOKEN_SECRET = "key"
BEARER_TOKEN = "key"

client = tweepy.Client(consumer_key = API_KEY,
                       consumer_secret = API_KEY_SECRET,
                       access_token = ACCESS_TOKEN,
                       access_token_secret = ACCESS_TOKEN_SECRET,
                       bearer_token = BEARER_TOKEN)

### Get Tweets:
ID_SVT = 372142346
ID_SOSVOVTOT = 1543388377571106816
tweets_svt = client.get_users_tweets(id = ID_SVT,
                                     exclude=["retweets", "replies"],
                                     max_results = 40).data
tweets_sosvovtot = client.get_users_tweets(id = ID_SOSVOVTOT, max_results = 40).data

def encode(string):
    """Encodes a string into Rövarspråket."""
    consonants_lowercase = "bcdfghjklmnpqrstvwxz"
    consonants_uppercase = "BCDFGHJKLMNPQRSTVWXZ"
    for char in consonants_lowercase:
        string = string.replace(char, char + "o" + char)
    for char in consonants_uppercase:
        char_lowercase = consonants_lowercase[consonants_uppercase.index(char)]
        string = string.replace(char, char + "o" + char_lowercase)
    return string

### Encode and store new SVT Nyheter article-tweets (just the text) as strings in a list:
new_tweets = []
for tweet in tweets_svt:
    split = tweet.text.split("https")
    new_tweet = encode(split[0]) + "https" + split[1]
    new_tweet = new_tweet.replace('\n', '')
    if len(new_tweet) <= 280:
        new_tweets.append(new_tweet)

### Remove already posted article-tweets from SosVovTot (duplicates):
old_tweets = []
for old_tweet in tweets_sosvovtot:
    for new_tweet in new_tweets:
        if old_tweet.text.split("https")[0] == new_tweet.split("https")[0]:
            new_tweets.remove(new_tweet)

### Tweet the new, original and encoded articles:
new_tweets.reverse()
for tweet in new_tweets:
    client.create_tweet(text=tweet)
