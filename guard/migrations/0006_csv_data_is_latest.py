# Generated by Django 5.0.7 on 2024-07-18 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guard', '0005_csv_data_file_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='csv_data',
            name='is_latest',
            field=models.BooleanField(default=False),
        ),
    ]