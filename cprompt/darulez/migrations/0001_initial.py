# Generated by Django 5.0.6 on 2024-05-23 02:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=70)),
            ],
        ),
        migrations.CreateModel(
            name='DocumentRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('sent', models.DateTimeField(blank=True, null=True)),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='darulez.application')),
            ],
        ),
        migrations.CreateModel(
            name='DocumentRule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(default='doc_request', max_length=15)),
                ('conditions', models.JSONField()),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='darulez.school')),
            ],
        ),
        migrations.AddField(
            model_name='application',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='darulez.school'),
        ),
    ]