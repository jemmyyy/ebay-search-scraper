import scrapy
from product_price_comparison.items import Product
from product_price_comparison.itemloaders import ProductLoader


class EbayscraperSpider(scrapy.Spider):
    name = "ebayscraper"
    allowed_domains = ["ebay.com"]
    
    def __init__(self, search=None, no_pages='5', start_page =None, *args, **kwargs):
        super(EbayscraperSpider, self).__init__(*args, **kwargs)
        self.search = search
        self.no_pages = int(no_pages)
        self.start_page = int(start_page)
        self.pages_searched = 0
        self.start_urls = [f'https://www.ebay.com/sch/i.html?_from=R40&_nkw={self.search}&_sacat=0&_pgn={self.start_page}&rt=nc']

    def parse(self, response):
        products = response.css('li.s-item')

        for product in products:
            item = ProductLoader(item = Product(), selector = product)
            name = product.css('div.s-item__title')
            item.add_css('name', '[role="heading"]::text')
            item.add_css('price', 'span.s-item__price::text')
            item.add_css('url', 'a.s-item__link::attr(href)')
            
            yield item.load_item()

        self.pages_searched += 1
        if self.pages_searched < self.no_pages:
            yield response.follow(f'https://www.ebay.com/sch/i.html?_from=R40&_nkw={self.search}&_sacat=0&_pgn={self.pages_searched+1}', callback=self.parse)

        