import os

from dotenv import load_dotenv
from scrapy.http.request import Request
from scrapy.spiders import CrawlSpider
from scrapy_selenium.http import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from ..items import AsmrScraperItem
from ..utils import count_elements

# load_dotenv(dotenv_path=Path(".").absolute().parent)
load_dotenv()


class ContentCrawlerSpider(CrawlSpider):
    name = 'content_crawler'
    allowed_domains = ['youtube.com']
    start_urls = [
        "https://www.youtube.com/c/GibiASMR/videos",
        "https://www.youtube.com/c/FrivolousFoxASMR/videos",
        "https://www.youtube.com/c/RoseASMR/videos",
        "https://www.youtube.com/c/ASMRGlow/videos",
        "https://www.youtube.com/channel/UClMJgjg2z_IrRm6J9KrhcuQ/videos",
    ]

    # rules = (
    #     Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    # )

    def start_requests(self):
        scroll_script = self.get_scroll_script()
        min_elements = os.getenv("MIN_ELEMENTS")

        for url in self.start_urls:
            yield SeleniumRequest(
                url=url,
                script=scroll_script,
                wait_time=30,
                wait_until=count_elements(
                    (By.XPATH, '//*[@id="video-title"]'),
                    min_elements
                    ),
                callback=self.extract_video_links
                )

    def extract_video_links(self, response):
        links = response.selector.xpath(
            '//*[@id="video-title"]//@href'
            ).extract()

        for link in links:
            yield SeleniumRequest(
                url="https://www.youtube.com" + link,
                callback=self.get_video_info,
                wait_time=10,
                script="scrollBy(0, 10000)",
                wait_until=EC.visibility_of_any_elements_located(
                    (By.XPATH, '//*[@id="count"]/yt-formatted-string')
                    )
                )

    def get_video_info(self, response):
        item = AsmrScraperItem()

        item["title"] = response.selector.xpath('//*[@id="container"]/h1/yt-formatted-string/text()').extract_first()
        item["upload_date"] = response.selector.xpath('//*[@id="date"]/yt-formatted-string/text()').extract_first()
        item["views"] = response.selector.xpath('//*[@id="count"]/yt-view-count-renderer/span[1]/text()').extract_first()
        item["author"] = response.selector.xpath('//*[@id="text"]/a/text()').extract_first()
        item["likes"] = response.selector.css("yt-formatted-string::attr(aria-label)").extract()[0]
        item["dislikes"] = response.selector.css("yt-formatted-string::attr(aria-label)").extract()[1]
        item["comments"] = response.selector.xpath('//*[@id="count"]/yt-formatted-string/text()').extract_first()

        yield item

    def get_scroll_script(self):
        js_script = """
        async function scroller() {
            for (i=0; i<=SCROLL_DEPTH; i++) {
                window.scrollBy(0, 10000)
                await new Promise(r => setTimeout(r, 3000));
            }
        }

        scroller()
        """.replace("SCROLL_DEPTH", os.getenv('SCROLL_DEPTH'))

        return js_script
