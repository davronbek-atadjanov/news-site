# Generated by Django 5.0.3 on 2024-04-12 06:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("news_app", "0003_comment"),
    ]

    operations = [
        migrations.AddField(
            model_name="news",
            name="view_count",
            field=models.IntegerField(default=0),
        ),
    ]
