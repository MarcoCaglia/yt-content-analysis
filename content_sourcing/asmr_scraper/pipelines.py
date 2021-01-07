# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import logging
from pathlib import Path

import pandas as pd
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from sqlalchemy import create_engine


class AsmrScraperPipeline:
    def process_item(self, item, spider):
        return item


class SqlPipeline:

    VIDEO_INFO_FILEDS = [
        "title", "upload_date", "views", "author", "likes", "dislikes",
        "comments", "timestamp", "video_url", "video_id", "project_tag"
        ]
    COMMENTS_FIELDS = ["video_id", "comments"]
    VIDEO_TABLE_NAME = "video_info"
    COMMENTS_TABLE_NAME = "comments"

    def __init__(self, data_path) -> None:
        self.data_path = Path(data_path).as_posix()

        self.con = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            data_path=crawler.settings.get("DATA_PATH")
        )

    def open_spider(self, spider):
        logging.info(f"Writing Data to DB: {self.data_path}")
        self.con = create_engine("sqlite:///" + self.data_path)

    def process_item(self, item, spider):
        # Split item into video information and comments
        video_info, comments = self._split_item(item)

        # Construct list of tuples with (table_names table)
        upload_data = [
            (SqlPipeline.VIDEO_TABLE_NAME, video_info),
            (SqlPipeline.COMMENTS_TABLE_NAME, comments)
        ]

        # Iterate over constructed list and upload second element of tuple
        # (table) and name the uploaded table with the first element of the
        # table (name).
        for name, table in upload_data:
            table.to_sql(
                name,
                con=self.con,
                index=False,
                if_exists="append"
            )

    def _split_item(self, item):
        # Split items in video info fields and comments fields.
        # Bot tables can be connected via video_id.
        video_info = {
            key: [item[key]] for key in SqlPipeline.VIDEO_INFO_FILEDS
            }
        comments = {key: item[key] for key in SqlPipeline.COMMENTS_FIELDS}

        # Convert both dictionaries to dataframes
        video_info = pd.DataFrame.from_dict(dict(video_info))
        comments = pd.DataFrame.from_dict(dict(comments))

        # Return both tables
        return video_info, comments
