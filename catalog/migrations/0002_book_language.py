# Generated by Django 3.2.4 on 2021-06-29 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='language',
            field=models.CharField(blank=True, default='English', max_length=50),
        ),
    ]
