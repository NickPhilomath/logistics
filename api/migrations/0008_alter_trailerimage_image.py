# Generated by Django 4.2 on 2023-04-03 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0007_trailerimage"),
    ]

    operations = [
        migrations.AlterField(
            model_name="trailerimage",
            name="image",
            field=models.ImageField(upload_to="trailer_images"),
        ),
    ]
