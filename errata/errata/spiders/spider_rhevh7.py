import scrapy
import pymongo
import time
from scrapy.contrib.spiders import CrawlSpider, Rule
from errata.items import ErrataItem, ExtractItem
from errata.helper.sele_helper import get_kerberos_auth_headers
from scrapy.contrib.loader import ItemLoader
from errata.helper.config import url_rhevh7, base_url
from scrapy.utils.url import urljoin_rfc
from errata.settings import MONGO_URI, MONGO_DATABASE

class RHEVHSpider(CrawlSpider):
    headers = get_kerberos_auth_headers()
    name = "rhevh7"
    allowed_domains = ["redhat.com"]
    start_urls = [url_rhevh7]

    rules = (

        )

    def make_requests_from_url(self, url):
        return scrapy.Request(url, headers=RHEVHSpider.headers,
                              callback=self.parse_item)

    def parse_item(self, response):
        item = ErrataItem()
        base_url = "https://errata.devel.redhat.com"

        for td in response.xpath('//tr'):
            a = td.xpath('td')
            # list_text = a.xpath('a/text()').extract()
            if a.xpath('a/text()').re(r'^RH.*'):
                item['advisory'] = a.xpath('a/text()').re(r'^RH.*')[0]
            else:
                continue
            if a.xpath('a/text()').re(r'rhev.*'):
                item['build_name'] = a.xpath('a/text()').re(r'rhev.*')[0]
                if item['build_name'] in self.get_all_verions_from_db():
                    return
            if a.xpath('text()').re(r'RH.*'):
                item['tag'] = a.xpath('text()').re(r'RH.*')[-1]
            
            summary = a.xpath('text()').extract()
            if len(summary) != 0:
                item['summary'] = summary[2]
            # item['text'] = a.xpath('text()').extract()
            # item['a_text'] = a.xpath('a/text()').extract()
            if a.xpath('@title').extract():
                org_date = a.xpath('@title').extract()[0]
                item['release_date'] = self.format_date(org_date)

                # item['release_date'] = a.xpath('@title').extract()[0]
            links = a.xpath('a/@href').re('/advi.*')
            if len(links) != 0:
                item['links'] = urljoin_rfc(base_url, a.xpath('a/@href').re('/advi.*')[0])

            item['ovirt_node_name'] = False
            item['rhevm_appliance'] = False
            yield item
            
    def get_all_verions_from_db(self):
        cli = pymongo.MongoClient(MONGO_URI)
        db = cli[MONGO_DATABASE]

        ret = [i['build_name'] for i in db['rhevh7'].find({}, projection=['build_name'])]
        
        cli.close()
        return ret

    def format_date(self, org_date):
        mid_date = time.strptime(org_date, "%a %b %d %H:%M:%S %Z %Y")
        formated_date = time.strftime("%Y-%m-%d", mid_date)
        return formated_date

