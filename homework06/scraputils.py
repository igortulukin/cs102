from time import sleep

import requests
from bs4 import BeautifulSoup


def extract_news(parser):
    news_list = []
    t_body = parser.find("table", {"class": "itemlist"})
    items_list = t_body.find_all("tr")
    more_link = t_body.find("a", {"class": "morelink"})
    for i in range(0, 90, 3):
        tr1 = items_list[i]
        tr2 = items_list[i + 1]
        link = tr1.find("a", {"class": "storylink"})
        title = link.text
        url = link["href"]
        try:
            domain = tr1.find("span", {"class": "sitestr"}).text
        except AttributeError:
            domain = 'news.ycombinator.com'
        try:
            author = tr2.find("a", {"class": "hnuser"}).text
            points = int(tr2.find("span", {"class": "score"}).text.split()[0])
            comments = tr2.find_all("a")[-1].text
            comments_value = 0 if comments == "discuss" else int(comments.split()[0])
            news_list.append({
                "author": author,
                "comments": comments_value,
                "points": points,
                "title": title,
                "url": url,
                "domain": domain
            })
        except AttributeError:
            continue
    return news_list, more_link["href"]


def get_news(url, n_pages=1):
    news = []
    for oops in range(n_pages):
        print(f"Collecting data from page: {url}")
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list, next_page = extract_news(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        sleep(2)
    return news