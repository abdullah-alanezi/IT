# Generated by Django 5.0.7 on 2024-07-28 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itsupport', '0010_alter_maintenancerequest_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maintenancerequest',
            name='status',
            field=models.CharField(choices=[('مفتوح', 'مفتوح'), ('تحت الإجراء', 'تحت الإجراء'), ('منتهي', 'منتهي')], default='مفتوح', max_length=20),
        ),
    ]
