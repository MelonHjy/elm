from django.db import models
# Create your models here.


class WheelManager(models.Manager):
    def get_queryset(self):
        return super(WheelManager, self).get_queryset().filter(type='wheel')


class NavManager(models.Manager):
    def get_queryset(self):
        return super(NavManager, self).get_queryset().filter(type='nav')


class IconManager(models.Manager):
    def get_queryset(self):
        return super(IconManager, self).get_queryset().filter(type='icon')


class LoginManager(models.Manager):
    def get_queryset(self):
        return super(LoginManager, self).get_queryset().filter(type='login')


class Img(models.Model):
    img = models.CharField(max_length=150)
    name = models.CharField(max_length=20)
    url_id = models.IntegerField()
    type = models.CharField(max_length=10)
    wheel = WheelManager()
    nav = NavManager()
    icon = IconManager()
    login = LoginManager()

    def __str__(self):
        return self.name


class Restaurant(models.Model):
    img = models.CharField(max_length=150)
    name = models.CharField(max_length=20)
    url_id = models.IntegerField()
    star = models.DecimalField(max_digits=2, decimal_places=1)
    month_sell = models.IntegerField()
    start_send = models.IntegerField()
    send_money = models.IntegerField()

    def __str__(self):
        return self.name


class Food(models.Model):
    img = models.CharField(max_length=150)
    restaurant = models.ForeignKey('Restaurant')
    name = models.CharField(max_length=20)
    money = models.IntegerField()
    type = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class User(models.Model):
    account = models.CharField(max_length=20)
    pswd = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    tel = models.CharField(max_length=20)
    img = models.CharField(max_length=150)
    token = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# 购物车表
class Cart(models.Model):
    account = models.CharField(max_length=20)
    food = models.CharField(max_length=20)
    num = models.CharField(max_length=20)
    money = models.IntegerField()
    restaurant = models.CharField(max_length=50)
    orderid = models.CharField(max_length=50)
    progress = models.CharField(max_length=20)




