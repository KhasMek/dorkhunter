from scrapy.spiders import Spider
from scrapy.selector import Selector
from dorkhunter.items import DorkhunterItem
from scrapy.http import Request


class MySpider(Spider):
    name = "dorkhunter"
    allowed_domains = ["exploit-db.com"]
    start_urls = ["https://www.exploit-db.com/google-hacking-database/?action=search&ghdb_search_page=1&ghdb_search_text=&ghdb_search_cat_id=0"]

    def parse(self, response):
        hxs = Selector(response)
        visited_pages = ['https://www.exploit-db.com/google-hacking-database/?action=search&ghdb_search_page=1&ghdb_search_text=&ghdb_search_cat_id=0']
        table = hxs.xpath('//table[@class="category-list"]/tbody/tr')
        next_page = hxs.xpath('//div[@class="pagination"]/a[@class="color"]/@href').extract()

        for entree in table:
            dork = DorkhunterItem()
            dork['title'] = entree.xpath('.//td[2]/a/text()').extract_first().strip()
            dork['date_added'] = entree.xpath('.//td[@class="date"]/text()').extract_first()
            dork['category'] = entree.xpath('.//td[@class="gd-description"]/a/text()').extract_first().strip()
            dork['summary'] = entree.xpath('.//td[@class="gd-description"]/p/text()').extract_first().strip()
            dork['direct_link'] = entree.xpath('.//td[2]/a/@href').extract_first().strip()
            yield dork

        for page in next_page:
            if page not in visited_pages:
                visited_pages.append(page)
                yield Request(page, self.parse)
