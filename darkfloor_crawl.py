import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
from concurrent.futures import ThreadPoolExecutor

def find_mp3_links(url, encountered_urls):
    response = requests.get(url)
    if response.status_code != 200:
        return None  # Indicate that the page doesn't exist or can't be accessed

    soup = BeautifulSoup(response.text, 'html.parser')
    mp3_links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.endswith('.mp3'):
            full_url = urljoin(url, href)
            if full_url not in encountered_urls:  # Avoid duplicates
                mp3_links.append(full_url)
                encountered_urls.add(full_url)
    return mp3_links if mp3_links else None

def download_mp3(url, directory='downloaded_mp3s', status_file='download_status.txt'):
    if not os.path.exists(directory):
        os.makedirs(directory)

    local_filename = os.path.join(directory, url.split('/')[-1])

    # Check if already downloaded
    if is_downloaded(local_filename, status_file):
        print(f"Already downloaded: {local_filename}")
        return

    # Download file
    with requests.get(url, stream=True) as r:
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    print(f"Downloaded: {local_filename}")

    # Mark as downloaded
    mark_as_downloaded(local_filename, status_file)

def is_downloaded(filename, status_file):
    if not os.path.exists(status_file):
        return False
    with open(status_file, 'r') as file:
        downloaded_files = file.readlines()
    return filename + '\n' in downloaded_files

def mark_as_downloaded(filename, status_file):
    with open(status_file, 'a') as file:
        file.write(filename + '\n')

if __name__ == '__main__':
    base_url = 'https://darkfloor.co.uk/mantisradio'
    encountered_urls = set()  # Track encountered .mp3 URLs

    number = 1  # Starting point for finding the upper limit
    while True:
        formatted_url = f"{base_url}{number}"
        print(f"Checking: {formatted_url}")
        mp3_links = find_mp3_links(formatted_url, encountered_urls)
        if mp3_links is None:
            break  # Stop if a page doesn't exist or has no .mp3 links
        number += 1

    max_number = number - 1  # Adjust for the last increment
    print(f"Upper limit found: {max_number}")

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = []
        for number in range(max_number, 0, -1):
            formatted_url = f"{base_url}{number}"
            print(f"Processing: {formatted_url}")
            mp3_links = find_mp3_links(formatted_url, encountered_urls)
            if mp3_links:
                for link in mp3_links:
                    futures.append(executor.submit(download_mp3, link))

        # Wait for all futures to complete
        for future in futures:
            future.result()
