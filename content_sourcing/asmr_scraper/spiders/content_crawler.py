"""Spider for Youtube stats scraping."""

import hashlib
import logging
import os
from datetime import datetime as dt
from pathlib import Path

import yaml
from dotenv import load_dotenv
from scrapy.spiders import CrawlSpider
from scrapy_selenium.http import SeleniumRequest
from selenium.webdriver.common.by import By

from ..items import AsmrScraperItem
from ..utils import count_elements

load_dotenv()


class ContentCrawlerSpider(CrawlSpider):

    # Setting custom class variables
    PROJECTS_PATH = Path(__file__).absolute().parent.parent.parent.parent \
        .joinpath("properties").joinpath("projects.yml")

    # Set maximum number of seconds to wait for each request
    # (Roughly equivalent to Selenium's implicit wait, but suitable for
    # scraping)
    MAX_WAIT_ON_REQUEST = int(os.getenv("MAX_WAIT_ON_REQUEST"))

    name = 'content_crawler'
    allowed_domains = ['youtube.com']
    with PROJECTS_PATH.open("r") as f:
        start_urls = yaml.safe_load(f)[os.getenv("PROJECT_TAG")]

    def start_requests(self):
        scroll_script = self.get_scroll_script(
            scroll_depth=os.getenv("SCROLL_DEPTH"),
            wait_time=os.getenv("MAX_WAIT_ON_SCROLL")
        )

        for url in self.start_urls:
            yield SeleniumRequest(
                url=url,
                script=scroll_script,
                wait_time=ContentCrawlerSpider.MAX_WAIT_ON_REQUEST,
                wait_until=count_elements(
                    (By.XPATH, '//*[@id="video-title"]'),
                    count=os.getenv("MIN_ELEMENTS")
                    ),
                callback=self.extract_video_links,
                move_on=True
                )

    def extract_video_links(self, response):
        links = response.selector.xpath(
            '//*[@id="video-title"]//@href'
            ).extract()

        logging.info(f"Found {len(links)} links from {response.url}...")

        scroll_script = self.get_scroll_script(
            scroll_depth=os.getenv("SCROLL_DEPTH"),
            wait_time=os.getenv("MAX_WAIT_ON_SCROLL")
        )

        for link in links:
            yield SeleniumRequest(
                url="https://www.youtube.com" + link,
                callback=self.get_video_info,
                wait_time=ContentCrawlerSpider.MAX_WAIT_ON_REQUEST,
                script=scroll_script,
                wait_until=count_elements(
                    (By.XPATH, '//*[@id="content-text"]'),
                    200
                    ),
                move_on=True
                )

    def get_video_info(self, response):
        item = AsmrScraperItem()

        video_title = response.selector.xpath('//*[@id="container"]/h1/yt-formatted-string/text()').extract_first()
        item["title"] = video_title
        item["upload_date"] = response.selector.xpath('//*[@id="date"]/yt-formatted-string/text()').extract_first()
        item["views"] = response.selector.xpath('//*[@id="count"]/yt-view-count-renderer/span[1]/text()').extract_first()
        item["author"] = response.selector.xpath('//*[@id="text"]/a/text()').extract_first()
        item["likes"] = response.selector.css("yt-formatted-string::attr(aria-label)").extract()[0]
        item["dislikes"] = response.selector.css("yt-formatted-string::attr(aria-label)").extract()[1]
        item["comments_nr"] = response.selector.xpath('//*[@id="count"]/yt-formatted-string/text()').extract_first()
        item["timestamp"] = dt.now()
        item["video_url"] = response.url
        item["project_tag"] = os.getenv("PROJECT_TAG")
        item["video_id"] = hashlib.sha256(video_title.encode("utf-8")).hexdigest()
        item["comments"] = response.selector.xpath('//*[@id="content-text"]/text()').extract()

        yield item

    def get_scroll_script(self, scroll_depth=10, wait_time=5):
        wait_time = str(float(wait_time) * 10 ** 3)
        js_script = f"""
        async function scroller() {{
            for (i=0; i<={scroll_depth}; i++) {{
                window.scrollBy(0, 10000)
                await new Promise(r => setTimeout(r, {wait_time}));
            }}
        }}

        scroller()
        """

        return js_script
