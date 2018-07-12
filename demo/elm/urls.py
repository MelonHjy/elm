from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^home/$', views.home, name='home'),
    url(r'^market/$', views.market, name='market'),
    url(r'^cart/$', views.cart, name='cart'),
    url(r'^mine/$', views.mine, name='mine'),
    url(r'^food/(\d+)/$', views.food, name='food'),
    url(r'^login/$', views.login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^quit/$', views.quit, name='quit'),
    url(r'^checkaccount/$', views.checkaccount, name='checkaccount'),
    url(r'^checkout/$', views.checkout, name='checkout'),
    url(r'^pay/$', views.pay, name='pay'),
]
