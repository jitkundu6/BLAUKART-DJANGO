# Generated by Django 2.2.23 on 2021-05-13 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authtoken',
            name='token',
            field=models.CharField(default='EU1EOS', max_length=50),
        ),
    ]