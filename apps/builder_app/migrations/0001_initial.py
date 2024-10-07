# Generated by Django 5.1.1 on 2024-10-06 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BuilderModel',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fish', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=9, unique=True)),
                ('phone_number2', models.CharField(blank=True, max_length=9, null=True, unique=True)),
                ('address', models.CharField(max_length=255)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'builders',
                'db_table': 'builder',
                'ordering': ['id'],
            },
        ),
    ]
