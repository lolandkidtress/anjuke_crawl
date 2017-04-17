# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from tutorial.items import anjukeItem
from tutorial.tools import writeCSV
from tutorial.tools import writeHEAD
import json


class anjuke(scrapy.Spider):
    name = "anjuke"
    allowed_domains = ["anjuke.com"]
    start_urls = [
        "http://dali.anjuke.com/sale/dalishib/b711-p1/?from_price=50&to_price=100#filtersort"
    ]
    next_URL = "http://dali.anjuke.com/sale/dalishib/b711-p{0}/?from_price=50&to_price=100#filtersort"
    MAX_PAGES = 50
    FROM_PAGES = 2
    HEAD = False

    URLS=start_urls

    def parse(self, response):
        filename = response.url
        print "start @:" +filename

        lis = response.xpath('//ul[@id="houselist-mod"]/li').extract()
        l_list = len(lis)
        if l_list>0 and self.HEAD!=True:
            print 'write head'
            writeHEAD()
            self.HEAD = True
        for i in range(l_list):
            item = anjukeItem()

            base_li = '//ul[@id="houselist-mod"]/li[{0}]'.format(i)
            title_div = base_li+'/div/div[@class="house-title"]/a/@title'
            href_div = base_li + '/div/div[@class="house-title"]/a/@href'

            #title
            desc = response.xpath(title_div+'[1]').extract()
            if len(desc) > 0 :
                #print desc[0].encode("utf-8")
                item["title"] = desc[0].encode("utf-8")
            #detail_link
            link = response.xpath(href_div + '[1]').extract()
            if len(link) > 0:
                #print desc[0].encode("utf-8")
                item["detail_link"] = link[0].encode("utf-8")
            #明细
            #大小
            size = response.xpath(base_li+'/div[2]/div[2]/span[1]/text()').extract()
            if len(size) > 0 :
                #print size[0].encode("utf-8")
                item["size"] = size[0].encode("utf-8")
            #地址 comm_add
            comm_add = response.xpath(base_li+'/div[2]/div[3]/span/text()').extract()
            if len(comm_add) > 0:
                #print comm_add[0].encode("utf-8")
                item["comm_add"] = comm_add[0].replace('\t','').replace('\n','').replace(' ','').encode("utf-8")
            #单价 unit_price
            unit_price = response.xpath(base_li+'/div[2]/div[2]/span[3]/text()').extract()
            if len(unit_price) > 0:
                #print unit_price[0].encode("utf-8")
                item["unit_price"] = unit_price[0].encode("utf-8")

            #buildTime 建造时间
            buildTime = response.xpath(base_li+'/div[2]/div[2]/span[5]/text()').extract()
            if len(buildTime) > 0:
                #print buildTime[0].encode("utf-8")
                item["buildTime"] = buildTime[0].encode("utf-8")

            # 总价 建造时间
            price_det = response.xpath(base_li+'/div[3]/span/strong/text()').extract()
            if len(price_det) > 0:
                #print price_det[0].encode("utf-8")
                item["price_det"] = price_det[0].encode("utf-8")
            #if len(desc) > 0:
            #   yield Request(link[0], meta={'item': item},callback=self.parse_detail)

            #print item
            writeCSV(item)

        if self.FROM_PAGES <= self.MAX_PAGES:
            next_page=self.next_URL.format(self.FROM_PAGES)
            self.FROM_PAGES = self.FROM_PAGES + 1
            print "next url:" + next_page
            yield Request(next_page, callback=self.parse)
        else :
            print "end,currpage:" + str(self.FROM_PAGES)
        # hrefs = response.xpath('//div[@class="multi-page"]//@href').extract()
        #
        # for href in hrefs:
        #     # print href.
        #     print "start track:"+href


        #  //*[@id="content"]/div[4]/div[7]/a[3]
        #// *[ @ id = "content"] / div[4] / div[7] / a[3]
        # with open(filename, 'wb') as f:
        #     f.write(response.body)


    def parse_detail(self,response):
        item = response.meta['item']
        filename = response.url
        # print "detail url @:" +filename

        menu_size = response.xpath('//*[@id="content"]/div[1]').extract()
        # if len(menu_size) >0 :
        #     print len(menu_size)
        community = response.xpath('//*[@id="content"]/div[1]/a[{0}]/text()'.format(len(menu_size))).extract()
        if len(community) >0:

            item["community"] = community[0].encode("utf-8")
            communityid = response.xpath('//*[@id="content"]/div[1]/a[3]/@href').extract()
            if len(communityid) >0:
                #print communityid[0].encode("utf-8")
                item["communityid"] = communityid[0].encode("utf-8").split("/")[-1]
                hist_url = 'http://dali.anjuke.com/v3/ajax/prop/pricetrend/?commid={0}'.format(communityid[0].encode("utf-8").split("/")[-1])
                #yield Request(hist_url,meta={'item': item}, callback=self.parse_hist)

    def parse_hist(self, response):
        price = ""
        item = response.meta['item']
        #print 'parse_hist'
        j_body = json.loads(response.body_as_unicode())
        hist = j_body["community"]
        for j in range(len(hist)):
            price_hist = hist[j]
            its = price_hist.items()
            for key, value in its:
                #print key, value  # print key,dict[key]
                price = price + value+","
        item["hist"] = price

if __name__ == "__main__":
    body = '{"status":"ok","community":[{"201405":"0"},{"201406":"0"},{"201407":"0"},{"201408":"0"},{"201409":"0"},{"201410":"0"},{"201411":"0"},{"201412":"0"},{"201501":"0"},{"201502":"0"},{"201503":"0"},{"201504":"8922"},{"201505":"9094"},{"201506":"9716"},{"201507":"9647"},{"201508":"9614"},{"201509":"9890"},{"201510":"10870"},{"201511":"12023"},{"201512":"0"},{"201601":"10788"},{"201602":"10823"},{"201603":"10743"},{"201604":"10778"},{"201605":"10893"},{"201606":"10961"},{"201607":"11973"},{"201608":"13018"},{"201609":"11615"},{"201610":"11914"},{"201611":"13430"},{"201612":"14072"},{"201701":"14150"},{"201702":"14168"},{"201703":"14647"},{"201704":"19781"}],"area":[{"201405":"0"},{"201406":"0"},{"201407":"0"},{"201408":"0"},{"201409":"0"},{"201410":"0"},{"201411":"0"},{"201412":"0"},{"201501":"0"},{"201502":"0"},{"201503":"0"},{"201504":"6093"},{"201505":"6129"},{"201506":"6186"},{"201507":"6204"},{"201508":"6175"},{"201509":"6332"},{"201510":"6215"},{"201511":"6215"},{"201512":"6178"},{"201601":"6178"},{"201602":"6198"},{"201603":"6151"},{"201604":"6171"},{"201605":"6236"},{"201606":"6275"},{"201607":"6300"},{"201608":"6334"},{"201609":"6352"},{"201610":"6367"},{"201611":"6424"},{"201612":"6424"},{"201701":"6459"},{"201702":"6467"},{"201703":"6685"},{"201704":"6930"}],"comm_midchange":"0.285625","area_midchange":"0.0295917"}'
    j_body = json.loads(body)
    hist = j_body["community"]
    for j in range(len(hist)):
        price=hist[j]
        its = price.items()
        for key, value in its:
            print key, value  # print key,dict[key]



