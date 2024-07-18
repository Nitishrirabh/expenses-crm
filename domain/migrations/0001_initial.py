# Generated by Django 5.0.7 on 2024-07-18 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DomainDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain_name', models.CharField(max_length=255)),
                ('expiry_date', models.DateField()),
                ('ssl_expiry_date', models.DateField()),
                ('server_name', models.CharField(max_length=255)),
                ('server_hosted_on', models.CharField(max_length=255)),
                ('server_expiry_date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'domain_details',
            },
        ),
    ]
