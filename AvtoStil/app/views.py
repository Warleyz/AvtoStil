"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpRequest
from .forms import feedbackForm
from django.contrib.auth.forms import UserCreationForm
from django.db import models

from .models import Blog
from .forms import BlogForm

from .models import Catalog
from .models import Comment # использование модели комментариев
from .forms import CommentForm # использование формы ввода комментария

from .models import Order
from .models import OrderItem
from .models import Category
from .models import Status

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Главная',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Наши контакты',
            'message':'Страница с нашими контактами.',
            'year':datetime.now().year,
        }
    )

def feedback(request):
    assert isinstance(request, HttpRequest)
    data = None
    callback = {'1': 'По телефону', '2': 'По почте'}
    issue = {'1': 'Не хватает товаров в заказе',
             '2': 'Товар не соотвестует качеству',
             '3': 'Получить гарантийный талон или инструкцию',
             '4': 'Другой вопрос'}
    if request.method == 'POST':
        form = feedbackForm(request.POST)
        if form.is_valid():
            data = dict()
            data['name'] = form.cleaned_data['name']
            data['phone'] = form.cleaned_data['phone']
            data['city'] = form.cleaned_data['city']
            data['email'] = form.cleaned_data['email']
            data['message'] = form.cleaned_data['message']
            data['issue'] = issue[ form.cleaned_data['issue'] ]
            data['callback'] = callback[ form.cleaned_data['callback'] ]
            if (form.cleaned_data['notice'] == True):
                data['notice']='Да'
            else:
                data['notice']='Нет'
            form = None
    else:
        form = feedbackForm()
    return render(
        request,
        'app/feedback.html',
        {
            'title':'Обратная связь',
            'year':datetime.now().year,
            'form':form,
            'data':data
        }
    )

def registration(request):
    """Renders the registration page."""
    assert isinstance(request, HttpRequest)
    if request.method == "POST": # после отправки формы
        regform = UserCreationForm(request.POST)
        if regform.is_valid(): #валидация полей формы
            reg_f = regform.save(commit=False) # не сохраняем автоматически данные формы
            reg_f.is_staff = False # запрещен вход в административный раздел
            reg_f.is_active = True # активный пользователь
            reg_f.is_superuser = False # не является суперпользователем
            reg_f.date_joined = datetime.now() # дата регистрации
            reg_f.last_login = datetime.now() # дата последней авторизации
            reg_f.save() # сохраняем изменения после добавления данных
            return redirect('home') # переадресация на главную страницу после регистрации
    else:
        regform = UserCreationForm() # создание объекта формы для ввода данных нового пользователя
    return render(
        request,
        'app/registration.html',
        {
            'regform': regform, # передача формы в шаблон веб-страницы
            'year':datetime.now().year,
        }
    )

def blog(request):
    """Renders the blog page."""
    assert isinstance(request, HttpRequest)
    posts = Blog.objects.all() # запрос на выбор всех статей блога из модели
    return render(
        request,
        'app/blog.html',
        {
            'title':'Блог',
            'posts': posts, # передача списка статей в шаблон веб-страницы
            'year':datetime.now().year,
        }
    )

def blogpost(request, parametr):
    """Renders the blogpost page."""
    assert isinstance(request, HttpRequest)
    post_1 = Blog.objects.get(id=parametr) # запрос на выбор конкретной статьи по параметру
   
    return render(
        request,
        'app/blogpost.html',
        {
            'post_1': post_1, # передача конкретной статьи в шаблон веб-страницы
            'year':datetime.now().year,
        }
        
    )

def newpost(request):
    """Renders the newpost page."""
    assert isinstance(request, HttpRequest)
    
    if request.method == "POST":                            #после отправки формы
        blogform = BlogForm(request.POST, request.FILES)
        if blogform.is_valid():
            blog_f = blogform.save(commit=False)
            blog_f.posted = datetime.now()
            blog_f.author = request.user
            blog_f.save()                       # сохраняем изменения после добавления полей
            
            return redirect('blog')             # переадресация на страниу Блог после создания статьи Блога
    else:
        blogform = BlogForm()
        
    return render(
        request,
        'app/newpost.html',
        {
            'blogform': blogform,               # передача формы в шаблон веб-страницы
            'title': 'Добавить статью блога',
            
            'year': datetime.now().year,
        }
    )


def catalog(request, cat_id = 0):
    """Renders the category page."""
    assert isinstance(request, HttpRequest)
    categories = Category.objects.all() # запрос на выбор всех категорий товаров
    products = Catalog.objects.filter(category_id = cat_id) # запрос на выбор продуктов конкретной категории
    
    if len(products) == 0:
        products = Catalog.objects.all()
        
    return render(
        request,
        'app/catalog.html',
        {
            'title':'Меню',
            'categories':categories,
            'cat_selected':cat_id,
            'products':products,
            'year':datetime.now().year,
        }
    )   

def product(request, parametr):
    """Renders the product page."""
    assert isinstance(request, HttpRequest)
    product_1 = Catalog.objects.get(id=parametr) # запрос на выбор конкретной статьи по параметру
    comments = Comment.objects.filter(good=parametr)
    
    if request.method == "POST": # после отправки данных формы на сервер методом POST
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_f = form.save(commit=False)
            comment_f.author = request.user # добавляем (так как этого поля нет в форме) в модель Комментария (Comment) в поле автор авторизованного пользователя
            comment_f.date = datetime.now() # добавляем в модель Комментария (Comment) текущую дату
            comment_f.good = Catalog.objects.get(id=parametr) # добавляем в модель Комментария (Comment) статью, для которой данный комментарий
            comment_f.save() # сохраняем изменения после добавления полей
            return redirect('product', parametr=product_1.id) # переадресация на ту же страницу статьи после отправки комментария
    else:
        form = CommentForm() # создание формы для ввода комментария

    return render(
        request,
        'app/product.html',
        {
            'product_1': product_1,
            
            'comments': comments, # передача всех комментариев к данной статье в шаблон веб-страницы
            'form': form, # передача формы добавления комментария в шаблон веб-страницы

            'year':datetime.now().year,
        }
        
    )

