# Generated by Django 4.1.5 on 2023-03-24 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0019_basicinfo_services_page'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total_price',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='productquantity',
            name='price',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_type',
            field=models.CharField(choices=[('Cash on Delivery', 'Cash on Delivery'), ('Online', 'Online')], default='Cash on Delivery', max_length=100),
        ),
    ]