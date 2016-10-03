# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

#class EpScrapePipeline(object):
    #def __init__(self):
     #   self.file = open('z.json', 'wb')

   # def process_item(self, item, spider):
       # line = json.dumps(dict(item), indent = 4) + "\n"
       # self.file.write(line)
       # return item


#intitial class
class EpScrapePipeline(object):
    def process_item(self, item, spider):
        return item