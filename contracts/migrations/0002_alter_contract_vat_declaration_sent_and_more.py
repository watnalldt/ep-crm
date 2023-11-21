# Generated by Django 4.2.7 on 2023-11-21 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='vat_declaration_sent',
            field=models.CharField(choices=[('YES', 'Yes'), ('NO', 'No')], default='NO', verbose_name='Vat Declaration Sent'),
        ),
        migrations.AlterField(
            model_name='historicalcontract',
            name='vat_declaration_sent',
            field=models.CharField(choices=[('YES', 'Yes'), ('NO', 'No')], default='NO', verbose_name='Vat Declaration Sent'),
        ),
    ]