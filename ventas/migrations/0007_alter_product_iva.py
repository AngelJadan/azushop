# Generated by Django 4.2.3 on 2023-07-22 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0006_alter_product_id_publisher'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='iva',
            field=models.CharField(choices=[('0', '0%'), ('12', '12%')], db_column='pro_iva', max_length=2, verbose_name='IVA'),
        ),
    ]
