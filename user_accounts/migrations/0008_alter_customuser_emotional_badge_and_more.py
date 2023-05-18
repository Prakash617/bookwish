# Generated by Django 4.1.5 on 2023-04-02 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_accounts', '0007_alter_customuser_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='emotional_badge',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='mental_badge',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='physical_badge',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='spiritual_badge',
            field=models.IntegerField(default=0),
        ),
    ]