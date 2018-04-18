# coding:utf-8
import scrapy
from lxml import etree

class productSpider(scrapy.Spider):
    name = "product"
    # allowed_urls = ["www.amazon.com"]
    # start_urls = ["#"]

    def getTasks(self):
        tasks = []

        for task in tasks:
            yield task

    def start_requests(self):
        # start_url = ["#"]
        base_url = "https://www.amazon.com/dp/"
        tasks = ["B01K8P2JWS"]



        for task in tasks:
            url = base_url + str(task)
            # yield
            print("-------------------------"+url+"-----------------")
            yield scrapy.Request(url, callback= self.parse)

    def parse(self, response):
        # amazon_product_detail
        #
        # filed_xpath:

        if response.status != 200:
            print("-----------------something wrong with the request, scrapy is making another request--------------------")
            return scrapy.Request(response.url, callback= self.parse)

        _item = {}

        price = response.xpath("//*[@id='priceblock_ourprice']/text()").extract()[0]

        _item["price"] = price

        category =  response.xpath("//*[@id='productTitle']/text()").extract()[0].strip()

        _item["category"] = category

        starts = response.xpath("//*[@id='acrPopover']/span[1]/a/i[1]/span/text()").extract()[0].strip()

        _item["starts"] = starts

        deliver_fee = response.xpath("//*[@id='ourprice_shippingmessage']/span/b/text()").extract()[0].strip()

        _item["deliver_fee"] = deliver_fee

        product_brief = {"item":[]}



        x = response.xpath("//*[@id='fbExpandableSectionContent']/ul/li")
        for i in x:
            item = i.xpath("./span[1]/text()").extract()[0].strip()
            product_brief["item"].append(item)
            # print(item)
        _item["product_brief"] = product_brief

        product_detail = {}

        # x = response.xpath("//*[@id='detail-bullets']/table/tr/td/div/ul/li")
        # for i in x:
        #     _key = i.xpath("./a/text()").extract()[0]
        #     _value = i.xpath("./text()").extract()[0]
        #     product_detail[_key] = _value
        # _item["product_detail"] = product_detail
        # from lxml import etree
        a = response.xpath("//*[@id='SalesRank']").extract()[0]
        li = etree.HTML(a.replace("\n", "")).xpath("//li[@id='SalesRank']")
        # li.xpath("./text()")
        # li[0].xpath("./text()")

        salesrank = li[0].xpath("./text()")[0][:-1]

        _item["salesrank"] = salesrank

        important_information = response.xpath("//*[@id='importantInformation']/div/div/text()")[1].extract()

        _item["important_information"] = important_information

        with open("j.txt","w+") as f:
            f.write(str(_item))


