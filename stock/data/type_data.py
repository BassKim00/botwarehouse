from django import setup
import os, sys, re
import requests
from bs4 import BeautifulSoup


if __name__ == "__main__":
    proj_path = "/Users/leeuram/2018Project/botwarehouse"
    sys.path.append(proj_path)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mirae.settings")
    setup()

from stock.models import *


class InfoData:

    def __init__(self):
        pass

    def getTypeData(self):
        rows = Stock.objects.exclude(code='000000')

        for row in rows:

            if row.businessType is None:
                url = self.makeUrlString(row.code)
                source_code = requests.get(url)
                plain_text = source_code.text
                soup = BeautifulSoup(plain_text, 'lxml')
                tags = soup.findAll("div", class_="trade_compare")

                if len(tags) > 0:
                    soup_detail = BeautifulSoup(str(tags[0]), 'lxml')
                    tags = soup_detail.findAll("a")

                    m = re.compile(r'>(.*)</')
                    type_match = m.search(str(tags[0]))
                    busiType = type_match.group().replace(">", "").replace("</", "")
                    # row.businessType = busiType
                    # row.save()
                    print(busiType)
            else:
                print(row.id)

    def makeUrlString(self, code):
        url = 'https://finance.naver.com/item/main.nhn?code='
        url = url + code
        url = str(url.encode("euc-kr")).split('\'')[1]
        url = url.replace("\\x", "%")
        return url


if __name__ == '__main__':
    e = InfoData()
    e.getTypeData()
