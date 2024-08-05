import os

URL = "https://news.ycombinator.com/"
# Allow override for testing purposes
DATABASE_FILE = os.environ.get('DATABASE_FILE', 'y_news.db')
