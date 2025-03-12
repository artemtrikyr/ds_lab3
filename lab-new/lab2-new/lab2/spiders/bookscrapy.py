import scrapy
from bs4 import BeautifulSoup
from lab2.items import BookItem


class BookscrapySpider(scrapy.Spider):
    name = "bookscrapy"
    allowed_domains = ["books.toscrape.com"]
    start_urls = [
        f"https://books.toscrape.com/catalogue/page-{page}.html" 
        for page in range(1, 5) # Парсимо перші 5 сторінок
    ]


    def parse(self, response):
        soup = BeautifulSoup(response.body, "html.parser")

        # Знаходимо всі блоки книг на сторінці
        books = soup.find_all("article", class_="product_pod")
        for book in books:
            h3_tag = book.find("h3")
            a_tag = h3_tag.find("a")
            title = a_tag.get("title") 
            price = book.find("p", class_="price_color").get_text(strip=True)
            book_url = response.urljoin(a_tag["href"])

            # Створюємо об'єкт BookItem
            item = BookItem(
                title=title,
                price=price
            )

            # Повертаємо запит для парсингу сторінки книги
            yield scrapy.Request(
                url=book_url,
                callback=self.parse_book,
                meta={"item": item}
            )

    def parse_book(self, response):
        soup = BeautifulSoup(response.body, "html.parser")

        # Отримуємо переданий item із мета-даних
        item = response.meta["item"]

        # Витягуємо посилання на зображення
        img_tag = soup.find("img", class_="thumbnail")
        if img_tag:
            item["image_url"] = response.urljoin(img_tag["src"])
        else:
            item["image_url"] = "Фото відсутнє"
        # Витягуємо опис через четвертий тег <p>
        description_tags = soup.find_all("p")
        if len(description_tags) > 3:
            item["description"] = description_tags[3].get_text(strip=True)
        else:
            item["description"] = "Опис відсутній"


        # Повертаємо готовий item
        yield item
