# Generated by Django 5.1.3 on 2024-11-19 15:15

import django.db.models.deletion
import pos_app.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pos_app', '0006_alter_menuresto_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderMenu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(default=pos_app.models.increment_order_menu_code, editable=False, max_length=20)),
                ('order_status', models.CharField(choices=[('Belum Bayar', 'Belum Bayar'), ('Sudah Bayar', 'Sudah Bayar')], default='Belum Bayar', max_length=20)),
                ('total_order', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
                ('tax_order', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
                ('total_payment', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
                ('payment', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
                ('changed', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
                ('status', models.CharField(choices=[('Aktif', 'Aktif'), ('Tidak Aktif', 'Tidak Aktif')], default='Aktif', max_length=20)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('cashier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cashier_order_menu', to=settings.AUTH_USER_MODEL)),
                ('table_resto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='table_resto_order_menu', to='pos_app.tableresto')),
                ('user_create', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_create_order_menu', to=settings.AUTH_USER_MODEL)),
                ('user_update', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_update_order_menu', to=settings.AUTH_USER_MODEL)),
                ('waitress', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='waitress_order_menu', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
