# Generated by Django 3.2.2 on 2021-06-17 15:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0011_alter_detail_phieudkday_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subjects',
            name='ID_time',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_management_app.time_subject'),
        ),
    ]
