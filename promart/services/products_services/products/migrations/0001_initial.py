# Generated by Django 5.2 on 2025-04-11 19:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Name')),
                ('icon', models.FileField(blank=True, null=True, upload_to='categories/%Y/%m/%d/', verbose_name='Image')),
                ('order', models.IntegerField(blank=True, default=None, null=True, verbose_name='Order')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active')),
                ('super_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subcategories', related_query_name='subcategory', to='products.category', verbose_name='Main category')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'ordering': ['order'],
                'unique_together': {('super_category', 'order')},
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('description', models.TextField(blank=True, max_length=1000, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('image', models.ImageField(blank=True, null=True, upload_to='products/')),
                ('stock', models.PositiveIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('status', models.CharField(choices=[('active', 'Active'), ('pending', 'Pending'), ('sold_out', 'Sold Out'), ('inactive', 'Inactive')], default='inactive', max_length=20)),
                ('create_at', models.DateTimeField(auto_now=True)),
                ('expire_at', models.DateTimeField()),
                ('category', models.ManyToManyField(to='products.category')),
            ],
        ),
    ]
