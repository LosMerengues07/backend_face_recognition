# Generated by Django 2.2.1 on 2019-09-02 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_auto_20190902_1359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='record_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
