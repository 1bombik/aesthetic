# Generated by Django 4.1.7 on 2023-03-26 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, height_field='400', null=True, upload_to='product', width_field='400'),
        ),
    ]
