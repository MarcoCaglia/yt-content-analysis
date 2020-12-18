import scrapy
from scrapy.http import request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class AsmrCrawlerSpider(scrapy.Spider):
    name = "asmr_crawler"
    allowed_domains = ["youtube.com"]
    start_urls = [
        "https://www.youtube.com/c/GibiASMR/videos",
        "https://www.youtube.com/c/FrivolousFoxASMR/videos",
        "https://www.youtube.com/c/RoseASMR/videos",
        "https://www.youtube.com/c/ASMRGlow/videos",
        "https://www.youtube.com/channel/UClMJgjg2z_IrRm6J9KrhcuQ/videos",
    ]

    def parse(self, response):
        reqs = SeleniumRequest(
            url=response.url,
            script="scrollBy(0, 10000)",
            wait_time=10,
            callback=self.get_all_links,
        )
        yield reqs

    def get_all_links(self, response):
        video_objects = response.meta["driver"].find_elements_by_xpath(
            '//*[@id="video-title"]'
        )
        links = [obj.get_attribute("title") for obj in video_objects]
        return {"links": links}
