# Generated by Django 3.2.4 on 2021-07-01 20:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_alter_bookinstance_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookinstance',
            options={'ordering': ['due_back'], 'permissions': (('view_all', 'Can view all books'), ('manage_status', 'Can check out and renew books'))},
        ),
    ]
