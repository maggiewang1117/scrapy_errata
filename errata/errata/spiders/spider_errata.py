import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from errata.items import ErrataItem, ExtractItem
from errata.helper.sele_helper import get_kerberos_auth_headers
from scrapy.contrib.loader import ItemLoader
from errata.helper.config import url, base_url

class ErrataSpider(CrawlSpider):
    headers = get_kerberos_auth_headers()
    name = "scrapy_errata"
    allowed_domains = ["redhat.com"]
    start_urls = [url]

    rules = (

        )

    def make_requests_from_url(self, url):
        return scrapy.Request(url, headers=ErrataSpider.headers,
                              callback=self.parse_item)

    def parse_item(self, response):
        item = ErrataItem()
        # base_url = "https://errata.devel.redhat.com"

        for td in response.xpath('//tr'):
            a = td.xpath('td')
            # list_text = a.xpath('a/text()').extract()
            item['advisory'] = a.xpath('a/text()').re(r'^RHBA-.*')
            item['build_name'] = a.xpath('a/text()').re(r'ovirt.*')
            item['tag'] = a.xpath('text()').re(r'RH.*')
            item['summary'] = a.xpath('text()').re('.*bug.*')
            # item['text'] = a.xpath('text()').extract()
            # item['a_text'] = a.xpath('a/text()').extract()
            item['release_date'] = a.xpath('@title').extract()
            links = a.xpath('a/@href').re('/advi.*')
            if len(links) != 0:
                item['links'] = base_url + a.xpath('a/@href').re('/advi.*')[0]
            yield item
            
