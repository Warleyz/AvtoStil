# Generated by Django 4.2.8 on 2023-12-13 03:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_blog_posted_alter_catalog_short_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='posted',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2023, 12, 13, 6, 20, 0, 309271), verbose_name='Опубликована'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2023, 12, 13, 6, 20, 0, 310272), verbose_name='Дата заказа'),
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
