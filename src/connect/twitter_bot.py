import tweepy
from requests_oauthlib import OAuth1
import requests
from datetime import datetime, timedelta, timezone

URL_TWEETS = "https://api.twitter.com/2/tweets"

class TwitterBot:
    def __init__ (self, bearer_token, api_key, api_secret_key, access_token, access_token_secret):
        self.client = tweepy.Client(bearer_token=bearer_token, wait_on_rate_limit=True)
        self.auth = OAuth1(api_key, api_secret_key, access_token, access_token_secret)
        
    def get_tweets(self, username, max_results=10):
        """
        Get tweets from a user using Tweepy with Twitter API v2 and classify tweet types.
    
        Parameters:
        - username (str): The username to fetch tweets for.
        - max_results (int): Maximum number of tweets to fetch (default 10).
    
        Returns:
        - tweets (list): List of classified tweets (dict with id, text, and type).
        """
    
        # Get the user's ID by username
        try:
            user = self.client.get_user(username=username)
            user_id = user.data.id
        except tweepy.TweepyException as e:
            print(f"Error fetching user ID: {e}")
            return []

        # Get the user's tweets
        try:
            response = self.client.get_users_tweets(id=user_id,
                                               max_results=max_results,
                                               tweet_fields=[
                                                   "created_at",
                                                   "referenced_tweets",
                                                   "in_reply_to_user_id"
                                               ])
            tweets = response.data or []  # Handle case where no tweets are returned

            # Filter tweets within the last 15 minutes
            now = datetime.now(timezone.utc)  # Current time in UTC with timezone awareness
            fifteen_minutes_ago = now - timedelta(minutes=15)

            recent_tweets = []
            for tweet in tweets:
                tweet_type = "original"  # Default type

                # Check for referenced_tweets
                if tweet.referenced_tweets:
                    for ref in tweet.referenced_tweets:
                        if ref["type"] == "retweeted":
                            tweet_type = "retweet"
                        elif ref["type"] == "quoted":
                            tweet_type = "quote"
                        elif ref["type"] == "replied_to":
                            tweet_type = "reply"

                # Check for reply (in_reply_to_user_id)
                if tweet.in_reply_to_user_id and tweet_type == "original":
                    tweet_type = "reply"

                # Filter based on creation time
                created_at = tweet.created_at  # This is already a timezone-aware datetime
                if created_at >= fifteen_minutes_ago:
                    recent_tweets.append({
                        "id": tweet.id,
                        "text": tweet.text,
                        "type": tweet_type,
                    })

            return recent_tweets
        except tweepy.TweepyException as e:
            print(f"Error fetching tweets: {e}")
            return []

    def post_tweet(self, content: str):
        """
        Post a tweet using Twitter API v2 with OAuth 1.0a.
    
        Parameters:
        - content (str): The content of the tweet to post.
    
        Returns:
        - response (boolean): Response from the Twitter API.
        """

        # Payload with the tweet content
        payload = {"text": content}
        
        response = requests.post(URL_TWEETS, auth=self.auth, json=payload)
    
        # Check if the request was successful
        if response.status_code == 201:
            return True
        else:
            print(f"Failed to post tweet: \n - status code: {response.status_code} \n - text: {response.text} \n - content: {content}")
            return False


# Example usage
if __name__ == "__main__":
    BEARER_TOKEN = r""
    USERNAME = "elonmusk"  # Replace with the username you want to fetch tweets for

    # Fetch tweets and classify them
    tweets = get_user_tweets_with_types(BEARER_TOKEN, USERNAME, max_results=5)
    print("Classified Tweets:")
    for tweet in tweets:
        print(
            f"- ID: {tweet['id']}, Type: {tweet['type']}, Text: {tweet['text']}"
        )
