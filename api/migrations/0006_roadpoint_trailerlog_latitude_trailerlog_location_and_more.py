# Generated by Django 4.1.7 on 2023-04-01 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0005_trailerlog"),
    ]

    operations = [
        migrations.CreateModel(
            name="RoadPoint",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("latitude", models.DecimalField(decimal_places=9, max_digits=12)),
                ("longitude", models.DecimalField(decimal_places=9, max_digits=12)),
                ("altitude", models.IntegerField(null=True)),
                ("address", models.CharField(max_length=255, null=True)),
                (
                    "degree",
                    models.DecimalField(decimal_places=1, max_digits=4, null=True),
                ),
                ("speed", models.DecimalField(decimal_places=3, max_digits=6)),
            ],
        ),
        migrations.AddField(
            model_name="trailerlog",
            name="latitude",
            field=models.DecimalField(decimal_places=9, default=0.0, max_digits=12),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="trailerlog",
            name="location",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="trailerlog",
            name="longitude",
            field=models.DecimalField(decimal_places=9, default=0.0, max_digits=12),
            preserve_default=False,
        ),
    ]
