# scrape.py
import requests
from bs4 import BeautifulSoup
import json

def scrape_animal_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    animal_data = []

    # Find the table containing the animal data (adjust the selector as needed)
    table = soup.find('table', {'class': 'wikitable'})
    if table:
        rows = table.find_all('tr')
        for row in rows[1:]:  # Skip the header row
            cols = row.find_all('td')
            if cols:
                animal = {
                    'name': cols[0].text.strip(),
                    'breed': cols[1].text.strip() if len(cols) > 1 else 'Unknown',
                    'age': cols[2].text.strip() if len(cols) > 2 else 'Unknown',
                    'image_url': 'https:' + cols[3].find('img')['src'] if len(cols) > 3 and cols[3].find('img') else None
                }
                animal_data.append(animal)

    return animal_data

# Example usage
if __name__ == '__main__':
    url = 'https://en.wikipedia.org/wiki/List_of_domesticated_animals'
    animals = scrape_animal_data(url)

    # Save the scraped data to a JSON file
    with open('animals.json', 'w') as f:
        json.dump(animals, f, indent=4)
