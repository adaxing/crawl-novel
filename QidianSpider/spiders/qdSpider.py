import scrapy
from scrapy.selector import Selector
from QidianSpider.items import QidianspiderItem

class QdspiderSpider(scrapy.Spider):
    name = 'qdSpider'
    allowed_domains = ['www.qidian.com']
    def start_requests(self):
        url = 'https://www.qidian.com/mm/all?size=1&action=1&orderId=&page=1&\vip=0&style=1&pageSize=50&siteid=0&pubflag=0&hiddenField=0&tag='
        tag = getattr(self, 'tag', None)
        if tag is not None:
            url = url + tag
        yield scrapy.Request(url, self.parse)
    
    def parse(self, response):
        '''
        select all books url from page, make requests to redirect each specific book's page
        '''
        # book_url = 'https://book.qidian.com/info/1014188209'
        # yield scrapy.Request(book_url, self.parseBook, dont_filter=True)
        books = response.xpath('//div[@class="book-mid-info"]/h4/a//@href').extract()
        for url in books:
            yield scrapy.Request('https://' + url, callback=self.parse_book, dont_filter=True)
        
    def parse_book(self, response):
        '''
        select start_read urls, created custom item  
        '''
        start_read_urls = response.xpath('/html/body/div[1]/div[6]/div[1]/div[2]/p[4]/a[1]/@href').extract()
        item = QidianspiderItem()
        for url in start_read_urls:
            yield scrapy.Request('https://' + url, meta={'item': item}, callback=self.parse_chapter_content, dont_filter=True)
        
    def parse_chapter_content(self, response):
        '''
        fetch title, chapter, content of chapter and update field values of items
        not all content save to local files as major contents of vip chapter is hidden by js
        '''
        item = response.meta['item']
        tag = getattr(self, 'tag', None)
        item['tag'] = tag
        content = ''
        # update title field value 
        book_titles = response.xpath('/html/body/div[2]/div[2]/a[4]/text()').extract()
        for name in book_titles:
            titles = item.get('title')
            if None == titles:
                item['title'] = name
                
        # update book content
        chapter_titles = response.xpath('//div[@class="text-head"]/h3/span[1]/text()').extract()
        for chapter_title in chapter_titles:
            content += chapter_title + '\n'
        
        paragraphs = response.xpath('//div[@class="read-content j_readContent"]/p/text()').extract()
        for sentence in paragraphs:
            content += sentence + '\n'

        description = item.get('content')
        if None == description:
            item['content'] = content
        else:
            item['content'] = description + content
        
        if content == '':
            yield item
        # read next chapter
        next_chapters = response.xpath('/html/body/div[2]/div[3]/div[2]/div[2]/a[3]/@href').extract()
        for url in next_chapters:
            yield scrapy.Request('https:' + url, meta={'item': item}, callback=self.parse_chapter_content, dont_filter=True)