# Generated by Django 5.1.3 on 2024-11-18 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pos_app', '0005_menuresto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuresto',
            name='description',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]