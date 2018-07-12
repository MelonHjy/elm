from django.shortcuts import render, redirect
from .models import Img, Restaurant, Food, User, Cart
from .forms.login import LoginForm, registerForm
import time, random, os
from django.conf import settings
from django.contrib.auth import logout
from django.http import JsonResponse


# Create your views here.


def home(request):
    try:
        del request.session['rest']
    except KeyError as e:
        pass
    wheelsList = Img.wheel.all()
    navList = Img.nav.all()
    restList = Restaurant.objects.all()
    return render(request, 'elm/home.html',
                  {'title': '饿了么', 'wheelsList': wheelsList, 'navList': navList, 'restList': restList})


def market(request):
    iconList = Img.icon.all()
    one = iconList[0]
    two = iconList[1]
    three = iconList[2]
    four = iconList[3]
    five = iconList[4]
    cheapList = iconList[5:]
    return render(request, 'elm/market.html', {'title': '发现', 'one': one, 'two': two,
                                               'three': three, 'four': four, 'five': five, 'cheapList': cheapList})


def cart(request):
    user = request.session.get('user')
    if user is None:
        loginImg = Img.login.get()
        return render(request, 'elm/cart.html', {'title': '订单', 'login': loginImg})
    # 筛选该账户的所有食物
    foodList = Cart.objects.filter(account=user.account)
    # 找出所有orderid
    orderidList = []
    for cart in foodList:
        if cart.orderid not in orderidList:
            orderidList.append(cart.orderid)
    # 把orderid相同的订单放在一起
    L = []
    for orderid in orderidList:
        oneOrder = foodList.filter(orderid=orderid)
        L.append(oneOrder)
    print(L)
    # [<QuerySet [<Cart: Cart object>]>, <QuerySet [<Cart: Cart object>, <Cart: Cart object>]>]
    return render(request, 'elm/cart.html', {'title': '订单', 'L': L})


def checkout(request):
    # ajax
    if request.method == 'POST':
        ga = request.POST.get('ga')
        food = Food.objects.get(id=ga)
        if request.POST.get('method') == 'add':
            # 如果session没有该餐厅
            if request.session.get(food.restaurant) is None:
                request.session[food.restaurant] = {food.id: 1, 'money': food.money}
                return JsonResponse({'num': '1', 'money': str(food.money)})
            # 有该餐厅(一定有money)，判断有无该food
            num = request.session.get(food.restaurant).get(food.id, 0)
            money = request.session.get(food.restaurant).get('money')
            num += 1
            money = money + food.money
            request.session[food.restaurant][food.id] = num
            request.session[food.restaurant]['money'] = money
            request.session.modified = True
            return JsonResponse({'num': str(num), 'money': str(money)})
        elif request.POST.get('method') == 'remove':
            num = request.session.get(food.restaurant).get(food.id)
            money = request.session.get(food.restaurant).get('money')
            num -= 1
            money = money - food.money
            request.session[food.restaurant][food.id] = num
            request.session[food.restaurant]['money'] = money
            request.session.modified = True
            return JsonResponse({'num': str(num), 'money': str(money)})
    # 按'去结算'后
    user = request.session.get('user')
    if user is None:
        return redirect('/login/')
    restaurant = request.session.get('rest')
    money = request.session.get(restaurant).get('money')
    return render(request, 'elm/checkout.html', {'title': '确认订单', 'user': user,
                                                 'url_id': restaurant.url_id, 'money': money})


def pay(request):
    # 按去支付后，创建Cart实例
    user = request.session.get('user')
    restaurant = request.session.get('rest')
    foodList = request.session.get(restaurant)
    foodList.pop('money')
    orderid = str(time.time()+random.randrange(1, 10000))
    for food_id in foodList:
        account = user.account
        num = foodList[food_id]
        f = Food.objects.get(id=food_id)
        c = Cart.objects.create(account=account, food=f.name, num=num, money=f.money,
                                restaurant=restaurant.name, orderid=orderid, progress='订单待支付')
        c.save()
    return render(request, 'elm/pay.html', {'title': '支付'})


def mine(request):
    user = request.session.get('user', None)
    return render(request, 'elm/mine.html', {'title': '我的', 'user': user})


def food(request, url_id):
    restaurant = Restaurant.objects.get(url_id=url_id)
    try:
        del request.session[restaurant]
    except KeyError as e:
        pass
    request.session['rest'] = restaurant
    foodList = restaurant.food_set.all()
    typeList = []
    for food in foodList:
        if food.type not in typeList:
            typeList.append(food.type)
    L = []
    for type in typeList:
        L.append(restaurant.food_set.filter(type=type))
    return render(request, 'elm/food.html', {'restaurant': restaurant, 'L': L, 'typeList': typeList})


def login(request):
    if request.method == 'POST':
        f = LoginForm(request.POST)
        if f.is_valid():
            account = f.cleaned_data["account"]
            pswd = f.cleaned_data["passwd"]
            try:
                user = User.objects.get(account=account)
                if user.pswd != pswd:
                    return redirect('/login/')
            except User.DoesNotExist as e:
                return redirect('/login/')
            # 登录成功
            user.token = str(time.time() + random.randrange(1, 10000))
            user.save()
            request.session["user"] = user
            if request.session.get('rest'):
                return redirect('/checkout/')
            return redirect('/mine/')
        else:
            return render(request, 'elm/login.html', {'title': '登录', 'form': f, 'error': f.errors})
    else:
        f = LoginForm()
        return render(request, 'elm/login.html', {'title': '登录', 'form': f})


def register(request):
    if request.method == 'POST':
        f = registerForm(request.POST, request.FILES)
        if f.is_valid():
            account = f.cleaned_data["account"]
            pswd = f.cleaned_data["passwd"]
            name = f.cleaned_data['name']
            tel = f.cleaned_data["tel"]
            token = str(time.time() + random.randrange(1, 10000))
            img = r'/static/mine/img/默认.png'
            if request.FILES.get('img'):
                path = os.path.join(settings.MEDIA_ROOT, account + '.png')
                img = settings.MEDIA_URL + account + '.png'
                with open(path, 'wb') as fp:
                    for chunk in request.FILES.get('img').chunks():
                        fp.write(chunk)
            user = User.objects.create(account=account, pswd=pswd, name=name, tel=tel, img=img, token=token)
            request.session["user"] = user
            return redirect('/mine/')
        else:
            return render(request, 'elm/register.html', {'title': '注册', 'form': f, 'error': f.errors})
    else:
        f = registerForm()
        return render(request, 'elm/register.html', {'title': '注册', 'form': f})


def checkaccount(request):
    acc = request.POST.get('acc')
    try:
        user = User.objects.get(account=acc)
        return JsonResponse({'message': '用户已被注册', 'status': 'error'})
    except User.DoesNotExist as e:
        return JsonResponse({'status': 'success'})


def quit(request):
    logout(request)
    return redirect('/mine/')
