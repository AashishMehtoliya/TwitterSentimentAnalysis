from tweepy.streaming import StreamListener
from tweepy import Stream
from tweepy import API
from tweepy import Cursor
import json
from tweepy import OAuthHandler
import numpy as np
import pandas as pd
import Twitter_SA

pd.set_option('display.max_columns', None)


# # # Twitter Client # # #
class TwitterClient():

        def __init__(self , twitter_user = None):
            self.auth = TwitterAuthentication().authenticate_app()
            self.twitter_client = API(self.auth)
            self.twitter_user = twitter_user

        def get_twitter_client(self):
            return self.twitter_client

        def get_user_timeline_tweets(self , num_tweets):

            tweets = []
            for tweet in Cursor(self.twitter_client.user_timeline , id = self.twitter_user).items(num_tweets):
                # tweet = tweet.encode('utf-8')
                tweets.append(tweet)
            return tweets

        def get_friend_list(self , no_of_friend):
            friend_list = []
            for friend in Cursor(self.twitter_client.friends , id = self.twitter_user).item(no_of_friend):
                friend_list.append(friend)

            return friend_list

        def get_home_timeline_tweets(self , no_of_tweets):
            timeline_tweets = []
            for tweet in Cursor(self.twitter_client.home_timeline , id = self.twitter_user).itmes(no_of_tweets):
                timeline_tweets.append(tweet)
            return timeline_tweets




# # # Twiiter Authenticater # # #
class TwitterAuthentication():

    def authenticate_app(self):
        auth = OAuthHandler(Twitter_SA.CONSUMER_KEY , Twitter_SA.CONSUMER_SECRET)
        auth.set_access_token(Twitter_SA.ACCESS_TOKEN , Twitter_SA.ACCESS_TOKEN_SECRET )
        return auth


class TwitterStreamer():
    """
    class for streaming and processing live tweets
    """
    def __init__(self):
        self.twitter_authenticator = TwitterAuthentication()

    def stream_tweets(self , fetched_tweets_file , hash_tags):
        Listener = TwitterListener(fetched_tweets_file)
        auth = self.twitter_authenticator.authenticate_app()

        stream = Stream(auth , Listener)

        stream.filter(track = hash_tags)


class TweeetAnalyzer():

    def tweet_to_dataframe(self , tweets):

        df = pd.DataFrame(data = [tweet.text for tweet in tweets]   , columns = ['Tweets'])

        df['id'] = np.array([tweet.id for tweet in tweets])
        df['len'] = np.array([len(tweet.text) for tweet in tweets])
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])
        df['source'] = np.array([tweet.source for tweet in tweets])
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        df['favorite'] = np.array([tweet.favorite for tweet in tweets])

        return df





class TwitterListener(StreamListener):
    """
    this is a basic listener that just print and received tweets to stdout
    """

    def __init__(self , fetched_tweets_file):
        self.fetched_tweets_file = fetched_tweets_file

    def on_data(self , data):
        try:
            print(data)
            with open(fetched_tweets_file , 'a' , encoding = 'utf-8') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("The error on data : %s" %str(e))

        return True

    def on_error(self , status):
        if status == 420:
            #returning false on_data method in case rate limit occurs
            return False
        print(status)

if __name__ == "__main__":

  twitter_client = TwitterClient()
  tweet_analyzer = TweeetAnalyzer()
  api = twitter_client.get_twitter_client()

  user_tweets = api.user_timeline(screen_name = 'TheTweetOfGod' , count = 20)

  df = tweet_analyzer.tweet_to_dataframe(user_tweets)
  print(df)


  for tweet in user_tweets:
    print(tweet.text)

  print(dir(user_tweets[0]))



