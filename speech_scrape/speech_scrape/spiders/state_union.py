import  scrapy
import re

class  StateUnionSpeech(scrapy.Spider):

    name = 'state_union' # name for scrapy crawl call

    custom_settings = {
        "DOWNLOAD_DELAY": 3,
        "CONCURENT_REQUESTS_PER_DOMAIN": 3,
        "HTTPCACHE_ENABLED": True
    }

    start_urls = ['https://en.wikisource.org/wiki/Portal:State_of_the_Union_Speeches_by_United_States_Presidents'] # webpage with data source links

    # define function to collect webpage source links
    def parse(self, response):

        main = 'https://en.wikisource.org' # link to main source webpage

        # extract the links to the individual pages
        for href in response.xpath(
                '//div[@class="mw-parser-output"]/ul/li/a[contains(text(), "State of the Union")]/@href'
        ).extract()[:-1]:

            url = main + href # complete webpage address

            # for each link, call parse function to scrape data from each webpage
            yield scrapy.Request(
                url=url,
                callback=self.parse_speech,
                meta={'url':url}
            )

    # define function to scrape data from each webpage
    def parse_speech(self, response):

        type = 'state_union'
        speaker = response.xpath('//span[@class="fn"]/text()').extract()[0]
        date = response.xpath('//div[@class="gen_header_title"]/b/following-sibling::text()').extract()[0]
        date = re.search(r'(\d+)', date).group()
        speech = response.xpath('//div[@class="mw-parser-output"]/p/text()').extract()

        # specify items to provide export file
        yield {
            'type': type,
            'speaker': speaker,
            'date': date,
            'speech': speech
        }

# terminal call in highest scrapy directory: scrapy crawl state_union -o state_union.csv
