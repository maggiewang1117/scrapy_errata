import scrapy
import pymongo
import time
import re
from scrapy.contrib.spiders import CrawlSpider, Rule
from errata.items import ErrataItem, ExtractItem, GetNodeVersionItem
from errata.helper.sele_helper import get_kerberos_auth_headers
from scrapy.contrib.loader import ItemLoader
from errata.helper.config import url_rhevh7, base_url
from scrapy.utils.url import urljoin_rfc
from errata.settings import MONGO_URI, MONGO_DATABASE
from scrapy.selector import Selector

class RHEVHSpider(CrawlSpider):
    headers = get_kerberos_auth_headers()
    name = "rhevh7"
    allowed_domains = ["redhat.com",
                        "eng.bos.redhat.com"]
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
                else:
                    build_version_list1 = item['build_name'].split("-")
                    build_tag_1 = build_version_list1[-2]
                    build_version_list2 = build_version_list1[-1].split(".")
                    build_version_list3 = ".".join(build_version_list2[:-1])
                    build_verison_url = "http://download.eng.bos.redhat.com/brewroot/packages/rhev-hypervisor7/" +\
                    build_tag_1 + "/" + build_version_list3 + "/data/logs/image/mock_output.log"
                    build_name_trans = item['build_name']
                    request = scrapy.Request(build_verison_url, meta={'item':build_name_trans},callback=self.get_ovirt_node_verison)
                    yield request

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

        ret = [i['build_name'] for i in db['releaseinfo.rhevh7'].find({}, projection=['build_name'])]
        
        cli.close()
        return ret

    def format_date(self, org_date):
        mid_date = time.strptime(org_date, "%a %b %d %H:%M:%S %Z %Y")
        formated_date = time.strftime("%Y-%m-%d", mid_date)
        return formated_date

    def get_ovirt_node_verison(self, response):
        f = open("/home/huiwa/PythonProject/scrapy_errata/errata/errata/result/node_verison.json", "w+")
        item = GetNodeVersionItem()
        f = re.compile("ovirt-node-\d.*\.rpm")
        sel = Selector(response)
        cont1 = sel.xpath('//body').extract()
        item_build_name = response.meta['item']
        item['build_version'] = item_build_name
        if cont1:
            node_version = f.search(cont1[0])

            print "="*20
            node_version = node_version.group()
            item['node_version'] = node_version
            build_verison = response.url
            print item
            print node_version
            print "="*20
        yield item


