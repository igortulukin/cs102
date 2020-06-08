import string

from bottle import (
    route, run, template, request, redirect
)

from scraputils import get_news
from db import News, session
from bayes import NaiveBayesClassifier

model = NaiveBayesClassifier()
s = session()
x, y = [], []


def clean(title):
    translator = str.maketrans("", "", string.punctuation)
    return title.translate(translator)


for n in s.query(News).all():
    x.append(clean(n.title).lower())
    y.append(n.label)
model.fit(x, y)
print(model.word_dict)


@route("/news")
def news_list():
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route("/add_label/<label>/<news_id>")
def add_label(label, news_id):
    news_item = s.query(News).filter(News.id == news_id).all()[0]
    news_item.label = label
    s.add(news_item)
    s.commit()
    redirect("/news")


@route("/classify")
def classify_news():
    news = get_news('https://news.ycombinator.com/newest', 3)
    news_titles = [news_item["title"] for news_item in news]
    news_urls = [news_item["url"] for news_item in news]
    news = list(zip(news_titles, news_urls))
    good = [f"{news[i][0]} {news[i][1]}" for i, p in enumerate(model.predict(news_titles)) if p == 'good']
    maybe = [news_titles[i] for i, p in enumerate(model.predict(news_titles)) if p == 'maybe']
    never = [news_titles[i] for i, p in enumerate(model.predict(news_titles)) if p == 'never']
    print(len(good), len(maybe), len(never))
    return template('news_recommendations', rows=good)


if __name__ == "__main__":
    run(host="localhost", port=8080)