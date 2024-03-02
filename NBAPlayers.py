from bs4 import BeautifulSoup
import requests
import re

import csv
import string


core_url = 'https://www.basketball-reference.com/players/LETTER/'
players = []

def new_url(letter):
    target_url = core_url.replace('LETTER',letter)
    return target_url

#scrape
def scrape_curr_page(letter):
    target_url = new_url(letter)
    response = requests.get(target_url)
    
    soup = BeautifulSoup(response.content, 'html.parser')
    tbody = soup.find('tbody')

    for tr in tbody.find_all('tr'):
        # Extract the player's name
        player_name = tr.find('th', {'data-stat': 'player'}).text
        
        # Extract the 'From' year
        from_year = tr.find('td', {'data-stat': 'year_min'}).text
        
        # Append the data to the players_data list
        players.append({'Player Name': player_name, 'From Year': from_year})
    
#add to CSV
def write_to_csv():
    csv_file_name = 'all_NBA_players.csv'
    fieldnames = ['Player Name', 'From Year']
    with open(csv_file_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for player in players:
            writer.writerow(player)
    print(f"Data has been written to {csv_file_name}")


for letter in list(string.ascii_lowercase):
    scrape_curr_page(letter)

write_to_csv()