# Y News Scraper

This project scrapes the first 30 entries from Hacker News and stores the data in a SQLite database. It provides functionalities to filter the entries based on the number of words in the title and sort them by points or comments.

## Setup

1. Clone this repository:
   ```git clone https://github.com/mhumud/y_scrapper.git```
2. Create a virtual environment and activate it:
   ```python3 -m venv .venv```
3. Install the dependencies:
   ```pip install -r requirements.txt```

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

For simplicity, a specific DB will be used for testing the functions. In the future an in-memory database would be more adequate.

# Architectural Decision Record (ADR)
## Web Scraper and Filtering System for Y Combinator News


### Context and Problem Statement
We need to create a web crawler to scrape the first 30 entries from Y Combinator News, extract specific data fields, store the data, and provide filtering options. The solution should be efficient, maintainable, and easy to use, with a focus on clean code, modularity, and proper documentation.

### Decision Drivers
- Proficiency: The solution should be implemented in a language that the developer is proficient in. For this case, Python is chosen.
- Modularity: The code should be modular and follow good object-oriented/functional programming practices.
- Ease of Use: The system should provide a simple command-line interface (CLI) for scraping and filtering operations.
- Data Persistence: The system should persist the scraped data and filter usage data in a storage mechanism.
- Documentation: Proper documentation and version control practices should be followed.


### Considered Options
- Using a Python script with BeautifulSoup for scraping, SQLite for storage, and argparse for CLI.
- Using a JavaScript-based solution with Node.js and Puppeteer for scraping, and a NoSQL database for storage.
- Using a web framework like Django or Flask to create a web interface for the scraper and filters.


### Decision Outcome
Chosen Option: Option 1 - Using a Python script with BeautifulSoup for scraping, SQLite for storage, and argparse for CLI.
Reasoning:
- Python’s BeautifulSoup is excellent for web scraping and is easy to use.
- SQLite provides a lightweight and easy-to-set-up database solution.
- argparse allows for straightforward command-line interface creation.

This combination aligns well with the requirement for clean, modular code and ease of use.

### Pros and Cons of the Options
#### Option 1: Python Script with BeautifulSoup, SQLite, and argparse
Pros:

- Familiarity: Developer is proficient in Python.
- Simplicity: Easy to set up and run.
- Modularity: Allows for clean separation of concerns.
- Community Support: Strong community support and extensive documentation.

Cons:

- Limited Scalability: Not suitable for very high-frequency scraping or large-scale data storage.

#### Option 2: JavaScript-based Solution with Node.js and Puppeteer
Pros:

- Modern: Leverages modern JavaScript ecosystem.
- Powerful: Puppeteer provides powerful browser automation capabilities.

Cons:

- Learning Curve: Requires more setup and learning if not already proficient in Node.js and Puppeteer.
- Complexity: More complex setup compared to the chosen Python solution.

#### Option 3: Web Framework like Django or Flask

Pros:

- Rich Features: Provides built-in support for database handling, templating, and routing.
- Extensibility: Easy to extend with more features like a web interface.

Cons:

- Overkill: Adds unnecessary complexity for the given requirements.
- Setup: Requires more setup and configuration.
