# Generated by Django 2.2.1 on 2019-09-02 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20190902_1304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='time',
            field=models.CharField(max_length=64),
        ),
    ]
