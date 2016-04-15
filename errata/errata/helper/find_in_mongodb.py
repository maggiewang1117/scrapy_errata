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
                


    def run(self):
        self.find_released_build()


if __name__ == "__main__":
    f = FindData()
    f.run()
