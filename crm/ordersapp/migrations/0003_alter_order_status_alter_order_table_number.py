# Generated by Django 5.1.6 on 2025-02-28 02:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ordersapp", "0002_order_total_price"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="status",
            field=models.CharField(
                choices=[
                    ("pending", "В ожидании"),
                    ("ready", "Готово"),
                    ("paid", "Оплачено"),
                ],
                db_index=True,
                default="pending",
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="table_number",
            field=models.IntegerField(db_index=True),
        ),
    ]
