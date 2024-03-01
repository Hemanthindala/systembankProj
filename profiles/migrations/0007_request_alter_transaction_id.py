# Generated by Django 4.2.10 on 2024-02-24 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0006_alter_moneytransfer_enter_the_amount_to_be_transferred_in_inr_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('from_account_number', models.IntegerField()),
                ('to_account_number', models.IntegerField()),
                ('amount_transferred', models.DecimalField(decimal_places=2, max_digits=10)),
                ('request_resolved', models.BooleanField(default=False)),
                ('date_and_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterField(
            model_name='transaction',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
