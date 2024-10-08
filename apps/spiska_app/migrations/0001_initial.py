# Generated by Django 5.1.1 on 2024-10-06 10:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpiskaModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('item', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='product_app.itemmodel')),
            ],
            options={
                'verbose_name_plural': 'spiskas',
                'db_table': 'spiska',
                'ordering': ['-id'],
            },
        ),
    ]
