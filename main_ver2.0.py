#%% [markdown]
# Final Project <br>
# Name: Brian Kim <br>
# Reference:
# 1. https://www.udemy.com/course/100-days-of-code/?couponCode=JUST4U02223
# 2. https://0goodmorning.tistory.com/66
# 3. https://m.blog.naver.com/scienleader/223173830206

'''Stock_Trading_News_Alert'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
from twilio.rest import Client

VIRTUAL_TWILIO_NUMBER = "+1"
VERIFIED_NUMBER = "+2"

STOCK_NAMES = ["TSLA", "IONQ", "NVDA"]
COMPANY_NAMES = {"TSLA": "Tesla", "IONQ": "IonQ", "NVDA": "Nvidia"}

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything/"

STOCK_API_KEY = "1"
NEWS_API_KEY = "2"
TWILIO_SID = "3"
TWILIO_AUTH_TOKEN = "4"


#%%
for STOCK_NAME in STOCK_NAMES:
    COMPANY_NAME = COMPANY_NAMES[STOCK_NAME]

    # Get stock data
    stock_params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": STOCK_NAME,
        "apikey": STOCK_API_KEY,
    }
    response = requests.get(STOCK_ENDPOINT, params=stock_params)

    if response.status_code == 200:
        data = response.json()
        if "Time Series (Daily)" in data:
            data_list = [value for (key, value) in data["Time Series (Daily)"].items()]
            yesterday_data = data_list[0]
            yesterday_closing_price = round(float(yesterday_data["4. close"]), 2)
            day_before_yesterday_data = data_list[1]
            day_before_yesterday_closing_price = round(float(day_before_yesterday_data["4. close"]), 2)

            # Calculate the price change percentage
            difference = yesterday_closing_price - day_before_yesterday_closing_price
            up_down = "🔺" if difference > 0 else "🔻"
            diff_percent = round((difference / day_before_yesterday_closing_price) * 100, 2)
            
            # Data Print
            print(STOCK_NAME)
            print(yesterday_closing_price)
            print(day_before_yesterday_closing_price)
            print(diff_percent)

            # Check if the difference is greater than 3%
            if abs(diff_percent) > 3:
                # Fetch news if significant stock change
                news_params = {
                    "apiKey": NEWS_API_KEY,
                    "qInTitle": COMPANY_NAME,
                }
                news_response = requests.get(NEWS_ENDPOINT, params=news_params)
                if news_response.status_code == 200:
                    articles = news_response.json().get("articles", [])
                    three_articles = articles[:3]

                    # Prepare messages with news info including URLs
                    formatted_articles = [
                        f"{STOCK_NAME}: {up_down}{diff_percent}%, {yesterday_closing_price}\nHeadline: {article['title']}.\nBrief: {article['description']}\nRead more: {article['url']}"
                        for article in three_articles
                    ]
                    # Print messages before sending
                    for article_message in formatted_articles:
                        print("Prepared message:", article_message)

                    # Send messages via Twilio
                    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
                    for article_message in formatted_articles:
                        message = client.messages.create(
                            body=article_message,
                            from_=VIRTUAL_TWILIO_NUMBER,
                            to=VERIFIED_NUMBER
                        )
                else:
                    print(f"Failed to retrieve news for {STOCK_NAME}. Status code: {news_response.status_code}, Response: {news_response.text}")
        else:
            print(f"Data not found in API response for {STOCK_NAME}. Here's what was returned:\n{data}")
    else:
        print(f"Failed to retrieve data for {STOCK_NAME}. Status code: {response.status_code}, Response: {response.text}")

# for STOCK_NAME in STOCK_NAMES:
#     COMPANY_NAME = COMPANY_NAMES[STOCK_NAME]

#     # Get stock data
#     stock_params = {
#         "function": "TIME_SERIES_DAILY",
#         "symbol": STOCK_NAME,
#         "apikey": STOCK_API_KEY,
#     }
#     response = requests.get(STOCK_ENDPOINT, params=stock_params)

#     # Check if the response contains the expected data
#     if response.status_code == 200:
#         data = response.json()
#         if "Time Series (Daily)" in data:
#             data_list = [value for (key, value) in data["Time Series (Daily)"].items()]
#             yesterday_data = data_list[0]
#             yesterday_closing_price = yesterday_data["4. close"]
#             day_before_yesterday_data = data_list[1]
#             day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]

#             # Calculate the price change percentage
#             difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
#             up_down = "🔺" if difference > 0 else "🔻"
#             diff_percent = round((difference / float(day_before_yesterday_closing_price)) * 100, 2)
            
#             # Data Print
#             print(STOCK_NAME)
#             print(yesterday_closing_price)
#             print(day_before_yesterday_closing_price)
#             print(diff_percent)

#             # Check if the difference is greater than 5%
#             if abs(diff_percent) > 5:
#                 # Fetch news if significant stock change
#                 news_params = {
#                     "apiKey": NEWS_API_KEY,
#                     "qInTitle": COMPANY_NAME,
#                 }
#                 news_response = requests.get(NEWS_ENDPOINT, params=news_params)
#                 if news_response.status_code == 200:
#                     articles = news_response.json().get("articles", [])
#                     three_articles = articles[:3]

#                     # Prepare messages with news info including URLs
#                     formatted_articles = [
#                         f"{STOCK_NAME}: {up_down}{diff_percent}%,{yesterday_closing_price}\nHeadline: {article['title']}.\nBrief: {article['description']}\nRead more: {article['url']}"
#                         for article in three_articles
#                     ]
#                     # Print messages before sending
#                     for article_message in formatted_articles:
#                         print("Prepared message:", article_message)

#                     # Send messages via Twilio
#                     client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
#                     for article_message in formatted_articles:
#                         message = client.messages.create(
#                             body=article_message,
#                             from_=VIRTUAL_TWILIO_NUMBER,
#                             to=VERIFIED_NUMBER
#                         )
#                 else:
#                     print(f"Failed to retrieve news for {STOCK_NAME}. Status code: {news_response.status_code}, Response: {news_response.text}")
#         else:
#             print(f"Data not found in API response for {STOCK_NAME}. Here's what was returned:\n{data}")
#     else:
#         print(f"Failed to retrieve data for {STOCK_NAME}. Status code: {response.status_code}, Response: {response.text}")


# %%[markdown]
# Stock Company Youtube Crawling
'''Stock Company Youtube Crawling'''
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup
import csv
import os

COMPANIES = {
    'Tesla': 'https://www.youtube.com/results?search_query=Tesla+stock',
    'IonQ': 'https://www.youtube.com/results?search_query=IonQ+stock',
    'Nvidia': 'https://www.youtube.com/results?search_query=Nvidia+stock'
}

def fetch_youtube_links(search_url):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(search_url)
    
    time.sleep(1.5)
    for _ in range(4):
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        time.sleep(0.3)

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    video_list = soup.find('div', {'id': 'contents'})
    video_items = video_list.find_all('ytd-video-renderer', {'class': 'style-scope ytd-item-section-renderer'})
    
    base_url = 'https://www.youtube.com'
    video_urls = [base_url + item.find('a', {'id': 'video-title'}).get('href') for item in video_items]
    
    driver.quit()
    return video_urls

# Specify the output directory
output_directory = '/Users/brian/Documents/GitHub/Stock_Trading_News_Alert'
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Define the filename in the specified directory
filename = os.path.join(output_directory, "youtube_video_links.csv")

with open(filename, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Company', 'Video URL'])
    for company, url in COMPANIES.items():
        print(f"Fetching YouTube links for {company}")
        links = fetch_youtube_links(url)
        print(f"Found {len(links)} videos for {company}")
        for link in links:
            writer.writerow([company, link])

print(f"Data has been written to {filename}")



# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
# import time
# from bs4 import BeautifulSoup
# import csv
# import tempfile

# COMPANIES = {
#     'Tesla': 'https://www.youtube.com/results?search_query=Tesla+stock',
#     'IonQ': 'https://www.youtube.com/results?search_query=IonQ+stock',
#     'Nvidia': 'https://www.youtube.com/results?search_query=Nvidia+stock'
# }

# def fetch_youtube_links(search_url):
#     # Setup Chrome options
#     chrome_options = Options()
#     chrome_options.add_argument('--headless')  # Run in headless mode to avoid UI rendering
#     # Initialize WebDriver with ChromeDriverManager
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
#     driver.get(search_url)
    
#     time.sleep(1.5)  # Allow page to load
#     for _ in range(4):
#         driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
#         time.sleep(0.3)

#     # Extract video links
#     html = driver.page_source
#     soup = BeautifulSoup(html, 'lxml')
#     video_list = soup.find('div', {'id': 'contents'})
#     video_items = video_list.find_all('ytd-video-renderer', {'class': 'style-scope ytd-item-section-renderer'})
    
#     base_url = 'https://www.youtube.com'
#     video_urls = [base_url + item.find('a', {'id': 'video-title'}).get('href') for item in video_items]
    
#     driver.quit()
#     return video_urls

# # Using a temporary file to write the CSV
# with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv', newline='', encoding='utf-8') as file:
#     writer = csv.writer(file)
#     writer.writerow(['Company', 'Video URL'])
#     for company, url in COMPANIES.items():
#         print(f"Fetching YouTube links for {company}")
#         links = fetch_youtube_links(url)
#         print(f"Found {len(links)} videos for {company}")
#         for link in links:
#             writer.writerow([company, link])
#     print("CSV file has been written to:", file.name)
