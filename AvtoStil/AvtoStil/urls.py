"""
Definition of urls for AvtoStil.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('feedback/', views.feedback, name='feedback'),
    path('blog/', views.blog, name='blog'),
    path('blogpost/<int:parametr>/', views.blogpost, name='blogpost'),
    path('newpost/', views.newpost, name='newpost'),
    path('registration/', views.registration, name='registration'),
    path('login/',
         LoginView.as_view
         (
             template_name='app/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Авторизация',
                 'year' : datetime.now().year,
             }
         ),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls),

    path('catalog/', views.catalog, name='catalog'),
    path('catalog/<int:cat_id>', views.catalog, name='catalog'),
    
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('quantity_minus/', views.quantity_minus, name='quantity_minus'),
    path('quantity_plus/', views.quantity_plus, name='quantity_plus'),
    path(r'delete_item/(?P<item>[0-9]+)/', views.delete_item, name='delete_item'),
    path('total_price/', views.total_price, name='total_price'),
    path('deal_order/', views.deal_order, name='deal_order'),
    
    path('myorders/', views.myorders, name='myorders'),
    path(r'orderdetails/(?P<order>[0-9]+)/', views.orderdetails, name='orderdetails'),
    path(r'order_cancel_cust/(?P<item>[0-9]+)/', views.order_cancel_cust, name='order_cancel_cust'),
    path(r'order_cancel_man/(?P<item>[0-9]+)/', views.order_cancel_man, name='order_cancel_man'),

    path('quantity_minus_order/', views.quantity_minus_order, name='quantity_minus_order'),
    path('quantity_plus_order/', views.quantity_plus_order, name='quantity_plus_order'),
    path(r'total_price_order/(?P<order>[0-9]+)/', views.total_price_order, name='total_price_order'),
    path(r'switch_status_order/', views.switch_status_order, name='switch_status_order'),
    path('ordersmanage/', views.ordersmanage, name='ordersmanage'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()