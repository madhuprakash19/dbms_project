# Generated by Django 3.2 on 2021-12-05 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0005_alter_department_hod'),
    ]

    operations = [
        migrations.AlterField(
            model_name='designation',
            name='name',
            field=models.CharField(max_length=30),
        ),
    ]
