"""Module with tests for the test module."""
import sqlite3
from src.filters import filter_entries_by_words_and_comments, filter_entries_by_words_and_points
from src.constants import DATABASE_FILE

def populate_test_db():
    """Populate the test database with dummy data"""
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

    mock_data = [
        (1, 'Short title with many words', 100, 50),
        (2, 'Short title', 20, 10),
        (3, 'Another short title', 180, 30),
        (4, 'Another much longer title this time', 15, 60),
        (5, 'This one is also very very long', 80, 70),
    ]
    c.executemany("INSERT INTO entries VALUES (?, ?, ?, ?)", mock_data)
    conn.commit()
    conn.close()
# Run the population first
populate_test_db()

def test_filter_entries_by_words_and_comments():
    """Function that checks the comments function"""
    results = filter_entries_by_words_and_comments()

    # Check that the filter is working correctly
    assert len(results) == 2
    # Check that the sorting is working correctly
    assert results[0][1] == 'This one is also very very long'
    assert results[0][3] == 70

def test_filter_entries_by_words_and_points():
    """Function that checks the points function"""
    results = filter_entries_by_words_and_points()

    # Check that the filter is working correctly
    assert len(results) == 3
    # Check that the sorting is working correctly
    assert results[0][1] == 'Another short title'
    assert results[0][2] == 180
