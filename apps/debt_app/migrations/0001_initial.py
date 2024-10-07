# Generated by Django 5.1.1 on 2024-10-06 10:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('builder_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DebtModel',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('phone_number', models.CharField(max_length=15)),
                ('phone_number2', models.CharField(blank=True, max_length=15, null=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('is_paid', models.BooleanField(default=False)),
                ('amount', models.DecimalField(decimal_places=3, default=0.0, max_digits=15)),
                ('builder', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='debts', to='builder_app.buildermodel')),
            ],
            options={
                'verbose_name_plural': 'debts',
                'db_table': 'debt',
                'ordering': ['id'],
            },
        ),
    ]
