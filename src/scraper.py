import requests
from bs4 import BeautifulSoup
import sqlite3
import argparse
from src.constants import URL, DATABASE_FILE
from src.filters import filter_entries_by_words_and_comments, filter_entries_by_words_and_points

# Function to scrape and load data
def scrape_news():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Filter the elements of the html that are being looked for
    entries = []
    items = soup.select('.athing')
    subtexts = soup.select('.subtext')

    for i in range(min(30, len(items))):
        item = items[i]
        subtext = subtexts[i]

        # Extract the desired elemnts
        number = int(item.select_one('.rank').text.strip('.'))
        title = item.select_one('.titleline').find('a').text
        score_element = subtext.select_one('.score')
        points = int(score_element.text.split()[0]) if score_element else 0
        subtext_element = subtext.select('a')[-1].text.split()[0]
        comments = int(subtext_element) if subtext_element.isnumeric() else 0

        # Append entries to list
        entries.append({
            'number': number,
            'title': title,
            'points': points,
            'comments': comments
        })

    return entries

# Function to save data to SQLite
def save_to_db(entries):
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()

    # Remove elements if table is already populated
    c.execute("DROP TABLE IF EXISTS entries")

    # Create table
    c.execute('''
    CREATE TABLE entries (
        number INTEGER,
        title TEXT,
        points INTEGER,
        comments INTEGER
    )
    ''')

    # Insert elements into table
    for entry in entries:
        c.execute('''
        INSERT INTO entries (number, title, points, comments)
        VALUES (?, ?, ?, ?)
        ''', (entry['number'], entry['title'], entry['points'], entry['comments']))

    conn.commit()
    conn.close()

# Main CLI function
def main():
    # Parser for easier CLI usage
    parser = argparse.ArgumentParser(description='Y Combinator News Scraper and Filter')
    parser.add_argument('--scrape', action='store_true', help='Scrape News')
    parser.add_argument('--filter', choices=['comments', 'points'], help='Filter entries')
    args = parser.parse_args()

    # Scrape the webpage
    if args.scrape:
        entries = scrape_news()
        save_to_db(entries)
        print("Scraping completed and data saved to database.")

    # Filter the database
    elif args.filter:
        if args.filter == 'comments':
            results = filter_entries_by_words_and_comments()
        elif args.filter == 'points':
            results = filter_entries_by_words_and_points()

        print("Number, Title, Points, Comments")
        for result in results:
            print(result)

    # Print the help menu
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
