# Generated by Django 2.2.2 on 2019-07-05 11:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_category_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='discount',
            name='date',
        ),
    ]
