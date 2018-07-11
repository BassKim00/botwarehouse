#!/usr/bin/env python
import openpyxl
import os
import django
import datetime

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mirae.settings")
    django.setup()

from stock.models import *

'''
excel insert
'''

class ExcelData:

    def __init__(self):
        pass

    def getExcelData(self):
        excel_document = openpyxl.load_workbook('stock.xlsx')
        sheet_name = excel_document.sheetnames[0]
        sheet = excel_document[sheet_name]

        # 모든 열
        all_rows = list(sheet.rows)
        for idx in range(len(all_rows)):
            if idx ==0:
                continue
            row=all_rows[idx]
            stock = Stock.objects.filter(name=row[0].value).first()
            if stock is None:
                stock = Stock(name=row[0].value)
                stock.save()
            s_datetime = datetime.datetime.strptime(str(row[1].value), '%Y%m%d')

            stock_data = Stock_Data(stock=stock, date=s_datetime, start=row[2].value, highest=row[3].value,
                                    lowest=row[4].value, close=row[5].value, volume=row[6].value,
                                    amount_money=row[7].value, amount_stock=row[8].value)
            stock_data.save()
            print(stock_data.id)

        # Stock_Data.objects.all().delete()



if __name__ == '__main__':
    e = ExcelData()
    e.getExcelData()
