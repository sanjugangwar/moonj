# Generated by Django 4.0.3 on 2022-11-30 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0009_registration_path_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registration',
            name='path_token',
            field=models.CharField(max_length=100),
        ),
    ]