def cart(request):
    """Renders the cart page."""
    current_order = Order.objects.filter(customer=request.user, order_status_id=1).first()
    if current_order == None:
        items = None
    else:
        items = OrderItem.objects.filter(order=current_order)
        
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/cart.html',
        {
            'title':'Ваша корзина',
            'order': current_order,
            'items': items,  
            'year':datetime.now().year,
        }
    )


def add_to_cart(request):
    current_product = Catalog.objects.filter(id = request.GET.get('product')).first()
    current_order, order_status_id = Order.objects.get_or_create(customer=request.user, order_status_id=1)
    if order_status_id:
        current_order.save()
    CartItem, order_status_id = OrderItem.objects.get_or_create(order=current_order, product=current_product)
    CartItem.quantity += 1
    CartItem.quantity_price = CartItem.product.price * CartItem.quantity
    CartItem.save()
    CartItem_list = OrderItem.objects.filter(order=current_order)
    current_order.total_price = 0
    for item in CartItem_list:
        current_order.total_price += item.quantity_price

    current_order.save()
    assert isinstance(request, HttpRequest)
    return redirect(reverse('catalog'))


def quantity_minus(request):
    current_item = OrderItem.objects.filter(id = request.GET.get('item')).first()
 
    current_item.quantity -= 1
    if current_item.quantity == 0:
        return redirect(reverse('delete_item', kwargs={'item': current_item.id}))
    else:

        current_item.quantity_price = current_item.product.price * current_item.quantity
        current_item.save()
    
        return redirect(reverse('total_price'))
    

def quantity_plus(request):
    current_item = OrderItem.objects.filter(id = request.GET.get('item')).first()
 
    current_item.quantity += 1
    current_item.quantity_price = current_item.product.price * current_item.quantity
    current_item.save()
    
    return redirect(reverse('total_price'))


def total_price(request):
    current_order, order_status_id = Order.objects.get_or_create(customer=request.user, order_status_id=1)
    order_list = OrderItem.objects.filter(order=current_order)
    current_order.total_price = 0
    for item in order_list:
        current_order.total_price += item.quantity_price

    current_order.save()
    return redirect(reverse('cart'))

def delete_item(request, item):
    current_item = OrderItem.objects.get(id = item).delete()
    return redirect(reverse('total_price'))


def deal_order(request):
    current_order = Order.objects.filter(customer=request.user, order_status_id=1).first()
    current_order.order_status_id = 2
    current_order.save()
    
    return redirect(reverse('myorders'))


def myorders(request):
    """Renders the myorders page."""
    current_orders = Order.objects.filter(customer=request.user).exclude(order_status_id=1)
        
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/myorders.html',
        {
            'title':'Мои заказы',
            'items': current_orders, 
            'year':datetime.now().year,
        }
    ) 


def ordersmanage(request):
    """Renders the ordersmanage page."""
    all_orders = Order.objects.all().exclude(order_status_id=1)
    all_statuses = Status.objects.all().exclude(id=1)
        
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/ordersmanage.html',
        {
            'title':'Список заказов клиентов',
            'items': all_orders,
            'statuses': all_statuses,
            'year':datetime.now().year,
        }
    ) 


def orderdetails(request, order):
    """Renders the order page."""
    current_order = Order.objects.get(id = order)
    items = OrderItem.objects.filter(order=current_order)
        
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/orderdetails.html',
        {
            'title':'Заказ',
            'order': current_order,
            'items': items,  
            'year':datetime.now().year,
        }
    ) 


def quantity_minus_order(request):
    current_item = OrderItem.objects.filter(id = request.GET.get('item')).first()
    current_order = request.GET.get('order')
    current_item.quantity -= 1
    current_item.quantity_price = current_item.product.price * current_item.quantity
    current_item.save()
    
    return redirect(reverse('total_price_order', kwargs={'order': current_order}))


def quantity_plus_order(request):
    current_item = OrderItem.objects.filter(id = request.GET.get('item')).first()
    current_order = request.GET.get('order')
    current_item.quantity += 1
    current_item.quantity_price = current_item.product.price * current_item.quantity
    current_item.save()
    
    return redirect(reverse('total_price_order', kwargs={'order': current_order}))


def total_price_order(request, order):
    order_list = OrderItem.objects.filter(order=order)
    current_order = Order.objects.get(id=order)
    current_order.total_price = 0
    for item in order_list:
        current_order.total_price += item.quantity_price

    current_order.save()
    return redirect(reverse('orderdetails', kwargs={'order': order}))


def switch_status_order(request):
    current_status = Status.objects.filter(id = request.GET.get('status')).first()
    current_order = Order.objects.filter(id = request.GET.get('order')).first()
    current_order.order_status = current_status
    current_order.save()
    return redirect(reverse('ordersmanage'))


def order_cancel_cust(request, item):
    # Order.objects.get(id = item).delete()
    cancel_status = Status.objects.get(id=8)
    current_order = Order.objects.get(id = item)
    current_order.order_status = cancel_status
    current_order.save()
    return redirect(reverse('myorders'))

def order_cancel_man(request, item):
    # Order.objects.get(id = item).delete()
    cancel_status = Status.objects.get(id=8)
    current_order = Order.objects.get(id = item)
    current_order.order_status = cancel_status
    current_order.save()
    return redirect(reverse('ordersmanage'))