# Generated by Django 3.2.2 on 2021-06-17 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0007_auto_20210617_1353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nhom_th',
            name='startday_TH',
            field=models.DateField(auto_now=True),
        ),
    ]
