from django.db import models
from datetime import date

# Create your models here.
class Stock(models.Model):
    name = models.CharField(max_length=64)
    code = models.CharField(max_length=64)
    businessType = models.CharField(max_length=250, null=True)


class Stock_Data(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    date = models.DateField()
    start = models.IntegerField()
    highest = models.IntegerField()
    lowest = models.IntegerField()
    close = models.IntegerField()
    volume = models.IntegerField()
    amount_money = models.IntegerField()
    amount_stock = models.IntegerField()

class Indicator_Rsi(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    date = models.DateField()
    type = models.CharField(max_length=3)
    price = models.IntegerField()

    class Meta:
        unique_together = (("stock", "date",),)

class Indicator_Macd(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    date = models.DateField()
    type = models.CharField(max_length=3)
    price = models.IntegerField()

    class Meta:
        unique_together = (("stock", "date",),)

class Indicator_Wr(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    date = models.DateField()
    type = models.CharField(max_length=3)
    price = models.IntegerField()

    class Meta:
        unique_together = (("stock", "date",),)

class Indicator_Cross(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    date = models.DateField()
    type = models.CharField(max_length=3)
    price = models.IntegerField()

    class Meta:
        unique_together = (("stock", "date",),)


class Indicator_Result(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    indicator = models.CharField(max_length=128)
    profit = models.FloatField()
    stock_count = models.IntegerField()
    last_price = models.IntegerField()
    current_price = models.IntegerField()

class Indicator_Sensitive(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    sensitive = models.CharField(max_length=256)

class User(models.Model):
    naver_id = models.CharField(max_length=128)
    fb_id = models.CharField(max_length=128, null=True)
    charged_yn = models.CharField(max_length=10, default='n')

class User_stock(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)

class Stock_News(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    title = models.CharField(max_length=512, null=True)
    link = models.CharField(max_length=512)

    class Meta:
        unique_together = (("stock", "link",),)