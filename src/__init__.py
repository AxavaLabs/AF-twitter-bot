from .connect import TwitterBot
from .llm import ChatGPT
from .exchange import CoinGeckoAPI
import ast
from datetime import datetime
import time

LIST_USER_TWITTER = ["elonmusk", "realDonaldTrump", "S4mmyEth",
                    "stevenyuntcap",
                    "aixbt_agent",
                    "0xCygaar",
                    "ahboyash",
                    "owen1v9",
                    "breadnbutter247",
                    "art_xbt",
                    "SMtrades_",
                    "based16z",
                    "DegenerateNews",
                    "Darrenlautf",
                    "l2beat",
                    "smyyguy",
                    "Fapital3",
                    "poopmandefi",
                    "DefiIgnas",
                    "Jaa9_Bravo",
                    "0xkuromi",
                    "CryptoLimbo_",
                    "cryptomocho",
                    "CryptosArnault",
                    "nobrainflip",
                    "AltCryptoGems",
                    "0xFinish",
                    "0xUnihax0r",
                    "CryptopepperP",
                    "J777Crypto",
                    "PyroNFT",
                    "RomeoTrades",
                    "tehMoonwalkeR",
                    "offshoda",
                    "RaAr3",
                    "ThorTrades8",
                    "crypto_leszcz",
                    "brommmyy",
                    "DeFi_Paanda",
                    "ChristiaanDefi",
                    "tedpillows",
                    "RaAr3s",
                    "andrewtalksdefi",
                    "0xjaypeg",
                    "0xAlan_"]
LIST_USERNAME = ["Elon Musk", "Donald Trump", "S4mmyEth",
                "stevenyuntcap",
                "aixbt_agent",
                "0xCygaar",
                "ahboyash",
                "owen1v9",
                "breadnbutter247",
                "art_xbt",
                "SMtrades_",
                "based16z",
                "DegenerateNews",
                "Darrenlautf",
                "l2beat",
                "smyyguy",
                "Fapital3",
                "poopmandefi",
                "DefiIgnas",
                "Jaa9_Bravo",
                "0xkuromi",
                "CryptoLimbo_",
                "cryptomocho",
                "CryptosArnault",
                "nobrainflip",
                "AltCryptoGems",
                "0xFinish",
                "0xUnihax0r",
                "CryptopepperP",
                "J777Crypto",
                "PyroNFT",
                "RomeoTrades",
                "tehMoonwalkeR",
                "offshoda",
                "RaAr3",
                "ThorTrades8",
                "crypto_leszcz",
                "brommmyy",
                "DeFi_Paanda",
                "ChristiaanDefi",
                "tedpillows",
                "RaAr3s",
                "andrewtalksdefi",
                "0xjaypeg",
                "0xAlan_"]

class Worker:

  idx_twitter_username = 0
  question_confirm = "Check the following tweets to see if they contain any information related to a coin. Return a list where each entry corresponds to the result (True or False) for each tweet (Ex: [True, False]). Only respond in the given format, no additional explanations."
  question_tweet_news = " just had some posts on Twitter that could affect the price of crypto. I’ll list them below in the following format: '{index}> {action}: {content}'. Your task is to analyze how these activities impact the overall crypto market or the price of a specific coin. Based on that, write a tweet offering advice to people, hashtags, and include a fun element, avoid tagging others. Tweet is short and limit only 25 words:"
  question_tweet_coin_price = "Based on the hourly changes in Bitcoin prices, write a tweet advising people which coins to buy, sell, and hold. Be sure to use hashtags with the coin symbols, like #BTC, #ETH, etc., for better visibility. Should be written as a long paragraph like expert advice rather than a dry report, remember to add a fun element in this tweet. Tweet is short and limit only 25 words: "
  
  def __init__(self, bearer_token, access_token, access_token_secret, api_key, api_secret_key, api_key_chatgpt, api_post_key, api_post_secret_key, access_post_token, access_post_token_secret):
    self.twitter_bot = TwitterBot(bearer_token, api_post_key, api_post_secret_key, access_post_token, access_post_token_secret)
    self.chatgpt_bot = ChatGPT(api_key_chatgpt)
    self.coingecko_bot = CoinGeckoAPI()
    
  def process(self):

    # get post
    username = LIST_USER_TWITTER[self.idx_twitter_username]  
    tweets = self.twitter_bot.get_tweets(username=username)
    print(f"tweets: {tweets}" )
    # tweets = [{'id': 1873417011294093499, 'text': 'Please post a bit more positive, beautiful or informative content on this platform', 'type': 'original'}, {'id': 1873416748852203631, 'text': '@TheBabylonBee hahaha', 'type': 'reply'}, {'id': 1873416599153373597, 'text': 'RT @teslaownersSV: "It\'s important that people have enough babies to support civilization. Civilization might die with a bang or with a whi…', 'type': 'retweet'}, {'id': 1873414878712709321, 'text': '@FoxNewsSunday @RoKhanna Ro is sensible', 'type': 'reply'}, {'id': 1873414542019170523, 'text': '@TPointUK Insane', 'type': 'reply'}]
    
    ## checkpost
    result_list = []
    if len(tweets) > 0:
      question = self.question_confirm
      for i, tweet in enumerate(tweets):
        question += "\n" + str(i) + ". " + tweet['text']
      result = self.chatgpt_bot.question(question)
      try:
        result_list = ast.literal_eval(result)
      except (SyntaxError, ValueError) as e:
        print(f"Error parsing result: {e}")

    ## create massage
    
    if True in result_list:
      j = 0
      question = LIST_USERNAME[self.idx_twitter_username] + self.question_tweet_news
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
    if True in result_list or self.idx_twitter_username == 0:
      content = content.replace("\"", "")
      result = self.twitter_bot.post_tweet(content)
      current_time = datetime.now()
      print(f"{current_time} : {result}")
    
    # update index
    self.idx_twitter_username += 1
    self.idx_twitter_username = self.idx_twitter_username%len(LIST_USER_TWITTER)