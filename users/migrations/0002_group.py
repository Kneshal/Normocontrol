# Generated by Django 2.2 on 2021-02-23 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Введите название группы', max_length=200, verbose_name='Название группы')),
                ('slug', models.SlugField(help_text='Укажите адрес для страницы группы', unique=True, verbose_name='Slug-метка')),
            ],
        ),
    ]
