# Generated by Django 4.0.4 on 2022-08-06 11:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stacks', '0014_remove_book_country_of_pub_book_country_of_pub'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='country_of_pub',
        ),
    ]
