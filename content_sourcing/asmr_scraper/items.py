# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AsmrScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    upload_date = scrapy.Field()
    views = scrapy.Field()
    author = scrapy.Field()
    likes = scrapy.Field()
    dislikes = scrapy.Field()
    comments = scrapy.Field()
    timestamp = scrapy.Field()
    video_link = scrapy.Field()
    video_id = scrapy.Field()
    comments = scrapy.Field()
