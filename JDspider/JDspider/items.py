# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join


class JdspiderItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    desc = scrapy.Field()
    price = scrapy.Field()
    haoping = scrapy.Field()
    zhongping = scrapy.Field()
    chaping = scrapy.Field()
    shaitu = scrapy.Field()

class JDspiderLoader(ItemLoader):
    default_item_class = JdspiderItem
    default_input_processor = MapCompose(lambda s: s.strip())
    default_output_processor = TakeFirst()
    description_out = Join()
