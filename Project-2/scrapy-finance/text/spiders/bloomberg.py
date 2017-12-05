import os
import pdb

import scrapy
from scrapy.spiders import CrawlSpider
from w3lib.html import remove_tags, remove_tags_with_content

from text.settings import BLOOMBERG_PATH

class BloombergSpider(CrawlSpider):
    name = 'bloomberg'
    handle_httpstatus_list = [200, 404]
    allowed_domains = ['bloomberg.com']
    start_urls = ['https://www.bloomberg.com']

    def parse(self, response):
        # Parse the response page
        url = response.url

        if 'bloomberg.com' not in url:
            return

        # Visit urls starting with bloomberg.com/news/articles and start from 2010
        if 'bloomberg.com/news/articles/201' not in url:
            return self.parse_links(response)
        else:
            return self._parse_response(response)

    def _parse_response(self, response):
        # Analyse response
        if response.status == 404:
            return self.parse_links(response)

        # Get the title first
        title = response.css('title::text').extract_first()

        # Replace / with a space - creates issues with writing to file
        title = title.replace('/', ' ')

        # Get the first div with class content
        content = response.css('div.content-well')[0]

        text = title + '\n\n'
        for child in content.xpath('//p[not(@class)] | //li[not(@class)]'):
            # Get the text from this child <p></p> tag
            paragraph = child.extract()

            # Remove tags including <p> and <a>
            paragraph = remove_tags(remove_tags_with_content(paragraph, ('script', ))).strip()

            # Replace '&amp;' with '&'
            paragraph = paragraph.replace('&amp;', '&')

            text += paragraph + '\n\n'
        # Create the directory
        tokens = response.url.split('/')
        dirname = self.create_dir(tokens[-2])

        # Save the title and the text both
        filename = '{}/{}'.format(dirname, tokens[-1] + '.txt')
        if not os.path.exists(filename):
            f = open(filename, 'w')
            #f.write(text.encode('ascii', 'ignore'))
            f.write(text)
            f.close()

        return self.parse_links(response)

    def create_dir(self, day):
        # Create the directory
        dirname = BLOOMBERG_PATH
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        dirname = dirname + '/' + day
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        return dirname

    def parse_links(self, response):
        links = response.css('a::attr(href)').extract()
        for link in links:

            if 'news/articles' not in link:
                continue

            if link.lower().endswith('.png') or link.lower().endswith('.jpg'):
                continue

            tokens = link.split('/')
            if len(tokens) < 2:
                continue
            filename = BLOOMBERG_PATH + tokens[-2] + '/' + tokens[-1] + '.txt'
            if os.path.exists(filename):
                continue

            if link is not None:            
                next_page = response.urljoin(link)
                yield scrapy.Request(next_page, callback=self.parse)

