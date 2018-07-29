from django.db import models

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

class Indicator_Result(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    indicator = models.CharField(max_length=128)
    profit = models.FloatField()

