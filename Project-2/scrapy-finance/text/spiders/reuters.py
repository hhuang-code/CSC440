import os
import re
import pdb

import scrapy
from scrapy.spiders import CrawlSpider
from w3lib.html import remove_tags, remove_tags_with_content

class ReutersSpider(CrawlSpider):
    name = 'reuters'
    handle_httpstatus_list = [200, 301, 400, 404]
    allowed_domains = ['reuters.com']
    start_urls = ['https://www.reuters.com']

    def parse(self, response):
        # Parse the response page
        url = response.url

        if 'reuters.com' not in url:
            return

        # Visit urls starting with reuters.com/articles
        if 'reuters.com/article' not in url:
            return self.parse_links(response)
        else:
            return self._parse_response(response)

    def _parse_response(self, response):
        # Analyse response
        if response.status == 404:
            print(response.headers)

        # Get the title first
        title = response.css('title::text').extract_first()

        # Replace / with a space - creates issues with writing to file
        title = title.replace('/', ' ')

        # Get the first div with class content
        content = response.css('div.inner-container')[0]

        text = title + '\n\n'
        for child in content.xpath('//p[not(@class)] | //li[not(@class)]'):
            # Get the text from this child <p></p> tag
            paragraph = child.extract()

            # Remove tags including <p> and <a>
            paragraph = remove_tags(remove_tags_with_content(paragraph, ('script', ))).strip()

            # Replace '&amp;' with '&'
            paragraph = paragraph.replace('&amp;', '&')

            text += paragraph + '\n\n'

        # get post date
        meta = response.xpath('//meta[@name="sailthru.date"]').extract_first()
        date = self.get_date(meta)
        if date is None:    # not found date, skip
            return self.parse_links(response)
        # Create the directory
        dirname = self.create_dir(date)   # arg: e.g. 2017-12-04

        # Save the title and the text both
        tokens = response.url.split('/')
        filename = '{}/{}'.format(dirname, tokens[-1] + '.txt')
        if not os.path.exists(filename):
            f = open(filename, 'w')
            #f.write(text.encode('ascii', 'ignore'))
            f.write(text)
            f.close()

        return self.parse_links(response)

    def get_date(self, string):
        # for articles starting from 2010
        date_pattern = re.compile('(201[0-9]{1}-[0-9]{2}-[0-9]{2})')
        date = date_pattern.search(string)
        if date is not None:
            return date.group(1)
        else:
            return None

    def create_dir(self, day):
        # Create the directory
        dirname = '/home/aaron/Documents/Courses/440/dataset/news/raw/reuters'
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        dirname = dirname + '/' + day
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        return dirname

    def parse_links(self, response):
        #pdb.set_trace()
        links = response.css('a::attr(href)').extract()
        for link in links:

            if 'article' not in link:
                continue

            if link.lower().endswith('.png') or link.lower().endswith('.jpg'):
                continue

            tokens = link.split('/')
            if len(tokens) < 2:
                continue

            next_page = response.urljoin(link)
            yield scrapy.Request(next_page, callback=self.parse)

