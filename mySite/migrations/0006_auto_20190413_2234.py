# Generated by Django 2.1.7 on 2019-04-13 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mySite', '0005_auto_20190413_2224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='name',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]