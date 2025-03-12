from requests import get
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/catalogue"
URL = f"{BASE_URL}/category/books/mystery_3/index.html"
HEADERS = {
    "user_agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}
FILE_NAME = "books.txt"
with open(FILE_NAME, "w", encoding="utf-8") as file:
    page = get(URL, headers=HEADERS)
    soup = BeautifulSoup(page.content,  "html.parser")
    books = soup.find_all("article", class_="product_pod")
    #для кожного дочірнього елемента
    for book in books:
        #ціна книжки
        price = book.find("p", class_=("price_color")).get_text(strip=True)
        #назва книги
        title = book.h3.a["title"]
        #посилання на сторінку книги
        url_book = BASE_URL + book.find("a")["href"].replace("../../../", "/")

        


        book_page = get(url_book, headers=HEADERS)
        soup = BeautifulSoup(book_page.content, "html.parser")

        # Опис книги (другий тег <p> у <article>)
        article = soup.find("article", class_="product_page")
        if article:
            description_tags = article.find_all("p")
            if len(description_tags) >= 4:
                description = description_tags[3].get_text(strip=True)
        #посилання на img
        img_tag = article.find("img", class_="thumbnail")
        book_img_url = BASE_URL + img_tag["src"].replace("../../", "/")
        file.write(f"посилання на фото - {book_img_url}")
        file.write(f"      опис - {description}")
        file.write(10 * "-")
