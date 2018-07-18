from django import setup
import os
import sys


if __name__ == "__main__":
    proj_path = "/Users/leeuram/2018Project/botwarehouse"
    sys.path.append(proj_path)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mirae.settings")
    setup()

from stock.models import *


class InfoData:

    def __init__(self):
        pass

    def getInfoData(self):
        print("asd")



if __name__ == '__main__':
    e = InfoData()
    e.getInfoData()
