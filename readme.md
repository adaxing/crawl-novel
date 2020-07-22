This mini project is only for my interest and practise of learning scrapy framework. It is to crawl novels from one of largest Chinese novel website, https://www.qidian.com.
The start url page is about girl's favorites, and my qdSpider only crawled for the first page. To avoid anti-scraping, random user-agent is added to middleware and set to
crawl only one page.

### Start run
    scrapy crawl qdSpider [-a tag=特工]

'-a tag=xx' is to help to crawl specific style of books, and create directory based on tag, otherwise, default 'novels' directory will be created, which means first page of 
completed and free books will be downloaded.
