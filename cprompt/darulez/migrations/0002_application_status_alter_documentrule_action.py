# Generated by Django 5.0.6 on 2024-05-23 03:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('darulez', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='status',
            field=models.CharField(choices=[('new', 'New'), ('submitted', 'Submitted')], default='new', max_length=15),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='documentrule',
            name='action',
            field=models.CharField(choices=[('doc_request', 'Document Request')], default='doc_request', max_length=15),
        ),
    ]
