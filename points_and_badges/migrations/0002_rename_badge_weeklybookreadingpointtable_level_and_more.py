# Generated by Django 4.1.5 on 2023-02-24 06:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('points_and_badges', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='weeklybookreadingpointtable',
            old_name='badge',
            new_name='level',
        ),
        migrations.RenameField(
            model_name='weeklymeditationpointtable',
            old_name='badge',
            new_name='level',
        ),
        migrations.RenameField(
            model_name='weeklyphysicalpointtable',
            old_name='badge',
            new_name='level',
        ),
        migrations.RenameField(
            model_name='weeklyrelationshippointtable',
            old_name='badge',
            new_name='level',
        ),
    ]
