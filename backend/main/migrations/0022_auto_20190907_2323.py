# Generated by Django 2.2.1 on 2019-09-07 23:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0021_delete_record'),
    ]

    operations = [
        migrations.RenameField(
            model_name='img',
            old_name='id',
            new_name='img_id',
        ),
    ]
