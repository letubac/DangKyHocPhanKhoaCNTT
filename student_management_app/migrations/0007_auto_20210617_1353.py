# Generated by Django 3.2.2 on 2021-06-17 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0006_auto_20210616_0657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nhom_th',
            name='endday_TH',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='thuchanh',
            name='MATH',
            field=models.CharField(max_length=30, primary_key=True, serialize=False),
        ),
    ]