import  scrapy

class  InaugurationSpeech(scrapy.Spider):

    name = 'inauguration3' # name for scrapy crawl call

    custom_settings = {
        "DOWNLOAD_DELAY": 3,
        "CONCURENT_REQUESTS_PER_DOMAIN": 3,
        "HTTPCACHE_ENABLED": True
    }

    start_urls = ['https://en.wikisource.org/wiki/Abraham_Lincoln%27s_Second_Inaugural_Address'] # webpage with data source links

    def parse(self, response):

        speech = response.xpath('//div[@class="mw-parser-output"]/div/p/text()').extract()

        yield {
            'speech': speech
        }



# terminal call in highest scrapy directory: scrapy crawl inauguration3 -o inauguration3.csv
