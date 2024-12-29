import requests
import pandas as pd
import time


class CoinGeckoAPI:
    BASE_URL = "https://api.coingecko.com/api/v3"

    @staticmethod
    def get_top_volatile_coins(currency="usd", top_n=10):
        """
        Fetch the top volatile coins based on 24-hour price change percentage.

        :param currency: Market currency (e.g., 'usd').
        :param top_n: Number of coins to fetch.
        :return: List of top volatile coins.
        """
        url = f"{CoinGeckoAPI.BASE_URL}/coins/markets"
        params = {
            "vs_currency": currency,
            "order": "percent_change_1h_desc",
            "per_page": top_n,
            "page": 1,
            "sparkline": False
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def get_historical_data(coin_id, currency="usd", days="1", interval="5m", retries=3):
        """
        Fetch historical market data for a given coin.

        :param coin_id: The unique ID of the coin (e.g., 'bitcoin').
        :param currency: Market currency (e.g., 'usd').
        :param days: Time period for historical data (e.g., '1' for 1 day).
        :param interval: Data interval (e.g., '5m' for 5 minutes).
        :param retries: Number of retries for failed requests.
        :return: Pandas DataFrame of historical data.
        """
        url = f"{CoinGeckoAPI.BASE_URL}/coins/{coin_id}/market_chart"
        params = {
            "vs_currency": currency,
            "days": days,
            "interval": interval
        }
        for attempt in range(retries):
            try:
                response = requests.get(url, params=params)
                response.raise_for_status()
                data = response.json()["prices"]
                df = pd.DataFrame(data, columns=["timestamp", "price"])
                df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
                return df
            except requests.RequestException as e:
                print(f"Attempt {attempt + 1}: Error fetching data for {coin_id} - {e}")
                if attempt < retries - 1:
                    time.sleep(2)  # Wait before retrying
                else:
                    raise


# Main Execution
if __name__ == "__main__":
    try:
        print("Fetching top 10 volatile coins...")
        top_coins = CoinGeckoAPI.get_top_volatile_coins(top_n=10)
        for i, coin in enumerate(top_coins, start=1):
            print(f"{i}. {coin['name']} ({coin['symbol']}): {coin['price_change_percentage_24h']}%")
    except requests.RequestException as e:
        print(f"Error accessing CoinGecko API: {e}")