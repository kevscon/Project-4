# initialize project and folders with: scrapy startproject speech_scrape
# test xpath calls: scrapy shell 'http://www.presidency.ucsb.edu/nomination.php'

import  scrapy

class  ConventionSpeech(scrapy.Spider):

    name = 'convention' # name for scrapy crawl call

    custom_settings = {
        "DOWNLOAD_DELAY": 3,
        "CONCURENT_REQUESTS_PER_DOMAIN": 3,
        "HTTPCACHE_ENABLED": True
    }

    start_urls = ['http://www.presidency.ucsb.edu/nomination.php'] # webpage with data source links

    # define function to collect webpage source links
    def parse(self, response):

        # extract the links to the individual pages
        for href in response.xpath(
                '//tr/td[@class="ver12"]/a/@href'
        ).extract():

            # for each link, call parse function to scrape data from each webpage
            yield scrapy.Request(
                url=href,
                callback=self.parse_speech,
                meta={'url':href}
            )

    # define function to scrape data from each webpage
    def parse_speech(self, response):

        type = 'convention'
        speaker = response.xpath('//table[@width="760"]/tr/td/table/tr/td/img/@alt').extract()[0]
        date = response.xpath('//tr/td/span[@class="docdate"]/text()').extract()[0] # change to year?
        speech = response.xpath('//span[@class="displaytext"]/p/text()').extract()

        # specify items to provide export file
        yield {
            'type': type,
            'speaker': speaker,
            'date': date,
            'speech': speech
        }

# terminal call in highest scrapy directory: scrapy crawl convention -o convention.csv
