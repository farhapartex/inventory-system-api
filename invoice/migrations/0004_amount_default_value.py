# Generated by Django 3.2.6 on 2021-08-24 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0003_create_by_invoice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
    ]
