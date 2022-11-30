# Generated by Django 4.0.3 on 2022-11-30 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0016_alter_user_orders_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_orders',
            name='razor_pay_trans_id',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='user_orders',
            name='status',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user_orders',
            name='time',
            field=models.TimeField(auto_now=True),
        ),
    ]