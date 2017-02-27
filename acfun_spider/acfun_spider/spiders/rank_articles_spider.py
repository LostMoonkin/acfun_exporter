import scrapy
import requests
import re
import json
from acfun_spider.items import ArticleItem


class RankArticlesSpider(scrapy.Spider):
    name = 'rank_articles_spider'

    start_urls = [
        'http://www.acfun.cn/v/list110/index.htm',
        'http://www.acfun.cn/v/list73/index.htm',
        'http://www.acfun.cn/v/list74/index.htm',
        'http://www.acfun.cn/v/list75/index.htm',
        'http://www.acfun.cn/v/list164/index.htm'
    ]

    def parse(self, response):

        div_selector = response.xpath(
            '//div[@id="block-rank-article"]/div[@class="mainer"]')

        item_url = div_selector.xpath('div[@class="item "]/a/@href').extract()

        last_item_url = div_selector.xpath(
            'div[@class="item last-item"]/a/@href').extract()

        urls = ["http://www.acfun.cn" + x for x in item_url] + \
            ["http://www.acfun.cn" + x for x in last_item_url]

        for url in urls:
            yield scrapy.Request(url, callback=self.parse_article_content)

    def parse_article_content(self, response):

        url = response.url

        desc = response.xpath('//div[@id="area-title-view"]')

        try:
            type = desc.xpath(
                'p[@id="title_1"]/span[@class="crumbs_1"]/a[2]/text()').extract()[0]
        except:
            type = 'Default'

        try:
            title = desc.xpath(
                'p[@id="title_1"]/span[@class="txt-title-view_1"]/text()').extract()[0]
        except:
            return
        info = {'views': '', 'comments': '', 'time': ''}
        try:
            time = desc.xpath(
                'p[@id="title_1"]/span[@id="txt-info-title_1"]/span[@class="time"]/text()').extract()[0]
            info['time'] = time
        except:
            pass

        try:
            ac = re.findall('/ac(.*)', url)[0]
            info_req = requests.get('http://www.acfun.cn/content_view.aspx?contentId=' + ac + '&channelId=110')
            info_data = json.loads(info_req.text)
            info['views'] = info_data[0]
            info['comments'] = info_data[1]
        except:
            pass

        item = ArticleItem()
        item['title'] = title
        item['type'] = type
        item['url'] = url
        item['info'] = info

        yield item
