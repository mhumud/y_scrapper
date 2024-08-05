import requests
from bs4 import BeautifulSoup
import sqlite3

# Function to scrape data
def scrape_news():
    url = 'https://news.ycombinator.com/'
    response = requests.get(url)
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

    save_to_db(entries)

# Function to save data to SQLite
def save_to_db(entries):
    conn = sqlite3.connect('y_news.db')
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

# Filter comments ordered by comments
def filter_entries_by_words_and_comments():
    conn = sqlite3.connect('y_news.db')
    c = conn.cursor()

    c.execute('''
    SELECT * FROM entries
    WHERE LENGTH(TRIM(title)) - LENGTH(REPLACE(TRIM(title), ' ', '')) + 1 > 5
    ORDER BY comments DESC
    ''')
    results = c.fetchall()
    conn.close()
    return results

# Filter comments ordered by points
def filter_entries_by_words_and_points():
    conn = sqlite3.connect('y_news.db')
    c = conn.cursor()

    c.execute('''
    SELECT * FROM entries
    WHERE LENGTH(TRIM(title)) - LENGTH(REPLACE(TRIM(title), ' ', '')) + 1 <= 5
    ORDER BY points DESC
    ''')
    results = c.fetchall()
    conn.close()
    return results
