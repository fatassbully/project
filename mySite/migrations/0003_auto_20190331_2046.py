# Generated by Django 2.1.7 on 2019-03-31 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mySite', '0002_auto_20190331_2029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='comment',
            field=models.ManyToManyField(blank=True, related_name='attachment', to='mySite.Comment'),
        ),
        migrations.AlterField(
            model_name='attachment',
            name='post',
            field=models.ManyToManyField(blank=True, related_name='attachment', to='mySite.Post'),
        ),
    ]
