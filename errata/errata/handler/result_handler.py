import json

class ResultHandler(object):
	def __init__(self, fileName):
		self.fileName = fileName
		self.itemList = []

	def getItems(self):
		with open(self.fileName,"r") as f:
			self.itemList = json.load(f)

	def generateHTMLHead(self):
		self.str1 = '''<html>
		<head>
		<meta charset="UTF-8">
		<title>RHEVH Verison List</title>
		</head>
		'''
		self.str2 = "</html>"
		self.str3 = """<table>
		<th>Build_name</th>
        <th>Tag_Name</th>
        <th>Release_date</th>
        """

	def generateHTMLBody(self):
		for item in self.itemList:
			for k,v in item:
				print k, v

	def run(self):
		self.getItems()


r1 = ResultHandler("../result/rhevh1.json")
r1.run()