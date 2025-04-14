# Generated by Django 5.1.7 on 2025-04-14 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DeliverySettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('free_delivery_threshold', models.DecimalField(decimal_places=2, default=50, max_digits=6)),
                ('standard_delivery_percentage', models.DecimalField(decimal_places=2, default=10, max_digits=5)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
