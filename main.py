import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from urllib.parse import urljoin
from model import Book, Base
from sqlalchemy.dialects.sqlite import insert


def parse_all_pages():
    rate_to_number = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

    base = "http://books.toscrape.com/"
    next_url = base
    store_ = []

    while next_url:
        resp = requests.get(next_url, timeout=20)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.content, "lxml")
        books = soup.find_all("article", class_="product_pod")

        for book in books:
            rel_img = book.find("img")["src"]
            img_url = urljoin(base, rel_img)

            rel_link = book.find("h3").find("a")["href"]
            product_url = urljoin(base, rel_link)

            rating_word = book.find("p", class_="star-rating")["class"][1]
            rating = rate_to_number.get(rating_word)

            title = book.find("h3").find("a")["title"]

            price_text = book.find("p", class_="price_color").get_text(strip=True)
            price = float(price_text.replace("£", ""))

            store_.append({
                "product_url": product_url,
                "img_url": img_url,
                "rating": rating,
                "title": title,
                "price": price
            })

        next_link = soup.select_one("li.next a")
        next_url = urljoin(next_url, next_link["href"]) if next_link else None

    return store_

def save_to_db(store):
    engine = create_engine("sqlite:///my_books.db")
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()


    stmt = insert(Book).values(store).prefix_with("OR IGNORE")
    session.execute(stmt)
    session.commit()

    session.commit()

    books = session.query(Book).limit(5).all()
    for b in books:
        print(b.id, b.title, b.rating, b.price)

    session.close()


if __name__ == "__main__":
    store = parse_all_pages()
    print("parsed:", len(store))
    save_to_db(store)

