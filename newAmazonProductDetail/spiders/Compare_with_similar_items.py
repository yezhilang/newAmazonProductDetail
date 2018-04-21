import requests
from lxml import etree
import re


if __name__ == "__main__":

    session = requests.session()
    url = "https://www.amazon.com/Fitbit-Charge-Wireless-Activity-Wristband/dp/B00N2BW638/ref=lp_8849526011_1_2?s=electronics&ie=UTF8&qid=1524280364&sr=1-2"
    headers = {
        "User-Agent":"Mozila/5.0"
    }
    html = session.get(url=url, headers=headers).text
    selector = etree.HTML(html)

    trs = selector.xpath("//*[@id='HLCXComparisonTable']/tr")
    this_asin = "thisasin"
    counter = 1
    campare = {}
    for tr in trs:
        l = []
        if counter == 1:
           xpath = "./th"
           subitems = tr.xpath(xpath)
           _key = "category"
           asins = []
           _as = ""
           for items in subitems:
               asxpath = "./a[1]/@href"
               try:
                   _as = re.findall("/dp/.*?/",items.xpath(asxpath)[0].strip())[0][4:-1]
               except:
                   _as = this_asin
               asins.append(_as)
               v = ""
               xpath = ".//*"
               item = items.xpath(xpath)
               for text in item:
                   try:
                       v = v + text.xpath("./text()")[0].strip()
                   except:
                       continue
               l.append(v)
           campare["asin"] = str(asins)
           campare[_key] = str(l)
           counter = counter + 1
           continue
        if counter == 2 or counter == 3:
            counter = counter + 1
            continue
        _key = tr.xpath("./th[1]/span[1]/text()")[0].strip()
        xpath = "./td"
        subitems = tr.xpath(xpath)
        for items in subitems:
           v = ""
           xpath = ".//*"
           item = items.xpath(xpath)
           for text in item:
               try:
                   v = v + text.xpath("./text()")[0].strip()
               except:
                   continue
           if v:
               l.append(v)

           _value = str(l)
           campare[_key] = _value
           counter = counter + 1
    l = []
    counter = 0
    for i in campare["category"]:
        d = {}
        for j in campare.keys():
            d[j] = eval(campare[j])[counter]
        counter = counter + 1
        l.append(d)
        if counter == len(eval(campare["category"])):
            break
    for i in l:
        i["Price"] = i["Price"].split("$")[1]
        print i



