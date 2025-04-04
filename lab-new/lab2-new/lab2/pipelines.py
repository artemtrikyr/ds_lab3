from scrapy.exceptions import DropItem
from re import search
import pymongo
import requests

class SaveToAPIPipeline:
    def process_item(self, item, spider):
        response = requests.post("http://localhost:3000/books", json=dict(item))
        if response.status_code != 201:
            spider.logger.error(f"Failed to save item: {response.text}")
        return item


class MongoDBPipeline:
    collection_name = 'books'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'scrapy_db')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        # Уникнення дублікатів за допомогою назви книги (title)
        self.db[self.collection_name].update_one(
            {'title': item.get('title')},  # Фільтр
            {'$set': dict(item)},  # Оновлення або вставка
            upsert=True  # Якщо запис відсутній — створюється новий
        )
        return item


class CleanTitlePipeline:
    def process_item(self, item, spider):
        title = item.get("title")

        # Витягуємо назву за допомогою регулярного виразу (тільки літери та числа)
        res = search(r"[A-Za-z0-9\s\.,'\-]+", title)

        if not res:
            raise DropItem(f"Invalid title: {title}")

        item["title"] = res.group(0).strip()
        return item

class PricePipeline:
    def process_item(self, item, spider):
        price = item.get("price")
        if price:
            # Видаляємо символи та перетворюємо в float
            price = price.replace("£", "").strip()
            try:
                item["price"] = float(price)
            except ValueError:
                raise DropItem(f"Invalid price format: {price}")
        return item
