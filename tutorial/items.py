# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class anjukeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #标题
    title = scrapy.Field()
    #地址
    comm_add = scrapy.Field()
    #总价
    price_det = scrapy.Field()
    #单价
    unit_price = scrapy.Field()
    #面积
    size = scrapy.Field()
    #建造时间
    buildTime = scrapy.Field()
    #详情地址
    detail_link = scrapy.Field()
    # 小区
    community = scrapy.Field()
    # 小区id
    communityid = scrapy.Field()
    #价格历史
    hist = scrapy.Field()

    pass
