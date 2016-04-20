#!/usr/bin/python2.7

import pymongo
import re
import sys

sys.path.append("/home/huiwa/PythonProject/scrapy_errata/errata")
from errata.settings import MONGO_URI, MONGO_DATABASE


class FindData(object):

    def __init__(self):
        self.cli = pymongo.MongoClient(MONGO_URI)
        self.db = self.cli[MONGO_DATABASE]

        # self.db = self.cli[MONGO_DATABASE]

    def list_rhevh7(self):
        rhevh7_list = [i for i in self.db["releaseinfo.rhevh7"].find({})]
        return rhevh7_list

    def list_ovirt_node(self):
        ovirt_node_list = [i for i in self.db["releaseinfo.buildversion"].find({})]
        return ovirt_node_list

    def find_released_build(self):
        rhevh7_list_1 = self.list_rhevh7()
        ovirt_node_list_1 = self.list_ovirt_node()

        for i in rhevh7_list_1:
            try:
                res_1 = i["build_name"].split("-")
                build_version = "-".join(res_1[-1:])
                f = re.compile(build_version)
                for j in ovirt_node_list_1:
                    if f.search(str(j['rhevh_name'])):
                        self.db['releaseinfo.buildversion'].update(
                            {"_id": j['_id']}, {"$set": {"released": True, }})

                        self.db['releaseinfo.rhevh7'].update(
                            {"_id": i["_id"]},
                            {"$set": {"ovirt_node_name": j["ovirt_node_name"],
                                      "rhevm_appliance": j['rhevm_appliance_name']}})
            except KeyError:
                pass

    def find_ovirt_node_in_rhevh7(self):
        node_version_list = [i for i in self.db['releaseinfo.rhevh7'].find({'build_version':
                                                                {'$regex': ".*"}})]
        for i in node_version_list:
            build_version = i['build_version']
            print i
            node_version = i['node_version']
            print build_version
            buildversion = self.db['releaseinfo.rhevh7'].update(
                {'build_name': build_version}, {"$set": {"ovirt_node_name": node_version}})
            print buildversion

    def insert_ovirt_node_manually(self):
        version_dict = {
            "rhev-hypervisor7-7.2-20160105.1.el7ev": "ovirt-node-3.2.3-30.el7.noarch",
            "rhev-hypervisor7-7.2-20151129.1.el7ev": "ovirt-node-3.2.3-29.el7.noarch",
            "rhev-hypervisor7-7.1-20151015.0.el7ev": "ovirt-node-3.2.3-23.el7.noarch",
            "rhev-hypervisor7-7.1-20150911.0.el7ev": "ovirt-node-3.2.3-20.el7.noarch",
            "rhev-hypervisor7-7.1-20150827.1.el7ev": "ovirt-node-3.2.3-20.el7.noarch",
            "rhev-hypervisor7-7.1-20150603.0.el7ev": "ovirt-node-3.2.3-3.el7.noarch",
            "rhev-hypervisor7-7.1-20150512.1.el7ev": "ovirt-node-3.2.2-3.el7.noarch",
            "rhev-hypervisor7-7.1-20150505.0.el7ev": "ovirt-node-3.2.2-3.el7.noarch",
            "rhev-hypervisor7-7.1-20150420.0.el7ev": "ovirt-node-3.2.2-3.el7.noarch",
        }

        for k, v in version_dict.items():
        	print k
        	print v
        	buildversion = self.db['releaseinfo.rhevh7'].update(
            	{'build_name': k}, {"$set": {"ovirt_node_name": v}})

    def run(self):
        self.find_released_build()
        self.find_ovirt_node_in_rhevh7()
        self.insert_ovirt_node_manually()


if __name__ == "__main__":
    f = FindData()
    f.run()
