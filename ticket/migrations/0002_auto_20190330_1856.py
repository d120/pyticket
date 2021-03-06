# Generated by Django 2.1.7 on 2019-03-30 17:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='assigned_group',
            field=models.ForeignKey(blank=True, help_text='Die Gruppe, für die das Ticket interessant ist.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth.Group', verbose_name='gruppe'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='ignored_by',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, verbose_name='ignoriert bei'),
        ),
    ]
