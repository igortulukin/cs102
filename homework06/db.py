from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from scraputils import get_news

Base = declarative_base()
engine = create_engine("sqlite:///news_marked.db")
session = sessionmaker(bind=engine)


class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key = True)
    title = Column(String)
    author = Column(String)
    url = Column(String)
    domain = Column(String)
    comments = Column(Integer)
    points = Column(Integer)
    label = Column(String)


Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    s = session()

    for n in get_news('https://news.ycombinator.com/newest', 34):
        news_item = News(
            title=n['title'],
            author=n['author'],
            url=n['url'],
            domain=n['domain'],
            comments=n['comments'],
            points=n['points'],
        )
        s.add(news_item)

    s.commit()