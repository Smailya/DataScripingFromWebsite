# Salah Fatwa Scraper

This Python script scrapes fatwa questions and answers related to Salah (prayer) from [Islamweb.net](https://www.islamweb.net). It searches for fatwa links, extracts the relevant content, and saves the data into a CSV file named `salah_fatwa.csv`.

## Features

- Navigates through search result pages to collect all relevant fatwa links.
- Extracts questions and answers from each fatwa page.
- Saves the extracted data into a structured CSV file.

## Requirements

- Python 3.x
- `requests` library
- `beautifulsoup4` library

## Installation

Install the required libraries using pip:

```bash
pip install requests beautifulsoup4
```

## Usage

1. Clone or download this repository.
2. Run the script:

```bash
python salah_fatwa_scraper.py
```

The script will:

- Scrape all fatwa links related to prayer.
- Visit each link to extract questions and answers.
- Save the results into `salah_fatwa.csv`.

## Notes

- The script includes polite delays (`time.sleep(1)`) between requests to avoid overwhelming the server.
- The script assumes certain HTML structures; if the website changes its layout, some selectors may need updating.
- You can modify the `SEARCH_URL` variable if you want to scrape different topics or pages.

## License

This project is for educational purposes. Use responsibly and ethically.

---

**Happy Scraping!**
