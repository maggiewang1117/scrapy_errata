#!/usr/bin/python

import pymongo
import url

class AddOvirtNodeVerion(object):
	def __init__(self, mongo_uri, mongo_database):
		self.cli = pymongo.MongoClient(mongo_uri)
		self.db = self.cli[mongo_database]

	def add_ovirt_node(self):


if __name__ == "__main__":
	version_dict = {"rhev-hypervisor7-7.2-20160219.0.el7ev": "ovirt-node-3.2.3-31.el7.noarch.rpm",
	"rhev-hypervisor7-7.2-20160105.2.el7ev": "ovirt-node-3.2.3-30.el7.noarch.rpm",
	"rhev-hypervisor7-7.2-20160105.1.el7ev": "ovirt-node-3.2.3-30.el7.noarch.rpm",
	"rhev-hypervisor7-7.2-20151129.1.el7ev": "",
	"rhev-hypervisor7-7.1-20151015.0.el7ev": "",
	"rhev-hypervisor7-7.1-20150911.0.el7ev": "",
	"rhev-hypervisor7-7.1-20150827.1.el7ev": "",
	"rhev-hypervisor7-7.1-20150603.0.el7ev": "",
	"rhev-hypervisor7-7.1-20150512.1.el7ev": "",
	"rhev-hypervisor7-7.1-20150505.0.el7ev": "",
	"rhev-hypervisor7-7.1-20150420.0.el7ev": "",
	}
