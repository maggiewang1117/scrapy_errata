import scrapy
import json
import pymongo
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.selector import Selector
from errata.items import BuildItem
from errata.settings import MONGO_URI, MONGO_DATABASE

class BuildSpider(CrawlSpider):
    name = "build"
    allowed_domains = ['tlv.redhat.com']

    start_urls = ["http://bob.eng.lab.tlv.redhat.com/builds/3.6"]

    rules = [
        Rule(LxmlLinkExtractor(allow=(r'/\d.*'),
                               restrict_xpaths=('//a')),
                                callback='parse_el7_link')
    ]

    def __init__(self, *args, **kwargs):
        super(BuildSpider, self).__init__(*args, **kwargs)

    def parse_el7_link(self, response):
        sel = Selector(response)
        el7_url = sel.xpath('//a/@href').re('el7/')
        if len(el7_url) != 0:
            el7_url = response.url + el7_url[0]
            request = scrapy.Request(el7_url, callback=self.parse_html_link)
            yield request

    def parse_html_link(self, response):
        sel = Selector(response)
        version_link = sel.xpath('//a/@href').re('\d.*\d_version_info.html')
        if len(version_link) != 0:
            version_link = response.url + version_link[0]

            request = scrapy.Request(version_link, callback=self.parse_build_info)
            yield request

    def parse_build_info(self, response):
        item = BuildItem()
        sel = Selector(response)
        item['release_name'] = sel.xpath('//tr/th/text()').re('\d+.*')[-1]
        if item['release_name'] in self.get_all_verions_from_db():
            return
        else:
            td_list = sel.xpath('//td')
            td_list_new = []
            for i in td_list:
                if i.xpath('text()').extract():
                    if i.xpath('text()').extract()[0]:
                        td_list_new.append(i.xpath('text()').extract()[0])
                elif i.xpath('font/text()'):
                    td_list_new.append(i.xpath('font/text()').extract()[0])
            
            item['ovirt_node_name'] = self.find_package(td_list_new, 'ovirt-node')
            item['rhevh_name'] = self.find_package(td_list_new, 'rhev-hypervisor7')
            item['rhevm_appliance_name'] = self.find_package(td_list_new, 'rhevm-appliance')
        
        yield item

    def find_package(self, package_dict, package_name):

        if package_name in package_dict:
            list_index = package_dict.index(package_name)
            key_name = package_dict[list_index+2]
            if key_name != "N/A":
                return package_dict[list_index+2]
            else:
                return False
        else:
            return False

    def get_all_verions_from_db(self):
        cli = pymongo.MongoClient(MONGO_URI)
        db = cli[MONGO_DATABASE]

        ret = [i['release_name'] for i in db['buildversion'].find({}, projection=['release_name'])]
        cli.close()
        print ret
        return ret


