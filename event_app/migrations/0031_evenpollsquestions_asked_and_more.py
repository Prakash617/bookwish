# Generated by Django 4.1.5 on 2023-04-29 22:57

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('event_app', '0030_remove_evenpollsquestions_results'),
    ]

    operations = [
        migrations.AddField(
            model_name='evenpollsquestions',
            name='asked',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='evenpollsquestions',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='evenpollsquestions',
            name='event',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='event_polls', to='event_app.event'),
        ),
    ]
