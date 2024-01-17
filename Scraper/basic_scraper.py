import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin

def sanitize_filename(filename):
    # Replace invalid characters with underscores
    invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename

def save_data_to_file(data, directory, filename):
    os.makedirs(directory, exist_ok=True)
    filename = sanitize_filename(filename)
    filepath = os.path.join(directory, filename)
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(data)
    print(f"Data saved to: {filepath}")

def web_crawler_with_saving_and_urls(url, data_directory='data'):
    # Send an HTTP request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract information or perform actions based on your needs
        # For example, print the absolute URLs of all the links on the page
        base_url = response.url
        urls_set = set()
        for link in soup.find_all('a'):
            relative_url = link.get('href')
            if relative_url:
                absolute_url = urljoin(base_url, relative_url)
                urls_set.add(absolute_url)

        # Save the entire HTML content to a file
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f"{url.replace('://', '_').replace('/', '_')}_{timestamp}.html"
        save_data_to_file(response.text, data_directory, filename)

        return urls_set

    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return set()

def crawl_urls_set(urls_set, data_directory='data'):
    for url in urls_set:
        print(f"\nCrawling URL: {url}")
        web_crawler_with_saving_and_urls(url, data_directory)

# Example usage
url_to_crawl = "https://google.com"
found_urls = web_crawler_with_saving_and_urls(url_to_crawl)

# Print the found URLs
print("Found URLs:")
for url in found_urls:
    print(url)

# Rerun crawlers on each URL in urls_set
crawl_urls_set(found_urls)
