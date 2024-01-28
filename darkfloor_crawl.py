from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def get_mp3_links(url):
    # Setup Selenium WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get(url)

    # Wait for the page to load
    time.sleep(5)  # Adjust the sleep time as needed

    # Find all download links or buttons (you might need to adjust the selector)
    download_elements = driver.find_elements(By.CSS_SELECTOR, "a[href$='.mp3']")

    mp3_links = [element.get_attribute('href') for element in download_elements]

    driver.quit()
    return mp3_links

def save_mp3_links(mp3_links, filename='mp3_links.txt'):
    with open(filename, 'w') as file:
        for link in mp3_links:
            file.write(link + '\n')
    print(f"Saved {len(mp3_links)} MP3 links to {filename}")

if __name__ == '__main__':
    url = 'https://darkfloor.co.uk/mantisradio/'
    mp3_links = get_mp3_links(url)
    save_mp3_links(mp3_links)
