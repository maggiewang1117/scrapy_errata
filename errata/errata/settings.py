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

COOKIES_ENABLED = False

ITEM_PIPELINES = {
    # 'errata.pipelines.CsdnblogPipeline': 300,
    # 'errata.pipelines.ErrataPipeline': 300,
    'errata.pipelines.BuildPipeline': 300
}
