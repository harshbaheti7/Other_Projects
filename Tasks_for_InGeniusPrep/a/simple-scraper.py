# Author: Harsh Baheti
# scrapy runspider simple-scraper.py -t csv -o a1.csv

from scrapy.spiders import Spider
from scrapy import Request
from collections import OrderedDict

class MySpider(Spider):
    name = 's0'
    allowed_domains = ['niche.com']
    start_urls = ["https://www.niche.com/k12/search/best-boarding-high-schools"]
    custom_settings = { 'DOWNLOAD_DELAY': 0.5 }
    
    def parse(self, response):
        rows = response.xpath("//div[@class='card']/a")
        items = []
        for row in rows[:50]:
            item = {}
            item['school_name'] = row.xpath("./div[@class='card__inner']/h2/text()").extract()
            item['niche_ranking'] = row.xpath("./div[@class='card__inner']/div[@class='search-result-badge']/text()").extract()
            item['location'] = row.xpath("./div[@class='card__inner']/ul/li[2]/text()").extract()
            item['num_of_students'] = row.xpath("./div[@class='card__inner']/ul[2]/li[2]/div/span[1]/text()").extract()
            item['link'] = row.xpath("./@href")[0].extract()
            url = item['link']
            req = Request(url, callback=self.parse_2)
            req.meta['data'] = item
            items.append(req)
        return items
        
    def parse_2(self, response):    
        item = response.meta['data']
        item['phone'] = response.xpath("//div[@id='app']/div[@class='platform']/section/main[@id='maincontent']/div[@class='profile profile--home']/div[@class='profile-body-wrap']/div[@class='profile-body profile-body--with-nav']/div[@class='profile-blocks']/section[@id='about']/div[@class='profile__buckets']/div[@class='profile__bucket--2']/div/div[@class='blank__bucket']/div[@class='scalar--three']/div[@class='scalar__value']/span/text()").extract()
        item['website'] = response.xpath("//div[@id='app']/div[@class='platform']/section/main[@id='maincontent']/div[@class='profile profile--home']/div[@class='profile-body-wrap']/div[@class='profile-body profile-body--with-nav']/div[@class='profile-blocks']/section[@id='about']/div[@class='profile__buckets']/div[@class='profile__bucket--2']/div/div[@class='blank__bucket']/div[@class='profile__website']/div[@class='profile__website__url']/a[@class='profile__website__link']/text()").extract()
        item['video_url'] = response.xpath("//iframe[@id='youtube-embed']/@src/text()").extract()
        item['student_teacher_ratio'] = response.xpath("//div[@id='app']/div[@class='platform']/section/main[@id='maincontent']/div[@class='profile profile--home']/div[@class='profile-body-wrap']/div[@class='profile-body profile-body--with-nav']/div[@class='profile-blocks']/section[@id='teachers']/div[@class='profile__buckets']/div[@class='profile__bucket--1']/div/div[@class='blank__bucket']/div[@class='scalar']/div[@class='scalar__value']/span/text()").extract()
        item['yearly_tuition'] = response.xpath("//div[@id='app']/div[@class='platform']/section/main[@id='maincontent']/div[@class='profile profile--home']/div[@class='profile-body-wrap']/div[@class='profile-body profile-body--with-nav']/div[@class='profile-blocks']/section[@id='tuition']/div[@class='profile__buckets']/div[@class='profile__bucket--1']/div[@class='scalar__bucket']/div[@class='scalar--one']/div[@class='scalar__value']/span/text()").extract()
        item['avg_financial_aid'] = response.xpath("//div[@id='app']/div[@class='platform']/section/main[@id='maincontent']/div[@class='profile profile--home']/div[@class='profile-body-wrap']/div[@class='profile-body profile-body--with-nav']/div[@class='profile-blocks']/section[@id='tuition']/div[@class='profile__buckets']/div[@class='profile__bucket--2']/div/div[@class='blank__bucket']/div[@class='scalar--three'][3]/div[@class='scalar__value']/span/text()").extract()
        item['application_deadline'] = response.xpath("//div[@id='app']/div[@class='platform']/section/main[@id='maincontent']/div[@class='profile profile--home']/div[@class='profile-body-wrap']/div[@class='profile-body profile-body--with-nav']/div[@class='profile-blocks']/section[@id='applying']/div[@class='profile__buckets']/div[@class='profile__bucket--1']/div/div[@class='blank__bucket']/div[@class='scalar--three'][1]/div[@class='scalar__value']/span/text()").extract()
        #More fields can be added similarly
        return item