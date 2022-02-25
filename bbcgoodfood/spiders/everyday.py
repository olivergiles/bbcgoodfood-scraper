import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re

class Recipe(scrapy.Item):
    title = scrapy.Field()
    prep = scrapy.Field()
    cook = scrapy.Field()
    desc = scrapy.Field()
    diff = scrapy.Field()
    serves = scrapy.Field()
    ingredients = scrapy.Field()

class BBCGoodSpider(CrawlSpider):
    name = 'everyday'
    start_urls = [
    f'https://www.bbcgoodfood.com/search/recipes/page/{p}/?q=everyday&sort=-relevance' 
    for p in range(1,14,1)
    ]
    allowed_domains = ['www.bbcgoodfood.com']
    rec_links = LinkExtractor(allow=r'/recipes/',
            deny=(r'/recipes/collection/', r'/recipes/category/'))
    all_links = LinkExtractor(allow=r'/recipes/')

    rules = [
        Rule(
            rec_links,
            callback='parse_item',
            follow=True
            ),
        Rule(
            all_links,
            callback='parse',
            follow=True
            )
    ]

    def parse_item(self, response):
        item = Recipe()
        item['title'] = response.xpath("/html/body/div/div[3]/main/div/section/div/div[3]/div[1]/h1/text()").extract_first()
        item['prep'] = response.xpath("/html/body/div/div[3]/main/div/section/div/div[3]/ul[1]/li[1]/div/div[2]/ul/li[1]/span[2]/time/text()").extract_first()
        item['cook'] = response.xpath("/html/body/div/div[3]/main/div/section/div/div[3]/ul[1]/li[1]/div/div[2]/ul/li[2]/span[2]/time/text()").extract_first()
        item['desc'] = response.xpath("/html/body/div/div[3]/main/div/section/div/div[3]/div[4]/div/p/text()").extract_first()
        item['diff'] = response.xpath("/html/body/div/div[3]/main/div/section/div/div[3]/ul[1]/li[2]/div/div[2]/text()").extract_first()
        item['serves'] = response.xpath("/html/body/div/div[3]/main/div/section/div/div[3]/ul[1]/li[3]/div/div[2]/text()").extract_first()
        item['ingredients'] = " ".join(response.xpath("/html/body/div/div[3]/main/div/div/div[1]/div[1]/div[2]/div[2]/div/section[1]/section/ul/li/text()").extract())
        return item
