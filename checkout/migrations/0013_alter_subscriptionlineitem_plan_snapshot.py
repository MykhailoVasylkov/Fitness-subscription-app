# Generated by Django 5.1.7 on 2025-05-19 16:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0012_alter_subscriptionlineitem_plan_snapshot'),
        ('plans', '0010_daysnapshot_daycontentitemsnapshot_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriptionlineitem',
            name='plan_snapshot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plans.subscriptionplansnapshot'),
        ),
    ]
