import requests
from bs4 import BeautifulSoup
import csv
import time

BASE_URL = "https://www.islamweb.net"
SEARCH_URL = "https://www.islamweb.net/ar/fatwa/?page=websearch&stxt=prayer"

def get_fatwa_links(search_url):
    """
    Scrape all fatwa links from the search results page.
    """
    links = []
    while search_url:
        print(f"Scraping search page: {search_url}")
        resp = requests.get(search_url)
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text, 'html.parser')

        # Find all fatwa links on this page
        for a in soup.find_all('a', href=True):
            href = a['href']
            # Fatwa links usually look like /ar/fatwa/65115/
            if href.startswith('/ar/fatwa/') and href.count('/') == 4:
                full_url = BASE_URL + href
                if full_url not in links:
                    links.append(full_url)

        # Find link to next page, if any (adjust selector as needed)
        next_page = soup.find('a', string="التالي")  # Arabic for "Next"
        if next_page and 'href' in next_page.attrs:
            search_url = BASE_URL + next_page['href']
            time.sleep(1)
        else:
            break
    return links

def scrape_fatwa_page(url):
    """
    Scrape the question and answer from a fatwa page.
    """
    resp = requests.get(url)
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, 'html.parser')

    # Extract question (usually in <h1> or <title>)
    question = ""
    h1 = soup.find('h1')
    if h1:
        question = h1.get_text(strip=True)
    elif soup.title:
        question = soup.title.get_text(strip=True)

    # Extract answer (usually in <div class="fatwa-content">)
    answer = ""
    answer_div = soup.find('div', class_='fatwa-content')
    if answer_div:
        answer = answer_div.get_text(separator='\n', strip=True)
    else:
        # Try to find the answer in another div if needed
        main_content = soup.find('div', {'id': 'MainContent'})
        if main_content:
            answer = main_content.get_text(separator='\n', strip=True)

    return question, answer

def save_to_csv(data, filename='salah_fatwa.csv'):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Question', 'Answer'])
        for question, answer in data:
            writer.writerow([question, answer])

def main():
    fatwa_links = get_fatwa_links(SEARCH_URL)
    print(f"Found {len(fatwa_links)} fatwa links.")

    all_data = []
    for i, url in enumerate(fatwa_links):
        print(f"Scraping fatwa {i+1}/{len(fatwa_links)}: {url}")
        question, answer = scrape_fatwa_page(url)
        if question and answer:
            all_data.append((question, answer))
        time.sleep(1)  # Be polite to the server

    save_to_csv(all_data)
    print(f"Scraping complete. Saved {len(all_data)} items to salah_fatwa.csv.")

if __name__ == "__main__":
    main()

