# Generated by Django 2.2.1 on 2019-09-02 11:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20190902_1117'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='record',
            options={'ordering': ['-record_id'], 'verbose_name': '记录', 'verbose_name_plural': '记录'},
        ),
    ]
