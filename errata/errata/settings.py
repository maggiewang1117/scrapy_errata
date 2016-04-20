# -*- coding: utf-8 -*-

# Scrapy settings for errata project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'errata'

SPIDER_MODULES = ['errata.spiders']
NEWSPIDER_MODULE = 'errata.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'errata (+http://www.yourdomain.com)'
_MONGOURI_TEST = 'mongodb://127.0.0.1:3001'
_MONGOURI_PROD = 'mongodb://meteor:redhat@10.66.10.22/meteordb?authMechanism=SCRAM-SHA-1'
MONGO_URI = _MONGOURI_PROD

MONGO_DATABASE = 'meteordb'


COOKIES_ENABLED = False

ITEM_PIPELINES = {
    # 'errata.pipelines.CsdnblogPipeline': 300,
    # 'errata.pipelines.ErrataPipeline': 300,
    'errata.pipelines.BuildPipeline': 300,
    # 'errata.pipelines.OvirtNodeNg36Pipeline': 300,
}


SPIDER_NAME_COLLECTION = {
	'build': 'releaseinfo.buildversion',
	'rhevh7': 'releaseinfo.rhevh7',
}

SPIDER_MAP = {
	'build': 'BuildSpider',
	'rhevh7': 'RHEVHSpider',
}