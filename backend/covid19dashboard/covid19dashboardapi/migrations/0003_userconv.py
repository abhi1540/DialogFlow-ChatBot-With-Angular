# Generated by Django 2.2.12 on 2020-04-16 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('covid19dashboardapi', '0002_auto_20200411_1531'),
    ]

    operations = [
        migrations.CreateModel(
            name='Userconv',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session', models.CharField(max_length=500)),
                ('userconv', models.CharField(max_length=1000)),
                ('botconv', models.CharField(max_length=1000)),
                ('date', models.DateTimeField()),
            ],
        ),
    ]
