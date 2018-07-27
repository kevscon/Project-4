import  scrapy

class  FarewellSpeech(scrapy.Spider):

    name = 'farewell' # name for scrapy crawl call

    custom_settings = {
        "DOWNLOAD_DELAY": 3,
        "CONCURENT_REQUESTS_PER_DOMAIN": 3,
        "HTTPCACHE_ENABLED": True
    }

    start_urls = ['http://www.presidency.ucsb.edu/farewell_addresses.php'] # webpage with data source links

    # define function to collect webpage source links
    def parse(self, response):

        links1 = response.xpath('//table[@width="650"]/tr/td/a/@href').extract()
        links2 = response.xpath('//table[@width="650"]/tr/td/p/a/@href').extract()
        hrefs = links1 + links2
        # extract the links to the individual pages
        for href in hrefs:

            # for each link, call parse function to scrape data from each webpage
            yield scrapy.Request(
                url=href,
                callback=self.parse_speech,
                meta={'url':href}
            )

    # define function to scrape data from each webpage
    def parse_speech(self, response):

        type = 'farewell'
        speaker = response.xpath('//table[@width="100%"]/tr/td/img/@alt').extract()[0]
        date = response.xpath('//span[@class="docdate"]/text()').extract()[0]
        speech = response.xpath('//span[@class="displaytext"]/p/text()').extract()

        # specify items to provide export file
        yield {
            'type': type,
            'speaker': speaker,
            'date': date,
            'speech': speech
        }

# terminal call in highest scrapy directory: scrapy crawl farewell -o farewell.csv
