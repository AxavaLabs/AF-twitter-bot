import tweepy
import os
from dotenv import load_dotenv

load_dotenv()

# Authenticate to Twitter
api_key = os.getenv("API_KEY")
api_secret_key = os.getenv("API_SECRET_KEY")
bearer_token = os.getenv("BEARER_TOKEN")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

client = tweepy.Client(bearer_token, access_token, access_token_secret, api_key, api_secret_key)

if __name__ == "__main__":
    # Create a tweet
    timeline = client.create_tweet(text = "Hello, world!")
