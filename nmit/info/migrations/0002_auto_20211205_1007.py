# Generated by Django 3.2 on 2021-12-05 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='hostel',
            name='type',
            field=models.CharField(default='BOYS', max_length=10),
        ),
        migrations.AlterField(
            model_name='hostel',
            name='name',
            field=models.CharField(max_length=20),
        ),
    ]
