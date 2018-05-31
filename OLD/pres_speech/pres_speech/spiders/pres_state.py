
import  scrapy


class  State_Union_Speech(scrapy.Spider):
    name = 'state_union'

    custom_settings = {
        "DOWNLOAD_DELAY": 3,
        "CONCURENT_REQUESTS_PER_DOMAIN": 3,
        "HTTPCACHE_ENABLED": True
    }

    start_urls = ['https://en.wikisource.org/wiki/Portal:State_of_the_Union_Speeches_by_United_States_Presidents']

    def parse(self, response):

        years = response.xpath('//div[@class="mw-parser-output"]/ul/li/a[@class="extiw"]/text()').extract()
        counter = 0
        year_list = [x for x in years if len(x) == 4]

        # Extract the links to the individual festival pages
        for href in response.xpath('//div[@class="mw-parser-output"]/ul/li/a[contains(text(),"State of the Union")]/@href').extract()[:-1]:
            # For each link, call parse_nom function
            main = 'https://en.wikisource.org'
            url = main + href

            year = year_list[counter]
            counter += 1

            yield scrapy.Request(
                url=url,
                callback=self.parse_state,
                meta={'url':url, 'year':year}
            )


    def parse_state(self, response):

        year = response.request.meta['year']
        speaker = response.xpath('//span[@id="header_author_text"]/span[@class="fn"]/text()').extract()[0]
        speech = response.xpath('//div[@class="mw-parser-output"]/div/p/text()').extract()

        yield {
            'speaker': speaker,
            'year':year,
            'speech': speech
        }
