import requests
from bs4 import BeautifulSoup
import csv
import time

# Base URL for searching questions related to Salah (prayer)
SEARCH_URL = "https://www.islamweb.net/ar/fatwa/index.php?page=1&query=الصلاة"

def get_questions_answers(page=1):
    """
    Fetches questions and answers related to Salah from the search results page.
    """
    url = f"https://www.islamweb.net/ar/fatwa/index.php?page={page}&query=الصلاة"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve page {page}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all question blocks - this depends on the website's HTML structure
    # Here, we assume each question is in a div with class 'fatwa-item' (example)
    # You need to inspect the actual HTML structure for accuracy.
    questions = []

    fatwa_items = soup.find_all('div', class_='fatwa-item')  # Adjust class as per actual HTML
    if not fatwa_items:
        print("No fatwa items found on this page.")
        return []

    for item in fatwa_items:
        question_tag = item.find('a', class_='fatwa-title')  # Adjust selector as needed
        if not question_tag:
            continue
        question_text = question_tag.get_text(strip=True)
        question_link = "https://www.islamweb.net" + question_tag['href']

        # Fetch the detailed answer page
        answer_response = requests.get(question_link)
        if answer_response.status_code != 200:
            print(f"Failed to retrieve answer for question: {question_text}")
            continue
        answer_soup = BeautifulSoup(answer_response.text, 'html.parser')

        # Extract the answer text - adjust selector based on actual HTML
        answer_div = answer_soup.find('div', class_='fatwa-content')
        if not answer_div:
            answer_text = "Answer not found"
        else:
            answer_text = answer_div.get_text(separator='\n', strip=True)

        questions.append((question_text, answer_text))
        time.sleep(1)  # polite delay to avoid hammering the server

    return questions

def save_to_csv(data, filename='salah_fatwa.csv'):
    """
    Saves the list of (question, answer) tuples to a CSV file.
    """
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Question', 'Answer'])
        for question, answer in data:
            writer.writerow([question, answer])

def main():
    all_data = []
    max_pages = 5  # Number of pages to scrape - adjust as needed

    for page in range(1, max_pages + 1):
        print(f"Scraping page {page}...")
        page_data = get_questions_answers(page)
        if not page_data:
            break
        all_data.extend(page_data)
        time.sleep(2)  # polite delay between pages

    print(f"Total questions retrieved: {len(all_data)}")
    save_to_csv(all_data)
    print("Data saved to salah_fatwa.csv")

if __name__ == "__main__":
    main()
