# Generated by Django 2.2.1 on 2019-09-07 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_auto_20190907_1636'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='session_id',
        ),
        migrations.AlterField(
            model_name='img',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]