import requests
from bs4 import BeautifulSoup
import sqlite3
import argparse
from .constants import URL, DATABASE_FILE
from .filters import filter_entries_by_words_and_comments, filter_entries_by_words_and_points

# Function to scrape and load data
def scrape_news():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')

    entries = []
    items = soup.select('.athing')
    subtexts = soup.select('.subtext')

    for i in range(min(30, len(items))):
        item = items[i]
        subtext = subtexts[i]

        number = item.select_one('.rank').text.strip('.')
        title = item.select_one('.titleline').find('a').text
        score_element = subtext.select_one('.score')
        points = score_element.text.split()[0] if score_element else '0'
        comments = subtext.select('a')[-1].text.split()[0]

        entries.append({
            'number': int(number),
            'title': title,
            'points': int(points),
            'comments': int(comments) if comments.isnumeric() else 0
        })

    return entries

# Function to save data to SQLite
def save_to_db(entries):
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()

    c.execute("DROP TABLE IF EXISTS entries")

    c.execute('''
    CREATE TABLE entries (
        number INTEGER,
        title TEXT,
        points INTEGER,
        comments INTEGER
    )
    ''')

    for entry in entries:
        c.execute('''
        INSERT INTO entries (number, title, points, comments)
        VALUES (?, ?, ?, ?)
        ''', (entry['number'], entry['title'], entry['points'], entry['comments']))

    conn.commit()
    conn.close()

# Main CLI function
def main():
    parser = argparse.ArgumentParser(description='Y Combinator News Scraper and Filter')
    parser.add_argument('--scrape', action='store_true', help='Scrape News')
    parser.add_argument('--filter', choices=['comments', 'points'], help='Filter entries')
    args = parser.parse_args()

    if args.scrape:
        entries = scrape_news()
        save_to_db(entries)
        print("Scraping completed and data saved to database.")

    elif args.filter:
        if args.filter == 'comments':
            results = filter_entries_by_words_and_comments()
        elif args.filter == 'points':
            results = filter_entries_by_words_and_points()

        print("Number, Title, Points, Comments")
        for result in results:
            print(result)

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
