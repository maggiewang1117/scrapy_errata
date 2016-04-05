# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ErrataItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    build_name = scrapy.Field()
    tag = scrapy.Field()
    release_date = scrapy.Field()
    links = scrapy.Field()
    advisory = scrapy.Field()
    summary = scrapy.Field()
    text = scrapy.Field()
    a_text = scrapy.Field()

class ExtractItem(scrapy.Item):
    build_name = scrapy.Field()



class DmozItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    desc = scrapy.Field()


class CsdnblogItem(scrapy.Item):
    article_name = scrapy.Field()
    article_url = scrapy.Field()

class BuildItem(scrapy.Item):
    rhevh_name = scrapy.Field()
    ovirt_node_name = scrapy.Field()
    release_name = scrapy.Field()
    rhevm_appliance_name = scrapy.Field()