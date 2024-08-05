# Y News Scraper

This project scrapes the first 30 entries from Hacker News and stores the data in a SQLite database. It provides functionalities to filter the entries based on the number of words in the title and sort them by points or comments.

## Setup

1. Clone the repository.
   ```git clone https://github.com/mhumud/y_scrapper.git```
2. Create a virtual environment and activate it.
   ```python3 -m venv .venv```
3. Install the dependencies:
   ```pip install 'r requirements.txt'```

## Usage

1. Run the scraper:
   ```
   python3 -m src.scraper --scrape
   ```

2. Filter entries:
   - More than 5 words in title, ordered by comments:
     ```
     python3 -m src.scraper --filter comments
     ```

   - 5 or fewer words in title, ordered by points:
     ```
     python3 -m src.scraper --filter points
     ```

## Testing

Run the tests:
```
DATABASE_FILE='test_news.db' pytest
```
