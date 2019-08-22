# Generated by Django 2.1 on 2019-07-29 14:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('typeid', models.IntegerField()),
                ('goods', models.CharField(max_length=32)),
                ('company', models.CharField(max_length=50)),
                ('content', models.TextField()),
                ('price', models.FloatField()),
                ('picname', models.CharField(max_length=255)),
                ('store', models.IntegerField(default=0)),
                ('num', models.IntegerField(default=0)),
                ('clicknum', models.IntegerField(default=0)),
                ('state', models.IntegerField(default=1)),
                ('addtime', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
                'db_table': 'goods',
            },
        ),
        migrations.CreateModel(
            name='Types',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('pid', models.IntegerField(default=0)),
                ('path', models.CharField(max_length=32)),
            ],
            options={
                'db_table': 'types',
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=32)),
                ('sex', models.IntegerField(default=1)),
                ('address', models.CharField(max_length=32)),
                ('code', models.CharField(max_length=6)),
                ('phone', models.CharField(max_length=32)),
                ('email', models.CharField(max_length=32)),
                ('state', models.IntegerField(default=1)),
                ('addtime', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
                'db_table': 'users',
            },
        ),
    ]