# Generated by Django 5.0.4 on 2024-05-23 04:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ewp', '0004_profile_doctor_type_profile_user_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doctor_type', models.CharField(blank=True, max_length=100, null=True)),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='ewp.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='ewp.profile')),
            ],
        ),
    ]