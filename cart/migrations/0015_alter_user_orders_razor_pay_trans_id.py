# Generated by Django 4.0.3 on 2022-11-30 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0014_user_orders_razor_pay_trans_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_orders',
            name='razor_pay_trans_id',
            field=models.CharField(max_length=500),
        ),
    ]
