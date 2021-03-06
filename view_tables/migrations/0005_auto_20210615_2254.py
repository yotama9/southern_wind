# Generated by Django 3.2.4 on 2021-06-15 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('view_tables', '0004_auto_20210521_2038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adventure',
            name='max_level',
            field=models.IntegerField(blank=True, help_text='What is the maximum character level for this adventure?'),
        ),
        migrations.AlterField(
            model_name='adventure',
            name='min_level',
            field=models.IntegerField(blank=True, help_text='What is the minimum character level for this adventure?'),
        ),
    ]
