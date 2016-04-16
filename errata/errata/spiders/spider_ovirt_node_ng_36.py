from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.selector import Selector
from errata.items import OvirtNg36Item
from errata.helper.config import ovirt_node_ng_36_url
import scrapy
import re


class OvirtNodeNg36Item(CrawlSpider):
    name = "ovirtnodeng36"
    allowed_domains = ['ovirt.org']
    start_urls = [ovirt_node_ng_36_url]

    rules = [
        # Rule(LxmlLinkExtractor(restrict_xpaths=('//a')),
        #      callback='parse_node_ng_36')
    ]

    # def __init__(self):
    #     str_image_update = r".*ovirt-node-ng-image-update.*"
    #     str_manifest = r".*manifest.*"
    #     str_squashfs = r".*squashfs.*"
    #     str_installer = r".*ovirt-node-ng-installer.*"
    #     str_tools = r".*ovirt-node-ng-tools.*"

    def make_requests_from_url(self, url):
        return scrapy.Request(url, callback=self.parse_item)

    def parse_item(self, response):
        base_url = response.url
        print "=" * 20
        print base_url
        print "=" * 20

        str_image_update = ".*ovirt-node-ng-image-update.*"
        str_manifest = r".*manifest.*"
        str_squashfs = r".*squashfs.*"
        str_installer = r".*ovirt-node-ng-installer.*"
        str_tools = r".*ovirt-node-ng-tools.*"
        sel = Selector(response)
        item = OvirtNg36Item()

        print sel.xpath('//a')

        for i in sel.xpath('//a'):
            if len(i.xpath('text()').re(str_image_update)) != 0:
                item['ngn_image_update'] = base_url + i.xpath('@href').extract()[0]
                tag_min = i.xpath('text()').extract()[0]
                tag_list = tag_min.split("-")
                tag_list.append('36')
                item['ngn_tag'] = "-".join(tag_list[-2:])
            elif len(i.xpath('text()').re(str_manifest)) != 0:
                item['ngn_manifest_rpm'] = base_url + i.xpath('@href').extract()[0]
            elif len(i.xpath('text()').re(str_squashfs)) != 0:
            	item['ngn_squash_fs'] = base_url + i.xpath('@href').extract()[0]
            elif len(i.xpath('text()').re(str_installer)) != 0:
            	item['ngn_installer_name'] = base_url + i.xpath('@href').extract()[0]
            elif len(i.xpath('text()').re(str_tools)) != 0:
            	item['ngn_tools_name'] = base_url + i.xpath('@href').extract()[0]
           	yield item
