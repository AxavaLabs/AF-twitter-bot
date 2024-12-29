from .connect import TwitterBot
from .llm import ChatGPT
from .exchange import CoinGeckoAPI
import ast
from datetime import datetime


LIST_USER_TWITTER = ["elonmusk", "realDonaldTrump"]
LIST_USERNAME = ["Elon Musk", "Donald Trump"]

class Worker:

  idx_twitter_username = 0
  question_confirm = "Check the following tweets to see if they contain any information related to a coin. Return a list where each entry corresponds to the result (True or False) for each tweet (Ex: [True, False]). Only respond in the given format, no additional explanations."
  question_tweet_news = " just had some posts on Twitter that could affect the price of crypto. I’ll list them below in the following format: '{index}> {action}: {content}'. Your task is to analyze how these activities impact the overall crypto market or the price of a specific coin. Based on that, write a tweet offering advice to people, make sure to use emojis, hashtags, and include a fun element, avoid tagging others. Limit 75 words:"
  question_tweet_coin_price = "Based on the hourly changes in Bitcoin prices, write a tweet advising people which coins to buy, sell, and hold. Be sure to use icons for engagement 💡📈📉💰 and include hashtags with the coin symbols, like #BTC, #ETH, etc., for better visibility. Should be written as a long paragraph like expert advice rather than a dry report, remember to add a fun element in this tweet. Limit 75 words: "
  
  def __init__(self, bearer_token, access_token, access_token_secret, api_key, api_secret_key, api_key_chatgpt):
    self.twitter_bot = TwitterBot(bearer_token,api_key, api_secret_key, access_token, access_token_secret)
    self.chatgpt_bot = ChatGPT(api_key_chatgpt)
    self.coingecko_bot = CoinGeckoAPI()
    
  def process(self):

    # # get post
    # username = LIST_USER_TWITTER[self.idx_twitter_username]  
    # tweets = self.twitter_bot.get_tweets(username=username)
    tweets = [{'id': 1873417011294093499, 'text': 'Please post a bit more positive, beautiful or informative content on this platform', 'type': 'original'}, {'id': 1873416748852203631, 'text': '@TheBabylonBee Bitcoin will up', 'type': 'reply'}, {'id': 1873416599153373597, 'text': 'RT @teslaownersSV: "It\'s important that people have enough babies to support civilization. Civilization might die with a bang or with a whi…', 'type': 'retweet'}, {'id': 1873414878712709321, 'text': '@FoxNewsSunday @RoKhanna Ro is sensible', 'type': 'reply'}, {'id': 1873414542019170523, 'text': '@TPointUK Insane', 'type': 'reply'}]
    
    ## checkpost
    question = self.question_confirm
    for i, tweet in enumerate(tweets):
      question += "\n" + str(i) + ". " + tweet['text']
    result = self.chatgpt_bot.question(question)
    result_list = ast.literal_eval(result)

    ## create massage
    question = LIST_USERNAME[self.idx_twitter_username] + self.question_tweet_news
    if True in result_list:
      j = 0
      for i, result in enumerate(result_list):
        if result == True:
          j += 1
          question += "\n" + str(j) + "> " + tweets[i]["type"] + ": " + tweets[i]['text']
      
      content = self.chatgpt_bot.question(question)
    else:

      # get coin price data
      top_coins = CoinGeckoAPI.get_top_volatile_coins(top_n=10)
      data = ""
      for i, coin in enumerate(top_coins, start=1):
          info = f"\n {i}. {coin['name']} ({coin['symbol']}): {coin['price_change_percentage_24h']}%"
          data += info
      question = self.question_tweet_coin_price + data
      content = self.chatgpt_bot.question(question)

    # post
    
    result = self.twitter_bot.post_tweet(content)
    current_time = datetime.now()
    print(f"{current_time} : {result}")
    
    # update index
    self.idx_twitter_username += 1
    self.idx_twitter_username = self.idx_twitter_username%len(LIST_USER_TWITTER)