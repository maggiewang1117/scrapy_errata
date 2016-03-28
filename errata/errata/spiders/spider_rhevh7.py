import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from errata.items import ErrataItem, ExtractItem
from errata.helper.sele_helper import get_kerberos_auth_headers
from scrapy.contrib.loader import ItemLoader
from errata.helper.config import url_rhevh7, base_url
from scrapy.utils.url import urljoin_rfc

class RHEVHSpider(CrawlSpider):
    headers = get_kerberos_auth_headers()
    name = "scrapy_rhevh"
    allowed_domains = ["redhat.com"]
    start_urls = [url_rhevh7]

    rules = (

        )

    def make_requests_from_url(self, url):
        return scrapy.Request(url, headers=RHEVHSpider.headers,
                              callback=self.parse_item)

    def parse_item(self, response):
        self.log("First try!")
        item = ErrataItem()
        base_url = "https://errata.devel.redhat.com"

        for td in response.xpath('//tr'):
            a = td.xpath('td')
            # list_text = a.xpath('a/text()').extract()
            item['advisory'] = a.xpath('a/text()').re(r'^RH.*')
            item['build_name'] = a.xpath('a/text()').re(r'rhev.*')
            item['tag'] = a.xpath('text()').re(r'RH.*')
            
            summary = a.xpath('text()').extract()
            if len(summary) != 0:
                item['summary'] = summary[2]
            # item['text'] = a.xpath('text()').extract()
            # item['a_text'] = a.xpath('a/text()').extract()
            item['release_date'] = a.xpath('@title').extract()
            links = a.xpath('a/@href').re('/advi.*')
            if len(links) != 0:
                item['links'] = urljoin_rfc(base_url, a.xpath('a/@href').re('/advi.*')[0])
            yield item
            # item['links'] = links[0]
            # yield item
            # ext_item = ExtractItem()
            # ext_item['build_name'] = item.get('text')
            # print list_text

            # item['advisory'] = a.xpath('a/text()').extract(0)
            # item['advisory'] = list_text[0]
            # item['build_name'] = list_text[1]
            # print a.xpath('text()').extract()
            # print a.xpath('text()').extract()
            # print a.xpath('a/text()').extract()
            # print a.xpath('text()').extract()
            # print a.xpath('@title').extract()
                # item['advisory'] = i.xpath('td/text()').extract()
                # item['tag'] = i.xpath('td').extract()
                # item['release_date'] = i.xpath('td/@title').extract()
                # item['build_name'] = i.xpath('td/text()').extract()
                # item['summary'] = i.xpath('td/text()').extract()
                # yield item


        # for sel in response.xpath('//tr/td'):
        #     item = ErrataItem()
        #     item['tag'] = sel.xpath('a/@title').extract()
        #     item['link'] = sel.xpath().extract()
        #     item['desc'] = sel.xpath('text()').extract()
        #     yield item
        # item = ErrataItem()
        # l1 = response.xpath('//tr')
        # self.log(l1)
