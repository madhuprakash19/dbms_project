# Generated by Django 3.2 on 2021-12-19 05:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('info', '0007_faculty_student_details_student_hostel'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='class_member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='student_class',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sem', models.CharField(blank=True, max_length=10, null=True)),
                ('section', models.CharField(blank=True, max_length=10, null=True)),
                ('academic_year', models.IntegerField(blank=True, null=True)),
                ('is_active', models.BooleanField(blank=True, null=True)),
                ('dept_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='info.department')),
                ('students', models.ManyToManyField(through='academic.class_member', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('code', models.CharField(blank=True, max_length=10, null=True)),
                ('description', models.CharField(blank=True, max_length=50, null=True)),
                ('dept_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='info.department')),
            ],
        ),
        migrations.CreateModel(
            name='subject_student_enrollment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='adm_no', to=settings.AUTH_USER_MODEL)),
                ('subject_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='academic.subject')),
            ],
        ),
        migrations.CreateModel(
            name='subject_handler',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField()),
                ('class_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='clas_id', to='academic.student_class')),
                ('faculty_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('subject_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='academic.subject')),
            ],
        ),
        migrations.AddField(
            model_name='class_member',
            name='class_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='academic.student_class'),
        ),
        migrations.AddField(
            model_name='class_member',
            name='student',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]