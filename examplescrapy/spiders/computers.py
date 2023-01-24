import scrapy
from scrapy.spiders import CrawlSpider, Spider
import re
from examplescrapy.items import NoutsItem


class ComputersSpider(CrawlSpider):
    name = 'computers'
    allowed_domains = ['notik.ru']
    start_urls = ["https://www.notik.ru/search_catalog/filter/work.htm",
                  "https://www.notik.ru/search_catalog/filter/work.htm?page=2"]

    default_headers = {}

    def scrap_computers(self, response):

        for card in response.xpath("//tr[@class='goods-list-table']"):
            Item = NoutsItem()
            price_selector = card.xpath(".//td[@class='glt-cell gltc-cart']")
            price = re.findall(r'\d+', price_selector.xpath(".//b").css("::text").get())
            Item['price'] = int("".join(price))
            Item['name'] = price_selector.xpath(".//a").attrib.get("ecname")
            description = card.xpath(".//td[@class='glt-cell w4']//text()").extract()
            Item['description'] = " ".join(x for x in description).replace("\r", "").replace("  ", " ").replace("ГБ", "Gb")
            Item['url'] = card.xpath(".//a").attrib.get("href")

            yield Item

    def parse_start_url(self, response, **kwargs):
        urls = self.start_urls
        for url in urls:
            yield response.follow(url, callback=self.scrap_computers, headers=self.default_headers)

