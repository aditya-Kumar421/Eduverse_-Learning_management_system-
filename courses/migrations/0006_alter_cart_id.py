# Generated by Django 5.0 on 2024-01-13 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_cart_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
