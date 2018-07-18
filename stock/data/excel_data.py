import openpyxl
import os
from django import setup
import datetime
import sys

if __name__ == "__main__":
    proj_path = "/Users/woong/Documents/mirae"
    sys.path.append(proj_path)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mirae.settings")
    setup()

from stock.models import *

dir = os.path.dirname(__file__)
'''
excel insert
'''

class ExcelData:

    def __init__(self):
        pass

    def getExcelData(self):
        excel_document = openpyxl.load_workbook(os.path.join(dir, 'stock02.xlsx'))
        sheet_name = excel_document.sheetnames[0]
        sheet = excel_document[sheet_name]

        # 모든 열
        all_rows = list(sheet.rows)
        for idx in range(len(all_rows)):
            if idx == 0:
                continue
            row=all_rows[idx]
            stock = Stock.objects.filter(name=row[0].value).first()
            if stock is None:
                stock = Stock(name=row[0].value)
                stock.save()
            s_datetime = datetime.datetime.strptime(str(row[1].value), '%Y%m%d')
            stock_data_chk = Stock_Data.objects.filter(stock=stock, date=s_datetime).first()
            if stock_data_chk is None:
                stock_data = Stock_Data(stock=stock, date=s_datetime, start=row[2].value, highest=row[3].value,
                                        lowest=row[4].value, close=row[5].value, volume=row[6].value)
                stock_data.save()
                print(stock_data.id)
            else:
                print("continue")

        # Stock_Data.objects.all().delete()



if __name__ == '__main__':
    e = ExcelData()
    e.getExcelData()
