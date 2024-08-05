import sqlite3
from datetime import datetime
from .constants import DATABASE_FILE

# Filter comments ordered by comments
def filter_entries_by_words_and_comments():
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()

    c.execute('''
    SELECT * FROM entries
    WHERE LENGTH(TRIM(title)) - LENGTH(REPLACE(TRIM(title), ' ', '')) + 1 > 5
    ORDER BY comments DESC
    ''')
    results = c.fetchall()
    conn.close()

    # Log the filter usage
    save_filter_usage('comments')

    return results

# Filter comments ordered by points
def filter_entries_by_words_and_points():
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()

    c.execute('''
    SELECT * FROM entries
    WHERE LENGTH(TRIM(title)) - LENGTH(REPLACE(TRIM(title), ' ', '')) + 1 <= 5
    ORDER BY points DESC
    ''')
    results = c.fetchall()
    conn.close()

    # Log the filter usage
    save_filter_usage('points')

    return results

# Function to save filter usage
def save_filter_usage(filter_type):
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()

    timestamp = datetime.now()
    c.execute('''
    CREATE TABLE IF NOT EXISTS filter_usage (
        filter_type TEXT,
        timestamp DATETIME
    )
    ''')

    c.execute('''
    INSERT INTO filter_usage (filter_type, timestamp)
    VALUES (?, ?)
    ''', (filter_type, timestamp))

    conn.commit()
    conn.close()
