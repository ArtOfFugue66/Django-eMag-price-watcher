# Generated by Django 3.2.5 on 2021-07-30 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0003_scrape'),
    ]

    operations = [
        migrations.AddField(
            model_name='scrape',
            name='time',
            field=models.TimeField(default=None),
        ),
    ]
