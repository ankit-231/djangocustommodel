# Generated by Django 4.1.7 on 2023-03-21 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0005_studentsnew_is_deleted"),
    ]

    operations = [
        migrations.AlterField(
            model_name="studentsnew",
            name="is_deleted",
            field=models.IntegerField(default=0, max_length=1),
        ),
    ]
