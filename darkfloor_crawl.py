import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
from concurrent.futures import ThreadPoolExecutor

def find_mp3_links(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to access {url}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    mp3_links = [urljoin(url, link['href']) for link in soup.find_all('a', href=True) if link['href'].endswith('.mp3')]
    return mp3_links

def download_mp3(url, directory='downloaded_mp3s'):
    if not os.path.exists(directory):
        os.makedirs(directory)

    local_filename = os.path.join(directory, os.path.basename(url))
    if os.path.exists(local_filename):  # Skip download if file already exists
        print(f"Already downloaded: {local_filename}")
        return

    with requests.get(url, stream=True) as r:
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    print(f"Downloaded: {local_filename}")

if __name__ == '__main__':
    base_url = 'https://darkfloor.co.uk/mantisradio'
    max_number = 354  # Hardcoded upper limit

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = []
        for number in range(max_number, 0, -1):
            formatted_url = f"{base_url}{number}"
            print(f"Processing: {formatted_url}")
            mp3_links = find_mp3_links(formatted_url)
            for link in mp3_links:
                futures.append(executor.submit(download_mp3, link))

        # Wait for all futures to complete
        for future in futures:
            future.result()
