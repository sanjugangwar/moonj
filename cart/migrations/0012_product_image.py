# Generated by Django 4.0.3 on 2022-11-28 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0011_remove_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(null=True, upload_to='myimage'),
        ),
    ]
