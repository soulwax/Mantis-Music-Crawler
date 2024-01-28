import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def find_mp3_links(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to access {url}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    mp3_links = [urljoin(url, link['href']) for link in soup.find_all('a', href=True) if link['href'].endswith('.mp3')]
    return mp3_links

def save_mp3_links(mp3_links, filename='mp3_links.txt'):
    with open(filename, 'a') as file:  # 'a' to append to the file
        for link in mp3_links:
            file.write(link + '\n')

if __name__ == '__main__':
    base_url = 'https://darkfloor.co.uk/mantisradio'
    max_number = 354  # Starting point

    for number in range(max_number, 0, -1):  # Descend from max_number to 1
        formatted_url = f"{base_url}{number}"
        print(f"Processing: {formatted_url}")
        mp3_links = find_mp3_links(formatted_url)
        if mp3_links:
            save_mp3_links(mp3_links)
        else:
            print(f"No MP3 links found at {formatted_url}")
