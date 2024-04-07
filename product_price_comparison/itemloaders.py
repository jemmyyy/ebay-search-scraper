from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose

def remove_quotes(str):
    return str.replace('"', '')

def remove_stars(str):
    return str.replace('*', '')

class ProductLoader(ItemLoader):

    default_output_processor = TakeFirst()

    name_in = MapCompose(remove_quotes, remove_stars)