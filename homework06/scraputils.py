# coding=utf-8
from time import sleep
import requests
from bs4 import BeautifulSoup


def extract_news(parser):
    """ Extract news from a given web page """
    news_list = []
    main_table = parser.find("table", {"class": "itemlist"})
    items_list = main_table.find_all("tr")
    more_link = main_table.find("a", {"class": "morelink"})
    for i in range(0, 90, 3):
        tr1 = items_list[i]
        tr2 = items_list[i+1]
        link = tr1.find("a", {"class": "storylink"})
        title = link.text
        url = link["href"]
        if url[:5] != 'https':
            url = 'https://news.ycombinator.com/' + url
        points = int(tr2.find("span", {"class": "score"}).text.split()[0])
        author = tr2.find("a", {"class": "hnuser"}).text
        comments = tr2.find_all("a")[-1].text
        comments_value = 0 if comments == "discuss" else int(comments.split()[0])
        news_list.append({
            'author': author,
            'points': points,
            'title': title,
            'url': url
        })
    return news_list, more_link["href"]


def get_news(url, n_pages=1):
    """ Collect news from a given web page """
    news = []
    for i in range(n_pages):
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list, next_page = extract_news(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        sleep(2)
    return news

print(get_news('https://news.ycombinator.com/newest'))