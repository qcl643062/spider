from scrapy_redis.spiders import RedisSpider
from JDspider.items import JDspiderLoader
from splinter import Browser
from scrapy import log



class Myspider(RedisSpider):
    '''spider that reads urls from redis queue (myspider:start_urls).'''
    name = 'jdspider'
    redis_key = 'jdspider_urls'

    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domain', '')
        self.allowed_domans = filter(None, domain.split(','))
        super(Myspider, self).__init__(*args, **kwargs)

    def parse(self, response):
        el = JDspiderLoader(response=response)
        el.add_xpath('title', '//*[@id="name"]/h1/text()')
        with Browser() as browser:
            url = response.url
            browser.visit(url)
            price = browser.find_by_id('jd-price')
            if price == []:
                price = browser.find_by_xpath('//*[@id="price"]/strong')
            # self.log(price[0].value, level=log.DEBUG)
            el.add_value('price', price[0].value[1:])
        with Browser() as browser:
            number = response.url.split('/')[-1].split('.')[0]
            url = 'http://club.jd.com/review/' + number + '-2-1.html'
            browser.visit(url)
            shaitu = browser.find_by_xpath('//*[@id="comments-list"]/div[1]/ul/li[5]/a/em')
            el.add_value('shaitu', shaitu[0].value[1:-1])
            haoping = browser.find_by_xpath('//*[@id="comments-list"]/div[1]/ul/li[2]/a/em')
            el.add_value('haoping', haoping[0].value[1:-1])
            zhongping = browser.find_by_xpath('//*[@id="comments-list"]/div[1]/ul/li[3]/a/em')
            el.add_value('zhongping', zhongping[0].value[1:-1])
            chaping = browser.find_by_xpath('//*[@id="comments-list"]/div[1]/ul/li[4]/a/em')
            el.add_value('chaping', chaping[0].value[1:-1])
        return el.load_item()

