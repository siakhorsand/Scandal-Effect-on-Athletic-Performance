from bs4 import BeautifulSoup
from selenium import webdriver
import time
import csv

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)
core_url = 'https://twitter.com/search?q=(nfl%20OR%20mlb%20OR%20nba)%20(from%3AMailOnline%20OR%20from%3ATMZ%20OR%20from%3AYahooNews%20OR%20from%3ANYTimes%20OR%20from%3ACNN%20OR%20from%3AFoxNews%20OR%20from%3ANYPost%20OR%20from%3Aguardian%20OR%20from%3ARollingStone%20OR%20from%3ACBS%20OR%20from%3Awashingtonpost)%20until%3A_ENDDATE_%20since%3A_STARTDATE_%20-filter%3Areplies&src=typed_query&f=top'
tweets = []

def new_url(start_month, year):
    end_year = year
    if(start_month == 11):
        end_month = 1
        end_year = year + 1
    else:
        end_month = start_month + 2
    
    
    
    year = str(year)
    end_year = str(end_year)
    start_month = str(start_month)
    end_month = str(end_month)

    target_url = core_url.replace('_STARTDATE_',year+'-'+start_month+'-01').replace('_ENDDATE_',end_year+'-'+end_month+'-01')
    return target_url

def scroll_page():
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#scrape
def scrape_curr_page(start_month,curr_year):
    target_url = new_url(start_month,curr_year)
    driver.get(target_url)
    for i in range(5):
        time.sleep(7)  
        resp = driver.page_source
        soup = BeautifulSoup(resp, 'html.parser')
        
        for tweet in soup.find_all("div", {"data-testid": "cellInnerDiv"}):
            tweet_text_element = tweet.find("div", {"data-testid": "tweetText"})
            if tweet_text_element:
                tweet_text = tweet_text_element.get_text().strip()
            else:
                tweet_text = ""
            
            tweet_user_element = tweet.find('a', href=True) 
            tweet_date_element = tweet.find('time')
            
            if tweet_user_element and tweet_date_element:
                tweet_user = tweet_user_element.get('href')
                tweet_date = tweet_date_element.get('datetime')
                tweets.append({'date': tweet_date, 'text': tweet_text, 'user': tweet_user})
                
        scroll_page()
    
#add to CSV
def write_to_csv():
    csv_file_name = 'tweets.csv'
    fieldnames = ['date', 'text', 'user']
    with open(csv_file_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for tweet in tweets:
            clean_text = tweet['text'].replace('\n', ' ')
            writer.writerow({'date': tweet['date'], 'text': clean_text, 'user': tweet['user']})
    print(f"Data has been written to {csv_file_name}")

start_months = [1,3,5,7,9,11]

for year in range(2013,2023):
    for start_month in start_months:
        scrape_curr_page(start_month, year)
        time.sleep(2)

write_to_csv()
