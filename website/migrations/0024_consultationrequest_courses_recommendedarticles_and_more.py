# Generated by Django 4.1.5 on 2023-04-06 03:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0023_alter_order_payment_info'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConsultationRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=100)),
                ('company', models.CharField(max_length=999)),
                ('message', models.TextField()),
                ('type', models.CharField(choices=[('Personal', 'Personal'), ('Professional', 'Professional')], default='Personal', max_length=999)),
            ],
        ),
        migrations.CreateModel(
            name='Courses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='website/course')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('time', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='RecommendedArticles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='website/course')),
                ('description', models.TextField()),
                ('link', models.URLField(blank=True, max_length=999)),
            ],
        ),
        migrations.CreateModel(
            name='RecommendedBooks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='website/course')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('link', models.URLField(blank=True, max_length=999)),
            ],
        ),
        migrations.CreateModel(
            name='RecommendedVideos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_link', models.URLField(blank=True, max_length=999)),
                ('description', models.TextField()),
                ('name', models.CharField(max_length=100)),
                ('iframe', models.CharField(max_length=100)),
            ],
        ),
    ]
