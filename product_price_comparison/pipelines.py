# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

class RemoveFirstItem:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get('name'):
            if adapter['name'] == 'Shop on eBay':
                raise DropItem(f'First element removed {item}')
            else:
                return item
        else:
            raise DropItem(f'Missing name {item}')

class RemoveNonRelevant:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        search_txt = spider.search
        search_txt = search_txt.replace('+', " ")

        if search_txt not in adapter['name'].lower():
            raise  DropItem(f'Nonrelevant data {item}')
        else:
            return item
