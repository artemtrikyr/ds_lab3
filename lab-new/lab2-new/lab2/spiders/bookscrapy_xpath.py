import scrapy
from lab2.items import BookItem


class BookscrapyXPathSpider(scrapy.Spider):
    name = "bookscrapy_xpath"
    allowed_domains = ["books.toscrape.com"]
    
    # Автоматично генеруємо список сторінок
    start_urls = [
        f"https://books.toscrape.com/catalogue/page-{page}.html" 
        for page in range(1, 5)
    ]

    def parse(self, response):
        # Знаходимо всі блоки книг
        books = response.xpath('//article[@class="product_pod"]')

        for book in books:
            # назву книги
            title = book.xpath('.//h3/a/@title').get()
            # ціну книги
            price = book.xpath('.//p[@class="price_color"]/text()').get()
            # посилання на сторінку книги
            book_url = response.urljoin(book.xpath('.//h3/a/@href').get())

            # Створюємо об'єкт BookItem
            item = BookItem(
                title=title,
                price=price
            )

            # Повертаємо запит для парсингу сторінки книги
            yield response.follow(
                book_url,
                callback=self.parse_book,
                meta={'item': item}
            )

    def parse_book(self, response):
        item = response.meta["item"]

        # Витягуємо опис (через четвертий тег <p>)
        description = response.xpath('(//article//p)[4]/text()').get()
        item["description"] = description

        image_url = response.xpath('//div[@class="item active"]//img/@src').get()
        if image_url:
            item["image_url"] = response.urljoin(image_url)


        # Повертаємо готовий item
        yield item
