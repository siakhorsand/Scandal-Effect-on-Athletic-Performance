from bs4 import BeautifulSoup
import requests
import re

import csv
import string


core_url = 'https://www.pro-football-reference.com/players/LETTER/'
players = []

def new_url(letter):
    target_url = core_url.replace('LETTER',letter)
    return target_url

#scrape
def scrape_curr_page(letter):
    target_url = new_url(letter)
    response = requests.get(target_url)
    
    soup = BeautifulSoup(response.content, 'html.parser')
    players_div = soup.find('div', id='div_players')

    for p_tag in players_div.find_all('p'):
        name = p_tag.find('a').text
        p_text = p_tag.text
        position_years = re.search(r'\((.*?)\)\s*(\d{4}-\d{4})', p_text)
    
        if position_years:
            position = position_years.group(1)
            years = position_years.group(2).split('-')
        else:
            position = ''
            years = ['', '']

        players.append({
            'Name': name,
            'Position': position,
            'Start Year': years[0],
            'End Year': years[1]
        })
    
#add to CSV
def write_to_csv():
    csv_file_name = 'all_NFL_players.csv'
    fieldnames = ['Name', 'Position', 'Start Year', 'End Year']
    with open(csv_file_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for player in players:
            writer.writerow(player)
    print(f"Data has been written to {csv_file_name}")


for letter in list(string.ascii_uppercase):
    scrape_curr_page(letter)

write_to_csv()