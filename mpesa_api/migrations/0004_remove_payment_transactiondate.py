# Generated by Django 2.2 on 2021-08-17 16:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mpesa_api', '0003_auto_20210817_1934'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='transactionDate',
        ),
    ]