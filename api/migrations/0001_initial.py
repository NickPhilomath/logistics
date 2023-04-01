# Generated by Django 4.1.7 on 2023-03-30 15:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Action",
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
                (
                    "operation",
                    models.CharField(
                        choices=[
                            ("cre", "create"),
                            ("upd", "update"),
                            ("del", "delete"),
                            ("dea", "deactivate"),
                            ("act", "activate"),
                            ("inv", "invite"),
                            ("exp", "expire"),
                        ],
                        max_length=3,
                    ),
                ),
                ("target", models.BigIntegerField(null=True)),
                (
                    "target_name",
                    models.CharField(
                        choices=[
                            ("dri", "driver"),
                            ("use", "user"),
                            ("gro", "gross"),
                            ("car", "carrier"),
                            ("veh", "vehicle"),
                            ("tra", "trailer"),
                            ("lin", "invite link"),
                        ],
                        max_length=3,
                    ),
                ),
                ("time", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Driver",
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
                ("first_name", models.CharField(max_length=20)),
                ("last_name", models.CharField(max_length=20)),
                (
                    "driver_type",
                    models.CharField(
                        choices=[
                            ("O88", "Owner operator - 88%"),
                            ("O85", "Owner operator - 85%"),
                            ("C30", "Company driver - 30%"),
                            ("C35", "Company driver - 35%"),
                            ("L", "Lease operator"),
                            ("R", "Rental operator"),
                        ],
                        default="L",
                        max_length=3,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("rea", "Ready"),
                            ("cov", "Covered"),
                            ("pre", "Prebooked"),
                            ("hom", "Home"),
                            ("enr", "Enroute"),
                            ("hol", "Holiday"),
                            ("res", "Rest"),
                            ("ina", "Inactive"),
                        ],
                        default="rea",
                        max_length=3,
                    ),
                ),
                (
                    "gross_target",
                    models.DecimalField(
                        decimal_places=2, default=10000.0, max_digits=9
                    ),
                ),
                ("notes", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "d_budget",
                    models.DecimalField(decimal_places=2, default=0, max_digits=9),
                ),
                (
                    "l_budget",
                    models.DecimalField(decimal_places=2, default=0, max_digits=9),
                ),
                (
                    "r_budget",
                    models.DecimalField(decimal_places=2, default=0, max_digits=9),
                ),
                ("last_status_change", models.DateTimeField(auto_now=True)),
                ("date_joined", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="EditDriver",
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
                ("first_name", models.CharField(max_length=20)),
                ("last_name", models.CharField(max_length=20)),
                (
                    "driver_type",
                    models.CharField(
                        choices=[
                            ("O88", "Owner operator - 88%"),
                            ("O85", "Owner operator - 85%"),
                            ("C30", "Company driver - 30%"),
                            ("C35", "Company driver - 35%"),
                            ("L", "Lease operator"),
                            ("R", "Rental operator"),
                        ],
                        default="L",
                        max_length=3,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("rea", "Ready"),
                            ("cov", "Covered"),
                            ("pre", "Prebooked"),
                            ("hom", "Home"),
                            ("enr", "Enroute"),
                            ("hol", "Holiday"),
                            ("res", "Rest"),
                            ("ina", "Inactive"),
                        ],
                        default="rea",
                        max_length=3,
                    ),
                ),
                (
                    "gross_target",
                    models.DecimalField(
                        decimal_places=2, default=10000.0, max_digits=9
                    ),
                ),
                ("notes", models.CharField(blank=True, max_length=255, null=True)),
                ("edit_time", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Trailer",
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
                ("number", models.CharField(max_length=20, unique=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("ius", "In use"),
                            ("uns", "Unused"),
                            ("rep", "Repairing"),
                        ],
                        default="uns",
                        max_length=3,
                    ),
                ),
                ("notes", models.CharField(blank=True, max_length=255, null=True)),
                ("last_trip", models.DateTimeField(null=True)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="EditTrailer",
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
                ("number", models.CharField(max_length=20, unique=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("ius", "In use"),
                            ("uns", "Unused"),
                            ("rep", "Repairing"),
                        ],
                        default="uns",
                        max_length=3,
                    ),
                ),
                ("notes", models.CharField(blank=True, max_length=255, null=True)),
                ("edit_time", models.DateTimeField(auto_now_add=True)),
                (
                    "trailer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="edit_trailer",
                        to="api.trailer",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
