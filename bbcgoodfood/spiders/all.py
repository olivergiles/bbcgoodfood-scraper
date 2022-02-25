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
    rating = scrapy.Field()
    popularity = scrapy.Field()
    engagement = scrapy.Field()
    url = scrapy.Field()

class BBCGoodSpider(CrawlSpider):
    name = 'all'
    start_urls = [
        'https://www.bbcgoodfood.com/recipes',
        'https://www.bbcgoodfood.com/'
    ]
    allowed_domains = ['www.bbcgoodfood.com']
    rec_links = LinkExtractor(allow=r'/recipes/',
            deny=(r'/collection/', r'/category/'))
    all_links = LinkExtractor(allow=r'/recipes/')

    rules = [
        Rule(
            rec_links,
            callback='parse_item',
            follow=True
            ),
        Rule(
            all_links,
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
        item['rating'] = response.xpath("/html/body/div/div[3]/main/div/section/div/div[3]/div[3]/div/a[1]/div/div/span[1]/text()").extract_first()
        item['popularity'] = response.xpath("/html/body/div/div[3]/main/div/section/div/div[3]/div[3]/div/a[1]/div/div/span[2]/text()").extract_first()
        item['url'] = response
        return item
