# Generated by Django 5.0.4 on 2024-05-23 04:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ewp', '0005_doctor_patient'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='doctor_type',
        ),
    ]