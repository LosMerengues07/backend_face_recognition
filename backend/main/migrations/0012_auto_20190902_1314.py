# Generated by Django 2.2.1 on 2019-09-02 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_auto_20190902_1313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='time',
            field=models.CharField(max_length=64),
        ),
    ]
