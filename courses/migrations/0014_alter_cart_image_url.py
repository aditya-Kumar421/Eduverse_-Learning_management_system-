# Generated by Django 5.0 on 2024-02-05 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0013_alter_cart_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='image_url',
            field=models.URLField(default='https://assets-global.website-files.com/62e95dddfb380a0e61193e7d/634970c7cbeed5644711b937_62fd57ccd6890f25796f92f9_AdobeStock_295461823.jpeg'),
        ),
    ]
