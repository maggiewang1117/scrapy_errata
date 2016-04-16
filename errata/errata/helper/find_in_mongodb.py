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
        rhevh7_list = [i for i in self.db["rhevh7"].find({})]
        return rhevh7_list

    def list_ovirt_node(self):
        ovirt_node_list = [i for i in self.db["buildversion"].find({})]
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
	                    self.db['buildversion'].update(
	                        {"_id": j['_id']}, {"$set": {"released": True, }})

	                    self.db['rhevh7'].update(
	                        {"_id": i["_id"]},
	                        {"$set": {"ovirt_node_name": j["ovirt_node_name"],
	                                   "rhevm_appliance": j['rhevm_appliance_name']}})
	        except KeyError:
	        	pass

    def find_ovirt_node_in_rhevh7(self):
    	node_version_list = [i for i in self.db['rhevh7'].find({'build_version': 
    		{'$regex': ".*"} })]
    	for i in node_version_list:
    		build_version = i['build_version']
    		print i
    		node_version = i['node_version']
    		print build_version
    		buildversion = self.db['rhevh7'].update({'build_name': build_version}, {"$set": {"ovirt_node_name": node_version}})
    		print buildversion
    		         


    def run(self):
        self.find_released_build()
        self.find_ovirt_node_in_rhevh7()


if __name__ == "__main__":
    f = FindData()
    f.run()
