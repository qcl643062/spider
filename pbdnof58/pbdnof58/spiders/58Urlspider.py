from scrapy_redis.spiders import RedisSpider
from pbdnof58.items import Pbdnof58Loader
from redis import Redis
from scrapy import log
from time import sleep

class Myspider(RedisSpider):
    '''spider that reads urls from redis queue (myspider:start_urls).'''
    name = 'myspider_58page'
    redis_key = 'myspider:58_urls'

    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domain', '')
        self.allowed_domans = filter(None, domain.split(','))
        super(Myspider, self).__init__(*args, **kwargs)
        self.url = 'http://bj.58.com'

    def parse(self, response):
        el = Pbdnof58Loader(response=response)
        PageUrl = response.xpath('//a[contains(@class, "next")]/@href').extract()
        self.log(PageUrl, level=log.DEBUG)
        r = Redis()
        if PageUrl != []:
            r.lpush('myspider:58_urls', self.url + PageUrl[0])
            sleep(1)
            el.add_value('UrlofPage', self.url + PageUrl[0])
        urls = response.xpath('//table[contains(@class, "tbimg")]/tr')
        for url in urls:
            url = url.xpath('td[contains(@class, "t")]/a/@href').extract()
            if len(url) == 1 and 'zhuan' not in url[0]:
                r.lpush('myspider:start_urls', url[0])
        return el.load_item()
