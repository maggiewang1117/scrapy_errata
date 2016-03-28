import json
import time

class ResultHandler(object):
    def __init__(self, fileName):
        self.fileName = fileName
        self.itemList = []

    def getItems(self):
        with open(self.fileName,"r") as f:
            self.itemList = json.load(f)

    def merge_item_lists(self):
        merge_item_lists = self.itemList[1:]
        for k in self.itemList[1:]:
            # print "*"*20
            # print k
            for k2 in merge_item_lists:
                # print "="*20
                # print k2
                if k["tag"] == k2['tag'] and k['build_name'] != k2['build_name']:
                    k2['build_name'].append(k['build_name'][0])
                    print merge_item_lists
        # print merge_item_lists

    def release_date_transfer(self, release_date):
        if release_date != []:
            time_trans_before = time.strptime(release_date[0], "%a %b %d %H:%M:%S %Z %Y")
            time_trans_after = time.strftime("%Y-%m-%d", time_trans_before)
        else:
            time_trans_after = "TBD"
        return time_trans_after


    def generateHTMLHead(self):
        self.str1 = '''<html>
		<head>
		<meta charset="UTF-8">
		<title>RHEVH Verison List</title>
		</head>
		<body>
		'''
        self.str2 = "</body></html>"
        self.str3 = """<table border="1">
        <th>Build_name</th>
        <th>Tag_Name</th>
        <th>Release_date</th>
        """
        self.str4 = "</table>"

    def generateHTMLBody(self):
        str_total = ""
        key_list = ["build_name", "tag", "release_date"]
        for item in self.itemList:
            if item['build_name'] != []:
                if len(item['tag']) == 1:
                    str_total += "<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % (item['build_name'][0],
                                                                             item['tag'][0],
                                                                             self.release_date_transfer(item['release_date']))
                else:
                    str_total += "<tr><td>%s</td><td>%s,%s</td><td>%s</td></tr>" % (item['build_name'][0],
                                                                             item['tag'][0],item['tag'][1],
                                                                             self.release_date_transfer(item['release_date']))
            # for k,v in item.items():
            #     if v != [] and k in key_list:
            #         str_next2 = "<td>%s</td>" % v
            #         str_total += str_next2
        return str_total

    def run(self):
        self.getItems()
        self.merge_item_lists()
        str_table = self.generateHTMLBody()
        self.generateHTMLHead()
        str_result = self.str1 + self.str3 + str_table + self.str4 + self.str2
        with open("../result/result.html", "w+") as f:
            f.write(str_result)

if __name__ == "__main__":
    r1 = ResultHandler("../result/rhevh1.json")
    r1.run()