# Generated by Django 3.2.4 on 2021-06-29 21:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_book_published'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookinstance',
            name='imprint',
        ),
    ]
