# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import os

import pandas as pd
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from sqlalchemy import create_engine


class AsmrScraperPipeline:
    def process_item(self, item, spider):
        return item


class SqlPipeline:
    def __init__(self, data_path) -> None:
        self.data_path = os.path.abspath(data_path)

        self.con = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            data_path=crawler.settings.get("DATA_PATH")
        )

    def open_spider(self, spider):
        self.con = create_engine("sqlite:///" + self.data_path)

    def process_item(self, item, spider):
        item = dict(item)
        item = {key: [item[key]] for key in item}
        df = pd.DataFrame.from_dict(dict(item))
        df.to_sql(
            "video_info",
            con=self.con,
            index=False,
            if_exists="append"
        )
