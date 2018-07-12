from django.contrib import admin
from .models import Restaurant, Food, User, Cart
# Register your models here.


# 关联对象：在创建一个餐厅时可直接添加食物
class FoodInfo(admin.TabularInline):
    model = Food
    extra = 5


@admin.register(Restaurant)
class RestAdmin(admin.ModelAdmin):
    inlines = [FoodInfo]
    # 列表页属性
    list_display = ['pk', 'img', 'name', 'url_id', 'star', 'month_sell', 'start_send', 'send_money' ]


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ['pk', 'img', 'restaurant', 'name', 'money',  'type']
    # 过滤器
    list_filter = ['restaurant']
    # 搜索字段
    search_fields = ['restaurant']
    # 分页
    list_per_page = 20


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['pk', 'account', 'pswd', 'name', 'tel', 'img', 'token']
    list_per_page = 20


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['pk', 'account', 'food', 'num', 'money',  'restaurant', 'orderid', 'progress']
    list_filter = ['account', 'orderid', 'progress']
    search_fields = ['account','orderid']
    list_per_page = 20
    # 添加、修改页属性
    fieldsets = [
        ('base', {'fields': ['account', 'restaurant', 'orderid', 'progress']}),
        ('food', {'fields': ['food', 'num', 'money']})
    ]

