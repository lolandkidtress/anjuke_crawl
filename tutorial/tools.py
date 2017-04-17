# -*- coding: utf-8 -*-

import csv

def writeCSV(item):

    csvfile = file('yunnan.csv', 'ab+')
    writer = csv.writer(csvfile,delimiter="^")
    list=[]

    print item
    list.append(item.get("title"))
    list.append(item.get("comm_add"))
    list.append(item.get("price_det"))
    list.append(item.get("unit_price"))
    list.append(item.get("size"))
    list.append(item.get("buildTime"))
    list.append(item.get("detail_link"))
    # list.append(item.get("community"))
    # list.append(item.get("communityid"))
    # list.append(item.get("hist"))

    writer.writerow(list)

    csvfile.close()

def writeHEAD():

    csvfile = file('yunnan.csv', 'wb')
    writer = csv.writer(csvfile)
    writer.writerow(['title', 'comm_add', 'price_det','unit_price','size','buildTime','detail_link'])

    csvfile.close()