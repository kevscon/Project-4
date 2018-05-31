import  scrapy

class  InaugurationSpeech(scrapy.Spider):

    name = 'state_union2' # name for scrapy crawl call

    custom_settings = {
        "DOWNLOAD_DELAY": 3,
        "CONCURENT_REQUESTS_PER_DOMAIN": 3,
        "HTTPCACHE_ENABLED": True
    }

    start_urls = ['https://en.wikisource.org/wiki/George_Washington%27s_First_State_of_the_Union_Address'] # webpage with data source links

    def parse(self, response):

        speech = response.xpath('//div[@class="mw-parser-output"]/div/p/text()').extract()

        yield {
            'speech': speech
        }



# terminal call in highest scrapy directory: scrapy crawl state_union2 -o state_union2.csv
