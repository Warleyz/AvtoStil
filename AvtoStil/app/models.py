"""
Definition of models.
"""

from django.db import models
from django.contrib import admin
from datetime import datetime
from django.forms.fields import DateTimeField
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

class Blog(models.Model):
    author = models.ForeignKey(User, null=True, blank=True, on_delete = models.SET_NULL, verbose_name = "Автор")
    title = models.CharField(max_length = 100, unique_for_date = "posted", verbose_name= "Заголовок")
    description = models.TextField(verbose_name = "Краткое содержание")
    content = models.TextField(verbose_name = "Полное содержание")
    posted = models.DateTimeField(default = datetime.now(), db_index = True, verbose_name = "Опубликована")
    image = models.FileField(default = 'temp.jpg', verbose_name="Путь к картинке")
    
    #Методы класса
    def get_absolute_url(self):
        return reverse("blogpost", args=[str(self.id)]) # Метод возарщает строку с URL-адресом записи
    
    def __str__(self):
        return self.title # Метод возвращает название, используемое для представления отдельных записей в административном разделе
    
    # Метаданные - вложенный класс, который задает дополнительные параметры модели:
    class Meta:
        db_table = "Posts"                      # Имя таблицы для модели
        ordering = ["-posted"]                  # Порядок сортировки данных в модели ( "-" означает убывание)  
        verbose_name = "статья блога"           # Имя, под которым модель будет отображаться административном разделе (для одной статьи блога)
        verbose_name_plural = "статьи блога"    # Тоже для всех статей блога     
admin.site.register(Blog)


class Category(models.Model):
	name = models.CharField(verbose_name = 'Категория товаров', max_length=50)
	
	def get_absolute_url(self):
		return reverse("catalog", args=[str(self.id)])

	def __str__(self):
		return self.name

	class Meta:
		db_table = 'Categories'
		ordering = ['id']
		verbose_name = 'Категория товара'
		verbose_name_plural = 'Категории товаров'
admin.site.register(Category)


class Status(models.Model):
	name = models.CharField(verbose_name = 'Статус заказа', max_length=50)
	
	def get_absolute_url(self):
		return reverse("statuses", args=[str(self.id)])

	def __str__(self):
		return self.name

	class Meta:
		db_table = 'Statuses'
		ordering = ['id']
		verbose_name = 'Статус заказа'
		verbose_name_plural = 'Статусы заказа'
admin.site.register(Status)


class Catalog(models.Model):
	name = models.TextField(verbose_name = 'Название товара', max_length = 200)
	short_description = models.TextField(verbose_name = 'Краткое описание', max_length = 500)
	description = models.TextField(verbose_name = 'Описание товара', max_length = 2000)
	price = models.DecimalField(verbose_name = 'Стоимость', max_digits=8, decimal_places=2)
	category = models.ForeignKey(Category, on_delete = models.CASCADE, verbose_name = 'Категория товара')
	image = models.FileField(default = 'temp.jpg', verbose_name = 'Путь к картинке')

	def get_absolute_url(self):
		return reverse("catalog", args=[str(self.id)])

	def __str__(self):
		return 'Товар %s: %s' % (self.id, self.name)

	class Meta:
		db_table = 'Catalog'
		ordering = ['id']
		verbose_name = 'Товар'
		verbose_name_plural = 'Товары'
admin.site.register(Catalog)

class Comment(models.Model):
    text = models.TextField(verbose_name = "Текст комментария")
    date = models.DateTimeField(default = datetime.now(), db_index = True, verbose_name = "Дата комментария")
    author = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = "Автор комментария")
    good = models.ForeignKey(Catalog, on_delete = models.CASCADE, verbose_name = "Товар комментария")
    
    # Методы класса
    def __str__(self): # Метод возвращает название, используемое для представления отдельных записей в административном разделе
        return 'Комментарий %d %s к %s' % (self.id, self.author, self.good)
    
    # Метаданные - вложенный класс, который задаёт дополнительные параметры модели:
    class Meta:
        db_table = "Comment"
        ordering = ["-date"]
        verbose_name = "Комментарии к товару"
        verbose_name_plural = "Комментраии к товарам"
        
admin.site.register(Comment)


class Order(models.Model):
	customer = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = 'Покупатель')
	order_date = models.DateTimeField(default= datetime.now(), db_index=True, verbose_name= "Дата заказа")
	order_status = models.ForeignKey(Status, on_delete = models.CASCADE, verbose_name = 'Статус заказа')
	total_price = models.DecimalField(default = 0, max_digits=8, verbose_name = 'Итоговая стоимость', decimal_places=2)

	def __str__(self):
		return 'Заказ %s ' % (self.id)

	class Meta:
		db_table = 'Orders'
		ordering = ['order_date']
		verbose_name = 'Заказ'
		verbose_name_plural = 'Заказы'  
admin.site.register(Order)
		

class OrderItem(models.Model):
	order = models.ForeignKey(Order, on_delete = models.CASCADE, verbose_name = 'Заказ')
	product = models.ForeignKey(Catalog, on_delete = models.CASCADE, verbose_name = 'Товар')
	quantity = models.IntegerField(default = 0, verbose_name = 'Количество товара')
	quantity_price = models.DecimalField(default = 0, max_digits=8, decimal_places=2, verbose_name = 'Суммарная стоимость товара')
	

	def __str__(self):
		return 'Товар %s к заказу %s' % (self.product, self.order)

	class Meta:
		db_table = 'OrderItems'
		ordering = ['order']
		verbose_name = 'Товар заказа'
		verbose_name_plural = 'Товары заказа'
admin.site.register(OrderItem)