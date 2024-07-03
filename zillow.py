from dotenv import load_dotenv
import os
import pandas as pd
import requests
import warnings
from datetime import date
import json

# settings
warnings.filterwarnings("ignore")
pd.set_option("display.max_columns", None)


def main():
    configure()
    api_key, listing_url = get_token()
    listing_response = get_listings(api_key, listing_url)
    process_listing(listing_response)

def configure():
    load_dotenv()

def get_token():
    api = os.getenv('api')
    url = os.getenv('url')
    return(api,url)


def get_listings(api_key, listing_url):
    url = "https://app.scrapeak.com/v1/scrapers/zillow/listing"

    querystring = {
        "api_key": api_key,
        "url":listing_url
    }

    return requests.request("GET", url, params=querystring)

def process_listing(listing_response):
    today = date.today().strftime("%y.%m.%d")
    print(listing_response.json().keys())

    num_of_properties = listing_response.json()["data"]["categoryTotals"]["cat1"]["totalResultCount"]
    print("Count of properties:", num_of_properties)
    df_listings = pd.json_normalize(listing_response.json()["data"]["cat1"]["searchResults"]["mapResults"])
    df_listings.to_csv("zillow." + today +".csv", index = False)

    text = json.dumps(listing_response.json(),sort_keys = True, indent = 4)


    with open("zillow."+ today +".json", "w", encoding="utf-8") as f:
        f.write(text)


if __name__ == '__main__':
    main()