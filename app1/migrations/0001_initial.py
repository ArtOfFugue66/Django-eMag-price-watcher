# Generated by Django 3.2.5 on 2021-07-28 14:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WatchItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('url', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Scrape',
            fields=[
                ('watchitem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app1.watchitem')),
                ('price', models.PositiveIntegerField()),
                ('date', models.DateTimeField()),
            ],
            bases=('app1.watchitem',),
        ),
    ]
