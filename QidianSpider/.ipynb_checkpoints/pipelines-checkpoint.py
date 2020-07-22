# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import os

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class QidianspiderPipeline(object):
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        file_name = adapter.get('title') + '.txt'
        dir_name = adapter.get('tag')
        # if not asign any specific tag, will create dir based on novels/*.txt
        if not dir_name:
            dir_name = 'novels'
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)            
        new_path = os.path.join(dir_name, file_name)
        if adapter.get('title'):
            self.file = open(new_path, 'w', encoding='utf-8')
            self.file.write(adapter.get('content') + '\n')
        return item
    
    def spider_closed(self, spider):
        self.file.close()
