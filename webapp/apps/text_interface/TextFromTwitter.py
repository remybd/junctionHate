import tweepy
import numpy as np
import scipy.stats

from apps.classifiers import NltkClassifier


class TextFromTwitter():
    def __init__(self):
        consumer_key = 'VqLtcUiHKrWy8YXfgWODFyFoe'
        consumer_secret = '7YNxcOhtHRjpq1ybx6RRE28WId2028z6S2y69L3bN6rmJJggx1'
        access_token = '140961368-NSM1xsEFmgIcJre5doFnV50JtAc2JjBdI46GB0nf'
        access_token_secret = 'fykaXl80SYQrG3TbePVZAGmuT6zyrd8fQl0f3BLtwz2S2'

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

        auth.set_access_token(access_token, access_token_secret)

        self.api = tweepy.API(auth)

    def get_status_from_user_from_tweet_id(self, user, tweet_number=1, tweet_id=""):
        if tweet_id == "":
            status = self.api.user_timeline(screen_name=user, count=tweet_number)
        else:
            status = self.api.user_timeline(screen_name=user, count=tweet_number, max_id=tweet_id)

        tweet_list = []

        for s in status:
            tweet = {"id": s.id, "message": s.text}
            tweet_list.append(tweet)
        return tweet_list

    def get_status_from_user(self, user, tweet_number=1):
        return self.get_status_from_user_from_tweet_id(user=user, tweet_number=tweet_number)

    def get_nltk_statistic(self, user, tweet_number=10):
        classifier = NltkClassifier.NltkClassifier()
        tweets = self.get_status_from_user(user, tweet_number=tweet_number)
        compound_scores = []
        for tweet in tweets:
            scores = classifier.analyse_text(tweet['message'])
            compound_scores.append(scores['compound'])
        return scipy.stats.describe(compound_scores)


if __name__ == '__main__':
    twitter = TextFromTwitter()
    print(twitter.get_nltk_statistic("potus", 200))
    print(twitter.get_nltk_statistic("realdonaldtrump", 200))
    print(twitter.get_nltk_statistic("matthewheimbach", 200))
