# Generated by Django 3.2.2 on 2021-06-17 15:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0012_alter_subjects_id_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subjects',
            name='MAGV',
        ),
    ]
