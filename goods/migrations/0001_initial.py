# Generated by Django 4.1.7 on 2023-03-26 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('image', models.ImageField(blank=True, height_field=400, null=True, upload_to='product', width_field=400)),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
    ]