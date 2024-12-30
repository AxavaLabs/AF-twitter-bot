import os
from dotenv import load_dotenv
from src import Worker
import time
import random

load_dotenv()

# Authenticate to Twitter
api_key = os.getenv("API_KEY")
api_secret_key = os.getenv("API_SECRET_KEY")
bearer_token = os.getenv("BEARER_TOKEN")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")


api_post_key = os.getenv("API_POST_KEY")
api_post_secret_key = os.getenv("API_POST_SECRET_KEY")
access_post_token = os.getenv("ACCESS_POST_TOKEN")
access_post_token_secret = os.getenv("ACCESS_POST_TOKEN_SECRET")

api_key_chatgpt = os.getenv("API_KEY_CHATGPT")

if __name__ == "__main__":
                       while True:
                                              print("-------START-------")
                                              worker = Worker(bearer_token, access_token, access_token_secret, api_key, api_secret_key, api_key_chatgpt, api_post_key, api_post_secret_key, access_post_token, access_post_token_secret)
                                              worker.process()
                                              print("-------END-------")
                                              time_wait = random.randint(1, 1000) + 1800
                                              time.sleep(time_wait)                       
                                              
                       
                       
