# Generated by Django 5.1.7 on 2025-05-02 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plans', '0005_rename_planday_day_rename_planweek_week'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriptionplan',
            name='level',
            field=models.CharField(choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced'), ('pro', 'Pro')], max_length=20),
        ),
    ]
