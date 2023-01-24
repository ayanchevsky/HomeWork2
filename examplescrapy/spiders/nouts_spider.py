import re

import scrapy
from scrapy.spiders import CrawlSpider, Spider
from examplescrapy.items import NoutsItem


class ComputersSpider(CrawlSpider):
    name = 'nouts'
    allowed_domains = ['laptop.ru']
    start_urls = [f"https://laptop.ru/catalog/noutbuki_planshety/notebooks/?PAGEN_2={x}" for x in range(1, 41)]

    default_headers = {}

    def scrap_nouts(self, response):

        for card in response.xpath("//div[@class='tabloid nowp']"):
            Item = NoutsItem()
            Item['name'] = card.xpath(".//a[@class='name ecLink']/span/text()").extract()[0]
            Item['description'] = card.xpath(".//div[@class='description']/text()").get()
            Item['url'] = card.xpath(".//a[@class='name ecLink']").attrib.get("href")
            item_price = card.xpath(".//a[@class='price getPricesWindow']/text()").extract()
            item_price = item_price[1].replace("\\xa0", "")
            Item['price'] = int("".join(re.findall(r'\d+', item_price)))
            yield Item

    def parse_start_url(self, response, **kwargs):
        urls = self.start_urls
        for url in urls:
            yield response.follow(url, callback=self.scrap_nouts, headers=self.default_headers)
