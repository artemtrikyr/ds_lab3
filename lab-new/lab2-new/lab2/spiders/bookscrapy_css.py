import scrapy
from lab2.items import BookItem


class BookscrapyCssSpider(scrapy.Spider):
    name = "bookscrapy_css"
    allowed_domains = ["books.toscrape.com"]
    
    # Автоматично генеруємо список сторінок
    start_urls = [
        f"https://books.toscrape.com/catalogue/page-{page}.html"
        for page in range(1, 10)
    ]

    def parse(self, response):
        # Знаходимо всі блоки книг через CSS
        books = response.css('article.product_pod')

        for book in books:
            # назву книги
            title = book.css('h3 a::attr(title)').get()
            # ціну книги
            price = book.css('p.price_color::text').get()
            # посилання на сторінку книги
            book_url = response.urljoin(book.css('h3 a::attr(href)').get())
            image_url = response.urljoin(book.css('img::attr(src)').get())

            # об'єкт BookItem
            item = BookItem(
                title=title,
                price=price,
                image_url=image_url,
                image_urls=[image_url]
            )

            # Повертаємо запит для парсингу сторінки книги
            yield scrapy.Request(
                book_url,
                callback=self.parse_book,
                meta={'item': item}
            )

    def parse_book(self, response):
        item = response.meta["item"]

        # Вибираємо текст параграфа після div#product_description
        description = response.css('#product_description + p::text').get()
        item["description"] = description 

        # Повертаємо готовий item
        yield item

