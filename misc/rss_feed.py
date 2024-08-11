############
#
# Extract Titles from RSS feed
#
# Implement get_headlines() function. It should take a url of an RSS feed
# and return a list of strings representing article titles.
#
############
import requests
from bs4 import BeautifulSoup


google_news_url = "https://news.google.com/news/rss"


def get_headlines(rss_url):
    """
    @returns a list of titles from the rss feed located at `rss_url`
    """
    feed_content = requests.get(rss_url).content
    soup = BeautifulSoup(feed_content, 'lxml-xml')
    feed_items = soup.find_all('item')

    return [item.find('title').text for item in feed_items]


if __name__ == '__main__':
    print(get_headlines(google_news_url))
