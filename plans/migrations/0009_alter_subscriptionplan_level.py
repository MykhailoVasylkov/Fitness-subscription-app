# Generated by Django 5.1.7 on 2025-05-05 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plans', '0008_alter_subscriptionplan_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriptionplan',
            name='level',
            field=models.IntegerField(choices=[(1, 'Beginner'), (2, 'Intermediate'), (3, 'Advanced'), (4, 'Pro')]),
        ),
    ]
