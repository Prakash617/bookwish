# Generated by Django 4.1.5 on 2023-02-12 16:57

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ActiveUsers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('active_user_count', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='AppInstalls',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('app_installs_count', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='BasicInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('founder_name', models.CharField(blank=True, max_length=200)),
                ('founder_image', models.CharField(blank=True, max_length=200)),
                ('founder_bio', models.CharField(blank=True, max_length=200)),
                ('founder_message', models.TextField(blank=True, max_length=9999)),
                ('about_us', models.CharField(blank=True, max_length=9999)),
                ('about_mission', models.CharField(blank=True, max_length=1000)),
                ('about_vision', models.CharField(blank=True, max_length=1000)),
                ('contact_phone1', models.BigIntegerField(blank=True, null=True)),
                ('contact_phone2', models.BigIntegerField(blank=True, null=True)),
                ('contact_address', models.CharField(blank=True, max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article_title', models.CharField(max_length=999)),
                ('article_slug', models.CharField(max_length=999)),
                ('feature_image', models.URLField(max_length=999)),
                ('article_body', models.TextField()),
                ('post_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Bookings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_date', models.DateField()),
                ('attendee_name', models.CharField(max_length=200)),
                ('attendee_address', models.CharField(max_length=500)),
                ('ateendee_contact', models.BigIntegerField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='CommonQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=999)),
                ('answer', models.TextField(max_length=999)),
            ],
        ),
        migrations.CreateModel(
            name='HomepageButton',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=999)),
                ('link', models.URLField(max_length=999)),
            ],
        ),
        migrations.CreateModel(
            name='HomeResource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=300)),
                ('iframe_code', models.TextField(max_length=999)),
            ],
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=300, null=True)),
                ('product_description', models.TextField(max_length=999, null=True)),
                ('product_price', models.IntegerField(null=True)),
                ('product_photos', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=3000), size=3)),
            ],
        ),
        migrations.CreateModel(
            name='Socials',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fb_url', models.URLField(blank=True, max_length=999)),
                ('in_url', models.URLField(blank=True, max_length=999)),
                ('yt_url', models.URLField(blank=True, max_length=999)),
                ('app_url', models.URLField(blank=True, max_length=999)),
                ('ln_url', models.URLField(blank=True, max_length=999)),
            ],
        ),
        migrations.CreateModel(
            name='Testimonials',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.CharField(max_length=200)),
                ('intro', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=100)),
                ('message', models.CharField(max_length=2000)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_date', models.DateField()),
                ('quantity', models.IntegerField()),
                ('status', models.CharField(choices=[('approved', 'approved'), ('unapproved', 'unapproved'), ('completed', 'completed')], default='unapproved', max_length=100)),
                ('payment_type', models.CharField(choices=[('Cash on Delivery', 'Cash on Delivery'), ('Online', 'Online')], default='online', max_length=100)),
                ('customer_name', models.CharField(max_length=999)),
                ('customer_phone', models.CharField(max_length=999)),
                ('delivery_address', models.CharField(max_length=999)),
                ('payment_info', models.JSONField()),
                ('order_item', models.ManyToManyField(to='website.shop')),
            ],
        ),
    ]